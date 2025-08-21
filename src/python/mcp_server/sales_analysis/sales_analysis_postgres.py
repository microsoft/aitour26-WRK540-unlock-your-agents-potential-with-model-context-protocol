#!/usr/bin/env python3
"""
AI-Friendly PostgreSQL Database Schema Tool

This script provides methods to query PostgreSQL database table schemas in AI-friendly formats
for dynamic query generation and AI model integration.

Usage:
    python sales_data_postgres.py

Requirements:
    - asyncpg (async PostgreSQL adapter)
    - asyncio (for async operations)
    - pandas (for structured JSON output)
    - python-dotenv (for environment variables)
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional

import asyncpg
from config import Config
from dotenv import load_dotenv
from opentelemetry.instrumentation.asyncpg import AsyncPGInstrumentor

# Load environment variables (don't override existing ones)
load_dotenv(override=False)

logger = logging.getLogger(__name__)
config = Config()

# Initialize AsyncPGInstrumentor with our tracer
AsyncPGInstrumentor().instrument()

# PostgreSQL connection configuration
POSTGRES_URL = config.POSTGRES_URL

SCHEMA_NAME = "retail"
MANAGER_ID = ""

# Constants - table names without schema prefix (will be added in queries)
CUSTOMERS_TABLE = "customers"
PRODUCTS_TABLE = "products"
ORDERS_TABLE = "orders"
ORDER_ITEMS_TABLE = "order_items"
STORES_TABLE = "stores"
CATEGORIES_TABLE = "categories"
PRODUCT_TYPES_TABLE = "product_types"
INVENTORY_TABLE = "inventory"


class PostgreSQLSchemaProvider:
    """Provides PostgreSQL database schema information in AI-friendly formats for dynamic query generation."""

    def __init__(self, postgres_config: Optional[str] = None) -> None:
        self.postgres_config = postgres_config or POSTGRES_URL
        self.connection_pool: Optional[asyncpg.Pool] = None
        self.all_schemas: Optional[Dict[str, Dict[str, Any]]] = None
        # In-memory cache for per-table schema look-ups
        self._schema_cache: Dict[str, Any] = {}

    async def __aenter__(self) -> "PostgreSQLSchemaProvider":
        """Async context manager entry - just return self, don't auto-create pool."""
        return self

    async def __aexit__(self, exc_type: Optional[type], exc_val: Optional[Exception], exc_tb: Optional[object]) -> None:
        """Async context manager exit - close connection pool if it was opened."""
        await self.close_pool()

    async def create_pool(self) -> None:
        """Create connection pool for better resource management."""
        if self.connection_pool is None:
            try:
                self.connection_pool = await asyncpg.create_pool(
                    self.postgres_config,
                    min_size=1,  # Minimum connections in pool
                    max_size=3,  # Very conservative pool size
                    command_timeout=30,  # 30 second query timeout
                    server_settings={
                        "jit": "off",  # Disable JIT to reduce memory usage
                        "work_mem": "4MB",  # Limit work memory per query
                        "statement_timeout": "30s",  # 30 second statement timeout
                    },
                )
                # Don't preload schemas here to avoid connection exhaustion
                logger.info("✅ PostgreSQL connection pool created: %s", self.postgres_config)
            except Exception as e:
                logger.error("❌ Failed to create PostgreSQL pool: %s", e)
                raise

    async def ensure_schemas_loaded(self, schema_name: str, rls_user_id: str) -> None:
        """Ensure schemas are loaded for the specified schema, loading them if not already cached."""
        if self.all_schemas is None:
            self.all_schemas = await self.get_all_schemas(schema_name, rls_user_id=rls_user_id)

    async def close_pool(self) -> None:
        """Close connection pool and cleanup."""
        if self.connection_pool:
            await self.connection_pool.close()
            self.connection_pool = None
            self.all_schemas = None
            self._schema_cache = {}
            logger.info("✅ PostgreSQL connection pool closed")

    async def get_connection(self) -> asyncpg.Connection:
        """Get a connection from pool."""
        if not self.connection_pool:
            raise RuntimeError("No database connection pool available. Call create_pool() first.")

        try:
            return await self.connection_pool.acquire()
        except Exception as e:
            logger.error("Failed to acquire connection from pool: %s", e)
            raise RuntimeError(f"Connection pool exhausted or unavailable: {e}") from e

    async def release_connection(self, conn: asyncpg.Connection) -> None:
        """Release connection back to pool."""
        if self.connection_pool:
            await self.connection_pool.release(conn)

    def _parse_table_name(self, table: str) -> tuple[str, str]:
        """Parse table name and return (schema, table_name) tuple. Always assumes table is fully qualified with schema.table format."""
        if "." not in table:
            raise ValueError(f"Table name '{table}' must be in 'schema.table' format (e.g., 'retail.customers')")

        parts = table.split(".", 1)
        if len(parts) != 2:
            raise ValueError(f"Table name '{table}' must be in 'schema.table' format (e.g., 'retail.customers')")

        schema, table_name = parts
        if not schema or not table_name:
            raise ValueError(f"Table name '{table}' must be in 'schema.table' format (e.g., 'retail.customers')")

        return schema, table_name

    def _get_qualified_table_name(self, table: str) -> str:
        """Get fully qualified table name with schema. Expects input to be already qualified."""
        if "." not in table:
            raise ValueError(f"Table name '{table}' must be in 'schema.table' format (e.g., 'retail.customers')")

        # Validate the format is correct
        schema, table_name = self._parse_table_name(table)
        return table

    async def table_exists(self, table: str) -> bool:
        """Check if a table exists in the specified schema."""
        conn = None
        try:
            conn = await self.get_connection()
            schema_name, table_name = self._parse_table_name(table)
            result = await conn.fetchval(
                """SELECT EXISTS (
                    SELECT 1 FROM information_schema.tables 
                    WHERE table_schema = $1 AND table_name = $2
                )""",
                schema_name,
                table_name,
            )
            return bool(result) if result is not None else False
        except Exception:
            return False
        finally:
            if conn:
                await self.release_connection(conn)

    async def column_exists(self, table: str, column: str) -> bool:
        """Check if a column exists in the given table."""
        conn = None
        try:
            conn = await self.get_connection()
            schema_name, table_name = self._parse_table_name(table)
            result = await conn.fetchval(
                """SELECT EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_schema = $1 AND table_name = $2 AND column_name = $3
                )""",
                schema_name,
                table_name,
                column,
            )
            return bool(result) if result is not None else False
        except Exception:
            return False
        finally:
            if conn:
                await self.release_connection(conn)

    async def fetch_distinct_values(self, column: str, table: str) -> List[str]:
        """Return sorted list of distinct values for a given column in a table, after validation."""
        schema_name, table_name = self._parse_table_name(table)
        if not await self.table_exists(table):
            raise ValueError(f"Table '{table}' does not exist")
        if not await self.column_exists(table, column):
            raise ValueError(f"Column '{column}' does not exist in table '{table}'")

        conn = None
        try:
            conn = await self.get_connection()
            qualified_table = self._get_qualified_table_name(table)
            rows = await conn.fetch(
                f"SELECT DISTINCT {column} FROM {qualified_table} WHERE {column} IS NOT NULL ORDER BY {column}"
            )
            return [row[0] for row in rows if row[0]]
        finally:
            if conn:
                await self.release_connection(conn)

    def infer_relationship_type(self, references_table: str) -> str:
        """Infer a relationship type based on the referenced table."""
        # Extract just the table name without schema for comparison
        try:
            _, table_name = self._parse_table_name(references_table)
        except ValueError:
            # If not in schema.table format, use as-is for comparison
            table_name = references_table

        return (
            "many_to_one"
            if table_name
            in {CUSTOMERS_TABLE, PRODUCTS_TABLE, STORES_TABLE, CATEGORIES_TABLE, PRODUCT_TYPES_TABLE, ORDERS_TABLE}
            else "one_to_many"
        )

    async def get_table_schema(self, table_name: str, rls_user_id: str) -> Dict[str, Any]:
        """Return schema information for a given table."""
        # Return cached version if available
        if table_name in self._schema_cache:
            return self._schema_cache[table_name]

        schema_name, parsed_table_name = self._parse_table_name(table_name)

        if not await self.table_exists(table_name):
            return {"error": f"Table '{table_name}' not found"}

        conn = None
        try:
            conn = await self.get_connection()

            await conn.execute("SELECT set_config('app.current_rls_user_id', $1, false)", rls_user_id)

            # Get column information
            columns = await conn.fetch(
                """SELECT 
                    column_name,
                    data_type,
                    is_nullable,
                    column_default,
                    ordinal_position
                FROM information_schema.columns 
                WHERE table_schema = $1 AND table_name = $2
                ORDER BY ordinal_position""",
                schema_name,
                parsed_table_name,
            )

            # Get primary key information
            primary_keys = await conn.fetch(
                """SELECT kcu.column_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu 
                    ON tc.constraint_name = kcu.constraint_name
                    AND tc.table_schema = kcu.table_schema
                WHERE tc.constraint_type = 'PRIMARY KEY'
                    AND tc.table_schema = $1 
                    AND tc.table_name = $2""",
                schema_name,
                parsed_table_name,
            )

            pk_columns = {row["column_name"] for row in primary_keys}

            # Get foreign key information
            foreign_keys = await conn.fetch(
                """SELECT 
                    kcu.column_name,
                    ccu.table_name AS foreign_table_name,
                    ccu.column_name AS foreign_column_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu 
                    ON tc.constraint_name = kcu.constraint_name
                    AND tc.table_schema = kcu.table_schema
                JOIN information_schema.constraint_column_usage ccu 
                    ON ccu.constraint_name = tc.constraint_name
                    AND ccu.table_schema = tc.table_schema
                WHERE tc.constraint_type = 'FOREIGN KEY'
                    AND tc.table_schema = $1 
                    AND tc.table_name = $2""",
                schema_name,
                parsed_table_name,
            )

            columns_format = ", ".join(f"{col['column_name']}:{col['data_type']}" for col in columns)
            lower_table = parsed_table_name.lower()

            # Define enum queries for each table to get unique values
            enum_queries = {
                STORES_TABLE: {"available_stores": ("store_name", f"{schema_name}.{STORES_TABLE}")},
                CATEGORIES_TABLE: {"available_categories": ("category_name", f"{schema_name}.{CATEGORIES_TABLE}")},
                PRODUCT_TYPES_TABLE: {"available_product_types": ("type_name", f"{schema_name}.{PRODUCT_TYPES_TABLE}")},
                PRODUCTS_TABLE: {
                    # Removed available_product_names to avoid lengthy output
                },
                ORDERS_TABLE: {
                    "available_years": ("EXTRACT(YEAR FROM order_date)::text", f"{schema_name}.{ORDERS_TABLE}")
                },
                ORDER_ITEMS_TABLE: {
                    # "price_range": ("unit_price", f"{schema_name}.{ORDER_ITEMS_TABLE}")
                },
            }

            enum_data = {}
            if lower_table in enum_queries:
                for key, (column, qualified_table) in enum_queries[lower_table].items():
                    try:
                        if key == "price_range":
                            # For price range, get min and max values
                            result = await conn.fetchrow(
                                f"SELECT MIN({column}) as min_price, MAX({column}) as max_price FROM {qualified_table}"
                            )
                            if result and result["min_price"] is not None:
                                enum_data[key] = f"${result['min_price']:.2f} - ${result['max_price']:.2f}"
                        elif key == "available_years":
                            # Handle years specially
                            rows = await conn.fetch(
                                f"SELECT DISTINCT {column} as year FROM {qualified_table} WHERE order_date IS NOT NULL ORDER BY year"
                            )
                            years = [str(row["year"]) for row in rows if row["year"]]
                            enum_data[key] = years
                        else:
                            enum_data[key] = await self.fetch_distinct_values(column, qualified_table)
                    except Exception as e:
                        logger.debug(f"Failed to fetch {key} for {qualified_table}: {e}")
                        enum_data[key] = []

            schema_data = {
                # Keep the original input (may include schema)
                "table_name": table_name,
                "parsed_table_name": parsed_table_name,  # Just the table name
                "schema_name": schema_name,  # The schema name
                "description": f"Table containing {parsed_table_name} data",
                "columns_format": columns_format,
                "columns": [
                    {
                        "name": col["column_name"],
                        "type": col["data_type"],
                        "primary_key": col["column_name"] in pk_columns,
                        "required": col["is_nullable"] == "NO",
                        "default_value": col["column_default"],
                    }
                    for col in columns
                ],
                "foreign_keys": [
                    {
                        "column": fk["column_name"],
                        "references_table": fk["foreign_table_name"],
                        "references_column": fk["foreign_column_name"],
                        "description": f"{fk['column_name']} links to {fk['foreign_table_name']}.{fk['foreign_column_name']}",
                        "relationship_type": self.infer_relationship_type(f"{schema_name}.{fk['foreign_table_name']}"),
                    }
                    for fk in foreign_keys
                ],
            }

            schema_data.update(enum_data)
            # Cache result for future calls
            self._schema_cache[table_name] = schema_data
            return schema_data

        finally:
            if conn:
                await self.release_connection(conn)

    async def get_all_table_names(self, schema_name: str) -> List[str]:
        """Get all user-defined table names in the specified schema."""
        conn = None
        try:
            conn = await self.get_connection()
            rows = await conn.fetch(
                """SELECT table_name FROM information_schema.tables 
                   WHERE table_schema = $1 AND table_type = 'BASE TABLE'
                   ORDER BY table_name""",
                schema_name,
            )
            return [row["table_name"] for row in rows]
        except Exception:
            return []
        finally:
            if conn:
                await self.release_connection(conn)

    async def get_all_schemas(self, schema_name: str, rls_user_id: str) -> Dict[str, Dict[str, Any]]:
        """Get schema metadata for all tables in the specified schema."""
        table_names = await self.get_all_table_names(schema_name)
        result = {}
        for table_name in table_names:
            # Store schema with qualified name using the specified schema
            qualified_name = f"{schema_name}.{table_name}"
            schema_data = await self.get_table_schema(qualified_name, rls_user_id=rls_user_id)
            # Cache by table name only for lookup
            result[table_name] = schema_data
        return result

    def format_schema_metadata_for_ai(self, schema: Dict[str, Any]) -> str:
        """Format schema data into an AI-readable format."""
        if "error" in schema:
            return f"**ERROR:** {schema['error']}"

        # Always use the full schema.table format for display
        # Should already be schema.table format
        table_display = schema.get("table_name")

        # Extract just table name for description
        try:
            _, table_name_only = self._parse_table_name(table_display) if table_display else ("", "unknown")
            table_description = table_name_only.replace("_", " ")
        except ValueError:
            table_description = table_display.replace("_", " ") if table_display else "unknown"

        lines = [f"# Table: {table_display}", ""]
        lines.append(f"**Purpose:** {schema.get('description', 'No description available')}")
        lines.append("\n## Schema")
        lines.append(schema.get("columns_format", "N/A"))

        if schema.get("foreign_keys"):
            lines.append("\n## Relationships")
            for fk in schema["foreign_keys"]:
                # Use the schema from the current table being processed
                current_schema = schema.get("schema_name")
                if current_schema:
                    fk_table_ref = f"{current_schema}.{fk['references_table']}"
                else:
                    # Fallback to just the table name if no schema available
                    fk_table_ref = fk["references_table"]
                lines.append(
                    f"- `{fk['column']}` → `{fk_table_ref}.{fk['references_column']}` ({fk['relationship_type'].upper()})"
                )

        enum_fields = [
            ("available_stores", "Stores Locations"),
            ("available_categories", "Valid Categories"),
            ("available_product_types", "Valid Product Types"),
            ("available_years", "Available Years"),
            ("price_range", "Price Range"),
        ]

        enum_lines = []
        for field_key, label in enum_fields:
            if schema.get(field_key):
                values = schema[field_key]
                # Always show the full list, no truncation
                enum_lines.append(f"**{label}:** {', '.join(values) if isinstance(values, list) else values}")

        if enum_lines:
            lines.append("\n## Valid Values")
            lines.extend(enum_lines)

        lines.append("\n## Query Hints")
        lines.append(f"- Use `{table_display}` for queries about {table_description}")
        if schema.get("foreign_keys"):
            for fk in schema["foreign_keys"]:
                # Use the schema from the current table being processed
                current_schema = schema.get("schema_name")
                if current_schema:
                    fk_table_ref = f"{current_schema}.{fk['references_table']}"
                else:
                    # Fallback to just the table name if no schema available
                    fk_table_ref = fk["references_table"]
                lines.append(f"- Join with `{fk_table_ref}` using `{fk['column']}`")

        return "\n".join(lines) + "\n"

    async def get_table_metadata_string(self, table_name: str, rls_user_id: str) -> str:
        """Return formatted schema metadata string for a single table."""
        # Always get fresh schema data for the specific table
        # This ensures we use the schema from the FQN rather than relying on cached data
        schema = await self.get_table_schema(table_name, rls_user_id=rls_user_id)
        return self.format_schema_metadata_for_ai(schema)

    async def get_table_metadata_from_list(self, table_names: List[str], rls_user_id: str) -> str:
        """Return formatted schema metadata strings for multiple tables efficiently using a single connection."""
        if not table_names:
            return "Error: table_names parameter is required and cannot be empty"

        conn = None
        try:
            conn = await self.get_connection()

            # Set rls_user_id once for the connection
            await conn.execute("SELECT set_config('app.current_rls_user_id', $1, false)", rls_user_id)

            schemas = []
            for table_name in table_names:
                try:
                    # Check if table exists first
                    schema_name, parsed_table_name = self._parse_table_name(table_name)
                    table_exists_result = await conn.fetchval(
                        """SELECT EXISTS (
                            SELECT 1 FROM information_schema.tables 
                            WHERE table_schema = $1 AND table_name = $2
                        )""",
                        schema_name,
                        parsed_table_name,
                    )

                    if not table_exists_result:
                        schemas.append(f"**ERROR:** Table '{table_name}' not found\n")
                        continue

                    # Get schema data efficiently within the same connection
                    # Use the original method but with our existing connection
                    schema_data = await self._get_table_metadata(conn, table_name)
                    formatted_schema = self.format_schema_metadata_for_ai(schema_data)
                    schemas.append(f"\n\n{formatted_schema}")

                except Exception as e:
                    schemas.append(f"Error retrieving {table_name} schema: {e!s}\n")

            return "".join(schemas)

        finally:
            if conn:
                await self.release_connection(conn)

    async def _get_table_metadata(self, conn: asyncpg.Connection, table_name: str) -> Dict[str, Any]:
        """Get table schema using an existing connection for efficiency."""
        # Return cached version if available
        if table_name in self._schema_cache:
            return self._schema_cache[table_name]

        schema_name, parsed_table_name = self._parse_table_name(table_name)

        # Get column information
        columns = await conn.fetch(
            """SELECT 
                column_name,
                data_type,
                is_nullable,
                column_default,
                ordinal_position
            FROM information_schema.columns 
            WHERE table_schema = $1 AND table_name = $2
            ORDER BY ordinal_position""",
            schema_name,
            parsed_table_name,
        )

        # Get primary key information
        primary_keys = await conn.fetch(
            """SELECT kcu.column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu 
                ON tc.constraint_name = kcu.constraint_name
                AND tc.table_schema = kcu.table_schema
            WHERE tc.constraint_type = 'PRIMARY KEY'
                AND tc.table_schema = $1 
                AND tc.table_name = $2""",
            schema_name,
            parsed_table_name,
        )

        pk_columns = {row["column_name"] for row in primary_keys}

        # Get foreign key information
        foreign_keys = await conn.fetch(
            """SELECT 
                kcu.column_name,
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu 
                ON tc.constraint_name = kcu.constraint_name
                AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage ccu 
                ON ccu.constraint_name = tc.constraint_name
                AND ccu.table_schema = tc.table_schema
            WHERE tc.constraint_type = 'FOREIGN KEY'
                AND tc.table_schema = $1 
                AND tc.table_name = $2""",
            schema_name,
            parsed_table_name,
        )

        columns_format = ", ".join(f"{col['column_name']}:{col['data_type']}" for col in columns)
        lower_table = parsed_table_name.lower()

        # Define enum queries for each table to get unique values
        enum_queries = {
            STORES_TABLE: {"available_stores": ("store_name", f"{schema_name}.{STORES_TABLE}")},
            CATEGORIES_TABLE: {"available_categories": ("category_name", f"{schema_name}.{CATEGORIES_TABLE}")},
            PRODUCT_TYPES_TABLE: {"available_product_types": ("type_name", f"{schema_name}.{PRODUCT_TYPES_TABLE}")},
            PRODUCTS_TABLE: {
                # Removed available_product_names to avoid lengthy output
            },
            ORDERS_TABLE: {"available_years": ("EXTRACT(YEAR FROM order_date)::text", f"{schema_name}.{ORDERS_TABLE}")},
            ORDER_ITEMS_TABLE: {
                # "price_range": ("unit_price", f"{schema_name}.{ORDER_ITEMS_TABLE}")
            },
        }

        enum_data = {}
        if lower_table in enum_queries:
            for key, (column, qualified_table) in enum_queries[lower_table].items():
                try:
                    if key == "available_years":
                        # Handle years specially
                        rows = await conn.fetch(
                            f"SELECT DISTINCT {column} as year FROM {qualified_table} WHERE order_date IS NOT NULL ORDER BY year"
                        )
                        years = [str(row["year"]) for row in rows if row["year"]]
                        enum_data[key] = years
                    else:
                        # Use existing connection for fetch_distinct_values-like operation
                        rows = await conn.fetch(
                            f"SELECT DISTINCT {column} FROM {qualified_table} WHERE {column} IS NOT NULL ORDER BY {column}"
                        )
                        enum_data[key] = [row[0] for row in rows if row[0]]
                except Exception as e:
                    logger.debug(f"Failed to fetch {key} for {qualified_table}: {e}")
                    enum_data[key] = []

        schema_data = {
            # Keep the original input (may include schema)
            "table_name": table_name,
            "parsed_table_name": parsed_table_name,  # Just the table name
            "schema_name": schema_name,  # The schema name
            "description": f"Table containing {parsed_table_name} data",
            "columns_format": columns_format,
            "columns": [
                {
                    "name": col["column_name"],
                    "type": col["data_type"],
                    "primary_key": col["column_name"] in pk_columns,
                    "required": col["is_nullable"] == "NO",
                    "default_value": col["column_default"],
                }
                for col in columns
            ],
            "foreign_keys": [
                {
                    "column": fk["column_name"],
                    "references_table": fk["foreign_table_name"],
                    "references_column": fk["foreign_column_name"],
                    "description": f"{fk['column_name']} links to {fk['foreign_table_name']}.{fk['foreign_column_name']}",
                    "relationship_type": self.infer_relationship_type(f"{schema_name}.{fk['foreign_table_name']}"),
                }
                for fk in foreign_keys
            ],
        }

        schema_data.update(enum_data)
        # Cache result for future calls
        self._schema_cache[table_name] = schema_data
        return schema_data

    async def execute_query(self, sql_query: str, rls_user_id: str) -> str:
        """Execute a SQL query and return results in compact JSON.

        Compact success shape:
          {"c":["col1","col2"],"r":[[v11,v12],[v21,v22]],"n":2}
        Empty result adds 'msg':
          {"c":[],"r":[],"n":0,"msg":"No rows"}
        Error shape:
          {"err":"...","q":"SELECT ...","c":[],"r":[],"n":0}
        """
        conn: Optional[asyncpg.Connection] = None
        try:
            conn = await self.get_connection()
            await conn.execute("SELECT set_config('app.current_rls_user_id', $1, false)", rls_user_id)

            rows = await conn.fetch(sql_query)
            if not rows:
                return json.dumps(
                    {"c": [], "r": [], "n": 0, "msg": "No rows"},
                    separators=(",", ":"),
                    default=str,
                )

            columns = list(rows[0].keys())
            data_rows = [[row[col] for col in columns] for row in rows]
            return json.dumps(
                {"c": columns, "r": data_rows, "n": len(data_rows)},
                separators=(",", ":"),
                default=str,
            )
        except Exception as e:
            return json.dumps(
                {"err": f"PostgreSQL query failed: {e!s}", "q": sql_query, "c": [], "r": [], "n": 0},
                separators=(",", ":"),
                default=str,
            )
        finally:
            if conn:
                await self.release_connection(conn)

    async def search_products_by_similarity(
        self, query_embedding: list[float], rls_user_id: str, max_rows: int = 20, similarity_threshold: float = 30.0
    ) -> str:
        """Search for products by similarity using pgvector cosine similarity.

        Args:
            query_embedding: The embedding vector to search for similar products
            max_rows: Maximum number of rows to return
            rls_user_id: Row-level security user ID
            similarity_threshold: Minimum similarity percentage (0-100) to include in results. Default is 50%.
        """
        conn = None
        try:
            max_rows = min(max_rows, 100)  # Limit to 100 for performance

            # Convert similarity percentage threshold to distance threshold
            # Similarity percentage = (1 - distance) * 100
            # So distance = 1 - (similarity_percentage / 100)
            distance_threshold = 1.0 - (similarity_threshold / 100.0)

            conn = await self.get_connection()

            await conn.execute("SELECT set_config('app.current_rls_user_id', $1, false)", rls_user_id)

            # Convert embedding to string format for PostgreSQL
            embedding_str = "[" + ",".join(map(str, query_embedding)) + "]"

            query = f"""
                SELECT 
                    p.*,
                    (pde.description_embedding <=> $1::vector) as similarity_distance
                FROM {SCHEMA_NAME}.product_description_embeddings pde
                JOIN {SCHEMA_NAME}.products p ON pde.product_id = p.product_id
                WHERE (pde.description_embedding <=> $1::vector) <= $3
                ORDER BY similarity_distance
                LIMIT $2
            """

            rows = await conn.fetch(query, embedding_str, max_rows, distance_threshold)

            if not rows:
                return json.dumps(
                    {"c": [], "r": [], "n": 0, "msg": f"No products >= {similarity_threshold}%"},
                    separators=(",", ":"),
                    default=str,
                )

            # Prepare compact columnar data including similarity percent
            base_columns = list(rows[0].keys())  # includes similarity_distance
            # We'll append 'sp' (similarity percent) short key instead of longer name
            columns = [*base_columns, "sp"]
            data_rows = []
            for row in rows:
                similarity_distance = row.get("similarity_distance", 1.0)
                similarity_percent = max(0, (1 - similarity_distance) * 100)
                row_values = [row[col] for col in base_columns]
                row_values.append(round(similarity_percent, 1))
                data_rows.append(row_values)

            return json.dumps({"c": columns, "r": data_rows, "n": len(data_rows)}, separators=(",", ":"), default=str)

        except Exception as e:
            return json.dumps(
                {"err": f"PostgreSQL semantic search failed: {e!s}", "c": [], "r": [], "n": 0},
                separators=(",", ":"),
                default=str,
            )
        finally:
            if conn:
                await self.release_connection(conn)


