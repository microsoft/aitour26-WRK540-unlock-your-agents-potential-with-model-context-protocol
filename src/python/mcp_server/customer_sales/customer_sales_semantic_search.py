#!/usr/bin/env python3
"""
Provides comprehensive customer sales database access with semantic search functionality for Zava Retail DIY Business.
This MCP server combines traditional product name search with AI-powered semantic search using embeddings.
"""

import argparse
import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Annotated, Optional

from customer_sales_postgres import PostgreSQLCustomerSales
from customer_sales_semantic_search_text_embeddings import SemanticSearchTextEmbedding
from mcp.server.fastmcp import Context, FastMCP
from pydantic import Field

RLS_USER_ID = None


@dataclass
class AppContext:
    """Application context containing database connection and semantic search tool."""

    db: PostgreSQLCustomerSales
    semantic_search: SemanticSearchTextEmbedding


@asynccontextmanager
async def app_lifespan(_server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage application lifecycle with type-safe context"""

    db = PostgreSQLCustomerSales()
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
            print(f"⚠️  Error closing database pool: {e}")


# Create MCP server with lifespan support
mcp = FastMCP("mcp-zava-sales-semantic",
              lifespan=app_lifespan, stateless_http=True)


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


def get_app_context() -> AppContext:
    """Get the application context from MCP context."""
    ctx = mcp.get_context()
    app_context = ctx.request_context.lifespan_context
    if isinstance(app_context, AppContext):
        return app_context
    raise RuntimeError("Invalid lifespan context type")


@mcp.tool()
async def semantic_search_products(
    ctx: Context,
    query_description: Annotated[str, Field(description="Use Natural language description to find products that Zava sells.")],
    max_rows: Annotated[int, Field(
        description="Maximum number of rows to return.")] = 10,
    similarity_threshold: Annotated[float, Field(
        description="Minimum similarity threshold (0-100) to consider a product a match.")] = 50.0
) -> str:
    """Search for products using semantic similarity based on natural language descriptions. This tool uses AI embeddings to find products that match the meaning and intent of your
    description, even if the exact words don't appear in the product names.

    Args:
        query_description: Use Natural language description to find products that Zava sells.. 
                          (e.g., "waterproof electrical box for outdoor use", "15 amp circuit breaker")
        max_rows: Maximum number of rows to return.

    Returns:
        Query results with similarity scores as a string.
    """

    rls_user_id = get_rls_user_id(ctx)

    print(f"Semantic search query: {query_description}")
    print(f"Manager ID: {rls_user_id}")
    print(f"Max Rows: {max_rows}")

    try:
        app_context = get_app_context()

        # Check if semantic search is available
        if not app_context.semantic_search.is_available():
            return "Error: Semantic search is not available. Azure OpenAI endpoint not configured."

        # Generate embedding for the query
        query_embedding = app_context.semantic_search.generate_query_embedding(
            query_description)
        if not query_embedding:
            return "Error: Failed to generate embedding for the query. Please try again."

        # Search for similar products using the embedding
        result = await app_context.db.search_products_by_similarity(query_embedding, rls_user_id=rls_user_id, max_rows=max_rows, similarity_threshold=similarity_threshold)
        return f"Semantic Search Results:\n{result}"

    except Exception as e:
        return f"Error executing semantic search: {e!s}"


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
