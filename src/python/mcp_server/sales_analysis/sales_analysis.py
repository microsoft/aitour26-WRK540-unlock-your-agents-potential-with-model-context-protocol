#!/usr/bin/env python3
"""
Provides comprehensive customer sales database access with individual table schema tools for Zava Retail DIY Business.
"""

import argparse
import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Annotated, Optional

from mcp.server.fastmcp import Context, FastMCP
from pydantic import Field
from sales_analysis_postgres import PostgreSQLSchemaProvider

RLS_USER_ID = None


@dataclass
class AppContext:
    """Application context containing database connection."""

    db: PostgreSQLSchemaProvider


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage application lifecycle with type-safe context"""

    db = PostgreSQLSchemaProvider()
    # Use connection pool instead of single connection for HTTP server
    await db.create_pool()

    try:
        yield AppContext(db=db)
    finally:
        # Cleanup on shutdown
        try:
            await db.close_pool()
        except Exception as e:
            print(f"⚠️  Error closing database pool: {e}")


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
        return f"Error: Invalid table names: {invalid_tables}. Valid tables are: {sorted(valid_tables)}"

    print(f"Manager ID: {rls_user_id}")
    print(f"Retrieving schemas for tables: {', '.join(table_names)}")

    try:
        provider = get_db_provider()
        return await provider.get_table_metadata_from_list(table_names, rls_user_id=rls_user_id)
    except Exception as e:
        return f"Error retrieving table schemas: {e!s}"


@mcp.tool()
async def execute_sales_query(
    ctx: Context, postgresql_query: Annotated[str, Field(description="A well-formed PostgreSQL query.")]
) -> str:
    """Always fetch and inspect the database schema before generating any SQL; use only exact table and column names, and never invent or infer data, columns, tables, or values—if the information isn’t present in the schema or database, clearly state that it cannot be answered. Join related tables for clarity, aggregate results where appropriate, and limit output to 20 rows with a note that the limit is for readability. To identify store types, use the retail.store.is_online boolean: true indicates an online store, false indicates a physical store.

    Args:
        postgresql_query: A well-formed PostgreSQL query.

    Returns:
        Query results as a string.
    """

    rls_user_id = get_rls_user_id(ctx)

    print(f"Manager ID: {rls_user_id}")
    print(f"Executing PostgreSQL query: {postgresql_query}")

    try:
        if not postgresql_query:
            return "Error: postgresql_query parameter is required"

        provider = get_db_provider()
        result = await provider.execute_query(postgresql_query, rls_user_id=rls_user_id)
        return f"Query Results:\n{result}"

    except Exception as e:
        return f"Error executing database query: {e!s}"


@mcp.tool()
async def get_current_utc_date() -> str:
    """Get the current UTC date and time in ISO format. Useful for date-based queries, filtering recent data, or understanding the current context for time-sensitive analysis.

    Returns:
        Current UTC date and time in ISO format (YYYY-MM-DDTHH:MM:SS.fffffZ)
    """
    print("Retrieving current UTC date and time")
    try:
        current_utc = datetime.now(timezone.utc)
        return f"Current UTC Date/Time: {current_utc.isoformat()}"
    except Exception as e:
        return f"Error retrieving current UTC date: {e!s}"


async def run_http_server() -> None:
    """Run the MCP server in HTTP mode."""
    print(f"❤️ 📡 MCP endpoint available at: http://{mcp.settings.host}:{mcp.settings.port}/mcp")

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
