#!/usr/bin/env python3
"""
Provides comprehensive customer sales database access with individual table schema tools for Zava Retail DIY Business.
"""

import asyncio
import logging
import os
from datetime import datetime, timezone
from typing import Annotated, Optional

from azure.monitor.opentelemetry import configure_azure_monitor
from config import Config
from mcp.server.fastmcp import Context, FastMCP
from opentelemetry.instrumentation.starlette import StarletteInstrumentor
from pydantic import Field
from sales_analysis_postgres import PostgreSQLSchemaProvider
from sales_analysis_text_embeddings import SemanticSearchTextEmbedding

config = Config()

logger = logging.getLogger(__name__)

for name in [
    "azure.core.pipeline.policies.http_logging_policy",
    "azure.ai.agents",
    "azure.ai.projects",
    "azure.core",
    "azure.identity",
    "uvicorn.access",
    "azure.monitor.opentelemetry.exporter.export._base",
]:
    logging.getLogger(name).setLevel(logging.WARNING)


db_provider = PostgreSQLSchemaProvider()
semantic_search_provider = SemanticSearchTextEmbedding()


# Create MCP server with lifespan support
mcp = FastMCP("mcp-zava-sales", stateless_http=True)


def get_header(ctx: Context, header_name: str) -> Optional[str]:
    """Extract a specific header from the request context."""

    request = ctx.request_context.request
    if request is not None and hasattr(request, "headers"):
        headers = request.headers
        if headers:
            header_value = headers.get(header_name)
            if header_value is not None:
                if isinstance(header_value, bytes):
                    return header_value.decode("utf-8")
                return str(header_value)

    return None


def get_rls_user_id(ctx: Context) -> str:
    """Get the Row Level Security User ID from the request context."""

    rls_user_id = get_header(ctx, "x-rls-user-id")
    if rls_user_id is None:
        # Default to a placeholder if not provided
        rls_user_id = "00000000-0000-0000-0000-000000000000"
    return rls_user_id


# @mcp.tool()
async def semantic_search_products(
    ctx: Context,
    query_description: Annotated[
        str,
        Field(
            description="Describe the Zava product you're looking for using natural language. Include purpose, features, or use case. For example: 'waterproof electrical box for outdoor use', '15 amp circuit breaker', or 'LED light bulbs for kitchen ceiling'."
        ),
    ],
    max_rows: Annotated[int, Field(description="The maximum number of products to return. Defaults to 20.")] = 20,
    similarity_threshold: Annotated[
        float,
        Field(
            description="A value between 20 and 80 that sets the minimum similarity threshold. Products below this value are excluded. Defaults to 30.0."
        ),
    ] = 30.0,
) -> str:
    """
    Search for Zava products using natural language descriptions to find matches based on semantic similarity—considering functionality, form, use, and other attributes.

    Returns:
        A JSON-formatted string containing a list of matching products. Each result includes:
          - `product_id`: The product's unique identifier.
          - `sku`: The product's stock keeping unit.
          - `product_name`: The name of the product.
          - `category_id`: The ID of the product's category.
          - `type_id`: The ID of the product's type.
          - `cost`: The cost of the product.
          - `base_price`: The base price of the product.
          - `gross_margin_percent`: The gross margin percentage of the product.
          - `product_description`: The description of the product.
          - `similarity_distance`: Cosine similarity score between the query and product embedding.
    """

    rls_user_id = get_rls_user_id(ctx)

    logger.info("Semantic search query: %s", query_description)
    logger.info("Manager ID: %s", rls_user_id)
    logger.info("Max Rows: %d", max_rows)

    try:
        # Check if semantic search is available
        if not semantic_search_provider.is_available():
            return "Error: Semantic search is not available. Azure OpenAI endpoint not configured."

        # Generate embedding for the query
        query_embedding = semantic_search_provider.generate_query_embedding(query_description)
        if not query_embedding:
            return "Error: Failed to generate embedding for the query. Please try again."

        # Search for similar products using the embedding
        return await db_provider.search_products_by_similarity(
            query_embedding, rls_user_id=rls_user_id, max_rows=max_rows, similarity_threshold=similarity_threshold
        )

    except Exception as e:
        logger.error("Error executing semantic search: %s", e)
        return "Error executing semantic search"


