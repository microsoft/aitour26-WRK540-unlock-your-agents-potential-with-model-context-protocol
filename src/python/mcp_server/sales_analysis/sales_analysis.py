#!/usr/bin/env python3
"""
Provides comprehensive customer sales database access with individual table schema tools for Zava Retail DIY Business.
"""

import argparse
import asyncio
import logging
import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Annotated, Optional

from azure.monitor.opentelemetry import configure_azure_monitor
from config import Config
from mcp.server.fastmcp import Context, FastMCP
from opentelemetry.instrumentation.starlette import StarletteInstrumentor
from pydantic import Field
from sales_analysis_postgres import PostgreSQLSchemaProvider
from sales_analysis_text_embeddings import SemanticSearchTextEmbedding

RLS_USER_ID = None
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


@dataclass
class AppContext:
    """Application context containing database connection."""

    db: PostgreSQLSchemaProvider
    semantic_search: SemanticSearchTextEmbedding


@asynccontextmanager
async def app_lifespan() -> AsyncIterator[AppContext]:
    """Manage application lifecycle with type-safe context"""

    db = PostgreSQLSchemaProvider()
    semantic_search = SemanticSearchTextEmbedding()
    # Use connection pool instead of single connection for HTTP server
    await db.create_pool()

    try:
        yield AppContext(db=db, semantic_search=semantic_search)
    finally:
        # Cleanup on shutdown
        try:
            await db.close_pool()
        except Exception as e:
            logger.error("⚠️  Error closing database pool: %s", e)


# Create MCP server with lifespan support
mcp = FastMCP("mcp-zava-sales", lifespan=app_lifespan, stateless_http=True)


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

    # if running in stdio mode, use the global RLS_USER_ID passed as an argument
    if RLS_USER_ID is not None:
        return RLS_USER_ID

    rls_user_id = get_header(ctx, "x-rls-user-id")
    if rls_user_id is None:
        # Default to a placeholder if not provided
        rls_user_id = "00000000-0000-0000-0000-000000000000"
    return rls_user_id


def get_db_provider() -> PostgreSQLSchemaProvider:
    """Get the database provider instance from context."""
    ctx = mcp.get_context()
    app_context = ctx.request_context.lifespan_context
    if isinstance(app_context, AppContext):
        return app_context.db
    raise RuntimeError("Invalid lifespan context type")


def get_app_context() -> AppContext:
    """Get the application context from MCP context."""
    ctx = mcp.get_context()
    app_context = ctx.request_context.lifespan_context
    if isinstance(app_context, AppContext):
        return app_context
    raise RuntimeError("Invalid lifespan context type")


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
        app_context = get_app_context()

        # Check if semantic search is available
        if not app_context.semantic_search.is_available():
            return "Error: Semantic search is not available. Azure OpenAI endpoint not configured."

        # Generate embedding for the query
        query_embedding = app_context.semantic_search.generate_query_embedding(query_description)
        if not query_embedding:
            return "Error: Failed to generate embedding for the query. Please try again."

        # Search for similar products using the embedding
        return await app_context.db.search_products_by_similarity(
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
        provider = get_db_provider()
        return await provider.get_table_metadata_from_list(table_names, rls_user_id=rls_user_id)
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

        provider = get_db_provider()
        result = await provider.execute_query(postgresql_query, rls_user_id=rls_user_id)
        return f"Query Results:\n{result}"

    except Exception as e:
        logger.error("Error executing database query: %s", e)
        return f"Error executing database query: {e!s}"


@mcp.tool()
async def get_current_utc_date() -> str:
    """Get the current UTC date and time in ISO format. Useful for date-based queries, filtering recent data, or understanding the current context for time-sensitive analysis.

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


async def run_http_server() -> None:
    """Run the MCP server in HTTP mode."""

    # Only configure azure monitor if running in HTTP mode
    # when running in STDIO mode, it will already be configured
    # from the host application
    configure_azure_monitor(connection_string=config.APPLICATIONINSIGHTS_CONNECTION_STRING)

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


def main() -> None:
    """Main entry point for the MCP server."""
    global RLS_USER_ID

    parser = argparse.ArgumentParser()
    parser.add_argument("--stdio", action="store_true", help="Run server in stdio mode")
    parser.add_argument("--RLS_USER_ID", type=str, default=None, help="Row Level Security User ID")
    args = parser.parse_args()

    # if running in stdio mode, set the global RLS_USER_ID
    RLS_USER_ID = args.RLS_USER_ID

    if args.stdio:
        mcp.run()
    else:
        # Run the HTTP server
        asyncio.run(run_http_server())


if __name__ == "__main__":
    main()