async def test_connection() -> bool:
    """Test PostgreSQL connection and return success status."""
    try:
        # Create a temporary pool for testing
        pool = await asyncpg.create_pool(POSTGRES_URL, min_size=1, max_size=1)
        conn = await pool.acquire()
        await pool.release(conn)
        await pool.close()
        return True
    except Exception as e:
        logger.error(f"Connection test failed: {e}")
        return False


async def main() -> None:
    """Main function to run the schema tool."""
    logger.info("🤖 AI-Friendly PostgreSQL Database Schema Tool")
    logger.info("=" * 50)

    # Test connection first
    if not await test_connection():
        logger.error("❌ Error: Cannot connect to PostgreSQL using: %s", POSTGRES_URL)
        logger.error("   Please verify:")
        logger.error("   1. PostgreSQL is running")
        logger.error("   2. Database 'zava' exists")
        logger.error("   3. POSTGRES_URL environment variable is correct")
        logger.error("   4. User has access to the retail schema")
        return

    try:
        async with PostgreSQLSchemaProvider() as provider:
            # Create connection pool (schemas will be loaded lazily when needed)
            await provider.create_pool()

            # Preload schemas for testing
            await provider.ensure_schemas_loaded(SCHEMA_NAME, rls_user_id=MANAGER_ID)

            logger.info("📋 Getting all table schemas from %s schema...", SCHEMA_NAME)
            if not provider.all_schemas:
                logger.warning("❌ No schemas available in %s schema", SCHEMA_NAME)
                logger.warning("Please run the PostgreSQL database generator first:")
                logger.warning("python shared/data/database/generate_zava_postgres.py")
                return

            logger.info("🧪 Testing SQL Query Execution:")
            logger.info("=" * 50)

            logger.info("📊 Test 1: Count all customers")
            result = await provider.execute_query(
                f"SELECT COUNT(*) as total_customers FROM {SCHEMA_NAME}.customers", rls_user_id=MANAGER_ID
            )
            logger.info("Result: %s", result)

            logger.info("📊 Test 2: Count stores")
            result = await provider.execute_query(
                f"SELECT COUNT(*) as total_stores FROM {SCHEMA_NAME}.stores", rls_user_id=MANAGER_ID
            )
            logger.info("Result: %s", result)

            logger.info("📊 Test 3: Count categories and types")
            result = await provider.execute_query(
                f"SELECT COUNT(*) as total_categories FROM {SCHEMA_NAME}.categories", rls_user_id=MANAGER_ID
            )
            logger.info("Result: %s", result)

            logger.info("📊 Test 4: Orders with revenue")
            result = await provider.execute_query(
                f"""SELECT COUNT(DISTINCT o.order_id) as orders, 
                    SUM(oi.total_amount) as revenue 
                    FROM {SCHEMA_NAME}.orders o 
                    JOIN {SCHEMA_NAME}.order_items oi ON o.order_id = oi.order_id 
                    LIMIT 1""",
                rls_user_id=MANAGER_ID,
            )
            logger.info("Result: %s", result)

            logger.info("✅ SQL Query tests completed!")
            logger.info("=" * 50)
            logger.info("📋 All table schemas in %s schema:\n", SCHEMA_NAME)

            # --- Use the new efficient method for getting all schemas ---
            all_table_names = [
                f"{SCHEMA_NAME}.{STORES_TABLE}",
                f"{SCHEMA_NAME}.{CATEGORIES_TABLE}",
                f"{SCHEMA_NAME}.{PRODUCT_TYPES_TABLE}",
                f"{SCHEMA_NAME}.{PRODUCTS_TABLE}",
                f"{SCHEMA_NAME}.{CUSTOMERS_TABLE}",
                f"{SCHEMA_NAME}.{ORDERS_TABLE}",
                f"{SCHEMA_NAME}.{ORDER_ITEMS_TABLE}",
                f"{SCHEMA_NAME}.{INVENTORY_TABLE}",
            ]
            logger.info(
                "Database schema info: %s",
                await provider.get_table_metadata_from_list(all_table_names, rls_user_id=MANAGER_ID),
            )

    except Exception as e:
        logger.error("❌ Error during analysis: %s", e)
        raise


if __name__ == "__main__":
    asyncio.run(main())
