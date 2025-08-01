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

from customer_sales_postgres import PostgreSQLCustomerSales
from mcp.server.fastmcp import Context, FastMCP
from pydantic import Field

RLS_USER_ID = None


@dataclass
class AppContext:
    """Application context containing database connection."""

    db: PostgreSQLCustomerSales


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage application lifecycle with type-safe context"""

    db = PostgreSQLCustomerSales()
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


def get_db_provider() -> PostgreSQLCustomerSales:
    """Get the database provider instance from context."""
    ctx = mcp.get_context()
    app_context = ctx.request_context.lifespan_context
    if isinstance(app_context, AppContext):
        return app_context.db
    raise RuntimeError("Invalid lifespan context type")


@mcp.tool()
async def get_products_by_name(
    ctx: Context,
    product_name: Annotated[str, Field(description="Name of the product to search for.")],
    max_rows: Annotated[int, Field(
        description="Maximum number of rows to return.")] = 20
) -> str:
    """Get products by name using a PostgreSQL query.

    Args:
        max_rows: Maximum number of rows to return.

    Returns:
        Query results as a string.
    """

    rls_user_id = get_rls_user_id(ctx)

    print(f"Manager ID: {rls_user_id}")
    print(f"Max Rows: {max_rows}")

    try:

        provider = get_db_provider()
        result = await provider.get_products_by_name(product_name, max_rows, rls_user_id=rls_user_id)
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
    print(
        f"❤️ 📡 MCP endpoint available at: http://{mcp.settings.host}:{mcp.settings.port}/mcp")

    # Run the FastMCP server as HTTP endpoint
    await mcp.run_streamable_http_async()


def main() -> None:
    """Main entry point for the MCP server."""
    global RLS_USER_ID

    parser = argparse.ArgumentParser()
    parser.add_argument("--stdio", action="store_true",
                        help="Run server in stdio mode")
    parser.add_argument("--RLS_USER_ID", type=str,
                        default=None, help="Row Level Security User ID")
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