@mcp.tool()
async def get_multiple_table_schemas(
    ctx: Context,
    table_names: Annotated[
        list[str],
        Field(
            description="List of table names. Valid table names include 'retail.customers', 'retail.stores', 'retail.categories', 'retail.product_types', 'retail.products', 'retail.orders', 'retail.order_items', 'retail.inventory'."
        ),
    ],
) -> str:
    """
    Retrieve schemas for multiple tables. Use this tool only for schemas you have not already fetched during the conversation.

    Args:
        table_names: List of table names. Valid table names include 'retail.customers', 'retail.stores', 'retail.categories', 'retail.product_types', 'retail.products', 'retail.orders', 'retail.order_items', 'retail.inventory'.

    Returns:
        Concatenated schema strings for the requested tables.
    """

    rls_user_id = get_rls_user_id(ctx)

    if not table_names:
        logger.error("Error: table_names parameter is required and cannot be empty")
        return "Error: table_names parameter is required and cannot be empty"

    valid_tables = {
        "retail.customers",
        "retail.stores",
        "retail.categories",
        "retail.product_types",
        "retail.products",
        "retail.orders",
        "retail.order_items",
        "retail.inventory",
    }

    # Validate table names
    invalid_tables = [name for name in table_names if name not in valid_tables]
    if invalid_tables:
        logger.error("Error: Invalid table names: %s. Valid tables are: %s", invalid_tables, sorted(valid_tables))
        return f"Error: Invalid table names: {invalid_tables}. Valid tables are: {sorted(valid_tables)}"

    logger.info("Manager ID: %s", rls_user_id)
    logger.info("Retrieving schemas for tables: %s", ", ".join(table_names))

    try:
        return await db_provider.get_table_metadata_from_list(table_names, rls_user_id=rls_user_id)
    except Exception as e:
        logger.error("Error retrieving table schemas: %s", e)
        return f"Error retrieving table schemas: {e!s}"


@mcp.tool()
async def execute_sales_query(
    ctx: Context, postgresql_query: Annotated[str, Field(description="A well-formed PostgreSQL query.")]
) -> str:
    """Always fetch and inspect the database schema before generating any SQL using the get_multiple_table_schemas tool; use only exact table and column names, and never invent or infer data, columns, tables, or values—if the information isn't present in the schema or database, clearly state that it cannot be answered. Join related tables for clarity, aggregate results where appropriate, and limit output to 20 rows with a note that the limit is for readability. To identify store types, use the retail.store.is_online boolean: true indicates an online store, false indicates a physical store. **NEVER** return entity IDs or UUIDs in the response, as they are not meaningful to the user. Instead, use descriptive names or values.

    Args:
        postgresql_query: A well-formed PostgreSQL query.

    Returns:
        Query results as a string.
    """

    rls_user_id = get_rls_user_id(ctx)

    logger.info("Manager ID: %s", rls_user_id)
    logger.info("Executing PostgreSQL query: %s", postgresql_query)

    try:
        if not postgresql_query:
            return "Error: postgresql_query parameter is required"

        result = await db_provider.execute_query(postgresql_query, rls_user_id=rls_user_id)
        return f"Query Results:\n{result}"

    except Exception as e:
        logger.error("Error executing database query: %s", e)
        return f"Error executing database query: {e!s}"


@mcp.tool()
async def get_current_utc_date() -> str:
    """Get the current UTC date and time in ISO format. Useful for date time relative queries or understanding the current date for time-sensitive analysis.

    Returns:
        Current UTC date and time in ISO format (YYYY-MM-DDTHH:MM:SS.fffffZ)
    """
    logger.info("Retrieving current UTC date and time")
    try:
        current_utc = datetime.now(timezone.utc)
        return f"Current UTC Date/Time: {current_utc.isoformat()}"
    except Exception as e:
        logger.error("Error retrieving current UTC date: %s", e)
        return f"Error retrieving current UTC date: {e!s}"


@mcp.tool()
async def get_sales_by_region(ctx: Context) -> str:
    """Get aggregated sales data grouped by geographic regions. This query groups Zava stores into logical regions and provides comprehensive sales metrics including total orders, total sales, average order item value, and unique customers by region.

    The regions are defined as follows:
    - Seattle Metro: Seattle, Bellevue, Kirkland, Redmond
    - Online: Zava Retail Online
    - Puget Sound: Everett, Tacoma  
    - Eastern Washington: Spokane

    Returns:
        Formatted table showing sales metrics by region with key insights.
    """
    
    rls_user_id = get_rls_user_id(ctx)
    
    logger.info("Manager ID: %s", rls_user_id)
    logger.info("Executing sales by region query")

    try:
        # SQL query to aggregate sales by region
        query = """
        WITH regional_mapping AS (
            SELECT 
                store_id,
                store_name,
                CASE 
                    WHEN store_name IN ('Zava Retail Seattle', 'Zava Retail Bellevue', 'Zava Retail Kirkland', 'Zava Retail Redmond') THEN 'Seattle Metro'
                    WHEN store_name = 'Zava Retail Online' THEN 'Online'
                    WHEN store_name IN ('Zava Retail Everett', 'Zava Retail Tacoma') THEN 'Puget Sound'
                    WHEN store_name = 'Zava Retail Spokane' THEN 'Eastern Washington'
                    ELSE 'Other'
                END AS region
            FROM retail.stores
        ),
        regional_sales AS (
            SELECT 
                rm.region,
                COUNT(DISTINCT o.order_id) AS total_orders,
                ROUND(SUM(oi.total_amount), 2) AS total_sales,
                ROUND(AVG(oi.total_amount), 2) AS avg_order_item_value,
                COUNT(DISTINCT o.customer_id) AS unique_customers
            FROM regional_mapping rm
            JOIN retail.orders o ON rm.store_id = o.store_id
            JOIN retail.order_items oi ON o.order_id = oi.order_id
            GROUP BY rm.region
        )
        SELECT 
            region,
            total_orders,
            CONCAT('$', TO_CHAR(total_sales, 'FM999,999,999.00')) AS total_sales_formatted,
            total_sales,
            CONCAT('$', TO_CHAR(avg_order_item_value, 'FM999.00')) AS avg_order_item_value_formatted,
            unique_customers,
            ROUND((total_sales / SUM(total_sales) OVER ()) * 100, 1) AS percentage_of_total_sales
        FROM regional_sales
        ORDER BY total_sales DESC
        LIMIT 20
        """
        
        result = await db_provider.execute_query(query, rls_user_id=rls_user_id)
        
        # Format the results into a readable table format
        formatted_result = "## Sales by Region\n\n"
        formatted_result += "| Region | Total Orders | Total Sales | Avg Order Item Value | Unique Customers | % of Total |\n"
        formatted_result += "|--------|-------------|-------------|---------------------|------------------|------------|\n"
        
        # Parse the query results and format them
        lines = result.strip().split('\n')
        if len(lines) > 1:  # Skip header line if present
            for line in lines[1:]:  # Skip the header
                if line.strip() and '|' in line:
                    parts = [p.strip() for p in line.split('|')[1:-1]]  # Remove empty first and last parts
                    if len(parts) >= 6:
                        region = parts[0]
                        total_orders = parts[1]
                        total_sales_formatted = parts[2]
                        avg_formatted = parts[4]
                        unique_customers = parts[5]
                        percentage = parts[6] if len(parts) > 6 else "N/A"
                        
                        formatted_result += f"| **{region}** | {total_orders:,} | {total_sales_formatted} | {avg_formatted} | {unique_customers:,} | {percentage}% |\n"
        
        formatted_result += "\n### Key Insights:\n\n"
        formatted_result += "1. **Regional Performance**: Shows the relative performance of each geographic region\n"
        formatted_result += "2. **Market Share**: Percentage distribution helps identify the strongest markets\n"
        formatted_result += "3. **Customer Base**: Unique customer counts indicate market penetration by region\n"
        formatted_result += "4. **Average Order Value**: Helps identify regions with higher-value transactions\n\n"
        formatted_result += "*Results are limited to 20 regions for readability*"
        
        return formatted_result

    except Exception as e:
        logger.error("Error executing sales by region query: %s", e)
        return f"Error executing sales by region query: {e!s}"


async def run_http_server() -> None:
    """Run the MCP server in HTTP mode."""

    # Only configure azure monitor if running in HTTP mode
    # when running in STDIO mode, it will already be configured
    # from the host application
    configure_azure_monitor(connection_string=config.APPLICATIONINSIGHTS_CONNECTION_STRING)

    # Ensure a single connection pool is created once for the process.
    try:
        await db_provider.create_pool()

        mcp.settings.port = int(os.getenv("PORT", mcp.settings.port))
        StarletteInstrumentor().instrument_app(mcp.sse_app())
        StarletteInstrumentor().instrument_app(mcp.streamable_http_app())
        logger.info(
            "❤️ 📡 MCP endpoint available at: http://%s:%d/mcp",
            mcp.settings.host,
            mcp.settings.port,
        )

        # Run the FastMCP server as HTTP endpoint
        await mcp.run_streamable_http_async()
    finally:
        # Close the pool on shutdown
        try:
            await db_provider.close_pool()
        except Exception as e:
            logger.error("⚠️  Error closing database pool: %s", e)


def main() -> None:
    """Main entry point for the MCP server."""

    # Run the HTTP server
    asyncio.run(run_http_server())


if __name__ == "__main__":
    main()
