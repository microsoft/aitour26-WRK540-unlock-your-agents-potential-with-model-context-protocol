"""
Customer Sales Database Generator for PostgreSQL with pgvector

This script generates a comprehensive customer sales database with optimized indexing
and vector embeddings support for PostgreSQL with pgvector extension.

DATA FILE STRUCTURE:
- product_data.json: Contains all product information (main_categories with products)
- reference_data.json: Contains store configurations (weights, year weights)

POSTGRESQL CONNECTION:
- Requires PostgreSQL with pgvector extension enabled
- Uses async connections via asyncpg
- Targets retail schema in zava database

FEATURES:
- Complete database generation with customers, products, stores, orders
- Product image embeddings population from product_data.json
- Product description embeddings population from product_data.json
- Vector similarity indexing with pgvector
- Performance-optimized indexes
- Comprehensive statistics and verification

USAGE:
    python generate_zava_postgres.py                     # Generate complete database
    python generate_zava_postgres.py --show-stats        # Show database statistics
    python generate_zava_postgres.py --embeddings-only   # Populate embeddings only
    python generate_zava_postgres.py --verify-embeddings # Verify embeddings table
    python generate_zava_postgres.py --help              # Show all options
"""

import argparse
import asyncio
import json
import logging
import os
import random
import sys
from datetime import date
from typing import Dict, List, Optional, Tuple

import asyncpg
from dotenv import load_dotenv
from faker import Faker

# Load environment variables
script_dir = os.path.dirname(os.path.abspath(__file__))
# Try to load .env from script directory first, then parent directories
env_paths = [
    os.path.join(script_dir, '.env'),
    os.path.join(script_dir, '..', '..', '..', '.env'),  # Up to workspace root
]

for env_path in env_paths:
    if os.path.exists(env_path):
        load_dotenv(env_path)
        break
else:
    # Fallback to default behavior
    load_dotenv()

# Initialize Faker and logging
fake = Faker()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# PostgreSQL connection configuration
POSTGRES_CONFIG = {
    'host': 'db',
    'port': 5432,
    'user': 'postgres',
    'password': 'P@ssw0rd!',
    'database': 'zava'
}

SCHEMA_NAME = 'retail'

# Super Manager UUID - has access to all rows regardless of RLS policies
SUPER_MANAGER_UUID = '00000000-0000-0000-0000-000000000000'

# Load reference data from JSON file
def load_reference_data():
    """Load reference data from JSON file"""
    try:
        json_path = os.path.join(os.path.dirname(__file__), 'reference_data.json')
        with open(json_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Failed to load reference data: {e}")
        raise

def load_product_data():
    """Load product data from JSON file"""
    try:
        json_path = os.path.join(os.path.dirname(__file__), 'product_data.json')
        with open(json_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Failed to load product data: {e}")
        raise

# Load the reference data
reference_data = load_reference_data()
product_data = load_product_data()

# Get reference data from loaded JSON
main_categories = product_data['main_categories']
stores = reference_data['stores']

# Check if seasonal trends are available
seasonal_categories = []
for category_name, category_data in main_categories.items():
    if 'washington_seasonal_multipliers' in category_data:
        seasonal_categories.append(category_name)

if seasonal_categories:
    logging.info(f"🗓️  Washington State seasonal trends active for {len(seasonal_categories)} categories: {', '.join(seasonal_categories)}")
else:
    logging.info("⚠️  No seasonal trends found - using equal weights for all categories")

def weighted_store_choice():
    """Choose a store based on weighted distribution"""
    store_names = list(stores.keys())
    weights = [stores[store]['customer_distribution_weight'] for store in store_names]
    return random.choices(store_names, weights=weights, k=1)[0]

def generate_phone_number(region=None):
    """Generate a phone number in North American format (XXX) XXX-XXXX"""
    return f"({random.randint(200, 999)}) {random.randint(200, 999)}-{random.randint(1000, 9999)}"

async def create_connection():
    """Create async PostgreSQL connection"""
    try:
        conn = await asyncpg.connect(**POSTGRES_CONFIG)
        logging.info(f"Connected to PostgreSQL at {POSTGRES_CONFIG['host']}:{POSTGRES_CONFIG['port']}")
        return conn
    except Exception as e:
        logging.error(f"Failed to connect to PostgreSQL: {e}")
        raise

async def create_database_schema(conn):
    """Create database schema, tables and indexes"""
    try:
        # Create schema if it doesn't exist
        await conn.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA_NAME}")
        logging.info(f"Schema '{SCHEMA_NAME}' created or already exists")
        
        # Enable pgvector extension if available
        try:
            await conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
            logging.info("pgvector extension enabled")
        except Exception as e:
            logging.warning(f"pgvector extension not available: {e}")
        
        # Create stores table
        await conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {SCHEMA_NAME}.stores (
                store_id SERIAL PRIMARY KEY,
                store_name TEXT UNIQUE NOT NULL,
                rls_user_id UUID NOT NULL,
                is_online BOOLEAN NOT NULL DEFAULT false
            )
        """)
        
        # Create customers table
        await conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {SCHEMA_NAME}.customers (
                customer_id SERIAL PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                primary_store_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (primary_store_id) REFERENCES {SCHEMA_NAME}.stores (store_id)
            )
        """)
        
        # Create categories table
        await conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {SCHEMA_NAME}.categories (
                category_id SERIAL PRIMARY KEY,
                category_name TEXT NOT NULL UNIQUE
            )
        """)
        
        # Create product_types table
        await conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {SCHEMA_NAME}.product_types (
                type_id SERIAL PRIMARY KEY,
                category_id INTEGER NOT NULL,
                type_name TEXT NOT NULL,
                FOREIGN KEY (category_id) REFERENCES {SCHEMA_NAME}.categories (category_id)
            )
        """)
        
        # Create products table with cost and selling price for 33% gross margin
        await conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {SCHEMA_NAME}.products (
                product_id SERIAL PRIMARY KEY,
                sku TEXT UNIQUE NOT NULL,
                product_name TEXT NOT NULL,
                category_id INTEGER NOT NULL,
                type_id INTEGER NOT NULL,
                cost DECIMAL(10,2) NOT NULL,
                base_price DECIMAL(10,2) NOT NULL,
                gross_margin_percent DECIMAL(5,2) DEFAULT 33.00,
                product_description TEXT NOT NULL,
                FOREIGN KEY (category_id) REFERENCES {SCHEMA_NAME}.categories (category_id),
                FOREIGN KEY (type_id) REFERENCES {SCHEMA_NAME}.product_types (type_id)
            )
        """)
        
        # Create inventory table
        await conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {SCHEMA_NAME}.inventory (
                store_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                stock_level INTEGER NOT NULL,
                PRIMARY KEY (store_id, product_id),
                FOREIGN KEY (store_id) REFERENCES {SCHEMA_NAME}.stores (store_id),
                FOREIGN KEY (product_id) REFERENCES {SCHEMA_NAME}.products (product_id)
            )
        """)
        
        # Create orders table (header only)
        await conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {SCHEMA_NAME}.orders (
                order_id SERIAL PRIMARY KEY,
                customer_id INTEGER NOT NULL,
                store_id INTEGER NOT NULL,
                order_date DATE NOT NULL,
                FOREIGN KEY (customer_id) REFERENCES {SCHEMA_NAME}.customers (customer_id),
                FOREIGN KEY (store_id) REFERENCES {SCHEMA_NAME}.stores (store_id)
            )
        """)
        
        # Create order_items table (line items)
        await conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {SCHEMA_NAME}.order_items (
                order_item_id SERIAL PRIMARY KEY,
                order_id INTEGER NOT NULL,
                store_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price DECIMAL(10,2) NOT NULL,
                discount_percent INTEGER DEFAULT 0,
                discount_amount DECIMAL(10,2) DEFAULT 0,
                total_amount DECIMAL(10,2) NOT NULL,
                FOREIGN KEY (order_id) REFERENCES {SCHEMA_NAME}.orders (order_id),
                FOREIGN KEY (store_id) REFERENCES {SCHEMA_NAME}.stores (store_id),
                FOREIGN KEY (product_id) REFERENCES {SCHEMA_NAME}.products (product_id)
            )
        """)
        
        # Create product_image_embeddings table for image data
        await conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {SCHEMA_NAME}.product_image_embeddings (
                product_id INTEGER PRIMARY KEY,
                image_url TEXT NOT NULL,
                image_embedding vector(512),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES {SCHEMA_NAME}.products (product_id)
            )
        """)
        
        # Create product_description_embeddings table for text embeddings
        await conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {SCHEMA_NAME}.product_description_embeddings (
                product_id INTEGER PRIMARY KEY,
                description_embedding vector(1536),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES {SCHEMA_NAME}.products (product_id)
            )
        """)
        
        # Create optimized performance indexes
        logging.info("Creating performance indexes...")
        
        # Category and type indexes
        await conn.execute(f"CREATE INDEX IF NOT EXISTS idx_categories_name ON {SCHEMA_NAME}.categories(category_name)")
        await conn.execute(f"CREATE INDEX IF NOT EXISTS idx_product_types_category ON {SCHEMA_NAME}.product_types(category_id)")
        await conn.execute(f"CREATE INDEX IF NOT EXISTS idx_product_types_name ON {SCHEMA_NAME}.product_types(type_name)")
        
        # Product indexes
        await conn.execute(f"CREATE INDEX IF NOT EXISTS idx_products_sku ON {SCHEMA_NAME}.products(sku)")
        await conn.execute(f"CREATE INDEX IF NOT EXISTS idx_products_category ON {SCHEMA_NAME}.products(category_id)")
        await conn.execute(f"CREATE INDEX IF NOT EXISTS idx_products_type ON {SCHEMA_NAME}.products(type_id)")
        await conn.execute(f"CREATE INDEX IF NOT EXISTS idx_products_price ON {SCHEMA_NAME}.products(base_price)")
        await conn.execute(f"CREATE INDEX IF NOT EXISTS idx_products_cost ON {SCHEMA_NAME}.products(cost)")
        await conn.execute(f"CREATE INDEX IF NOT EXISTS idx_products_margin ON {SCHEMA_NAME}.products(gross_margin_percent)")
        
        # Inventory indexes
        await conn.execute(f"CREATE INDEX IF NOT EXISTS idx_inventory_store_product ON {SCHEMA_NAME}.inventory(store_id, product_id)")
        await conn.execute(f"CREATE INDEX IF NOT EXISTS idx_inventory_product ON {SCHEMA_NAME}.inventory(product_id)")
        await conn.execute(f"CREATE INDEX IF NOT EXISTS idx_inventory_store ON {SCHEMA_NAME}.inventory(store_id)")
        
        # Store indexes
        await conn.execute(f"CREATE INDEX IF NOT EXISTS idx_stores_name ON {SCHEMA_NAME}.stores(store_name)")
        
        # Order indexes
        await conn.execute(f"CREATE INDEX IF NOT EXISTS idx_orders_customer ON {SCHEMA_NAME}.orders(customer_id)")
        await conn.execute(f"CREATE INDEX IF NOT EXISTS idx_orders_store ON {SCHEMA_NAME}.orders(store_id)")
        await conn.execute(f"CREATE INDEX IF NOT EXISTS idx_orders_date ON {SCHEMA_NAME}.orders(order_date)")
        await conn.execute(f"CREATE INDEX IF NOT EXISTS idx_orders_customer_date ON {SCHEMA_NAME}.orders(customer_id, order_date)")
        await conn.execute(f"CREATE INDEX IF NOT EXISTS idx_orders_store_date ON {SCHEMA_NAME}.orders(store_id, order_date)")
        
        # Order items indexes
        await conn.execute(f"CREATE INDEX IF NOT EXISTS idx_order_items_order ON {SCHEMA_NAME}.order_items(order_id)")
        await conn.execute(f"CREATE INDEX IF NOT EXISTS idx_order_items_store ON {SCHEMA_NAME}.order_items(store_id)")
        await conn.execute(f"CREATE INDEX IF NOT EXISTS idx_order_items_product ON {SCHEMA_NAME}.order_items(product_id)")
        await conn.execute(f"CREATE INDEX IF NOT EXISTS idx_order_items_total ON {SCHEMA_NAME}.order_items(total_amount)")
        
        # Product image embeddings indexes
        await conn.execute(f"CREATE INDEX IF NOT EXISTS idx_product_image_embeddings_product ON {SCHEMA_NAME}.product_image_embeddings(product_id)")
        await conn.execute(f"CREATE INDEX IF NOT EXISTS idx_product_image_embeddings_url ON {SCHEMA_NAME}.product_image_embeddings(image_url)")
        
        # Vector similarity index for product image embeddings (if pgvector is available)
        try:
            await conn.execute(f"CREATE INDEX IF NOT EXISTS idx_product_image_embeddings_vector ON {SCHEMA_NAME}.product_image_embeddings USING ivfflat (image_embedding vector_cosine_ops) WITH (lists = 100)")
            logging.info("Product image embeddings vector similarity index created")
        except Exception as e:
            logging.warning(f"Could not create product image embeddings vector index: {e}")
        
        # Vector similarity index for product description embeddings (if pgvector is available)
        try:
            await conn.execute(f"CREATE INDEX IF NOT EXISTS idx_product_description_embeddings_vector ON {SCHEMA_NAME}.product_description_embeddings USING ivfflat (description_embedding vector_cosine_ops) WITH (lists = 100)")
            logging.info("Product description embeddings vector similarity index created")
        except Exception as e:
            logging.warning(f"Could not create product description embeddings vector index: {e}")
        
        # Covering indexes for aggregation queries
        await conn.execute(f"CREATE INDEX IF NOT EXISTS idx_order_items_covering ON {SCHEMA_NAME}.order_items(order_id, store_id, product_id, total_amount, quantity)")
        await conn.execute(f"CREATE INDEX IF NOT EXISTS idx_products_covering ON {SCHEMA_NAME}.products(category_id, type_id, product_id, sku, cost, base_price)")
        await conn.execute(f"CREATE INDEX IF NOT EXISTS idx_products_sku_covering ON {SCHEMA_NAME}.products(sku, product_id, product_name, cost, base_price)")
        
        # Customer indexes
        await conn.execute(f"CREATE INDEX IF NOT EXISTS idx_customers_email ON {SCHEMA_NAME}.customers(email)")
        await conn.execute(f"CREATE INDEX IF NOT EXISTS idx_customers_primary_store ON {SCHEMA_NAME}.customers(primary_store_id)")
        
        logging.info("Performance indexes created successfully!")
        
        # Enable Row Level Security (RLS) and create policies
        # Note: All RLS policies include access for SUPER_MANAGER_UUID which bypasses all restrictions
        logging.info("Setting up Row Level Security policies...")
        logging.info(f"Super Manager UUID (access to all rows): {SUPER_MANAGER_UUID}")
        
        # Enable RLS on tables that should be restricted by store manager
        await conn.execute(f"ALTER TABLE {SCHEMA_NAME}.orders ENABLE ROW LEVEL SECURITY")
        await conn.execute(f"ALTER TABLE {SCHEMA_NAME}.order_items ENABLE ROW LEVEL SECURITY")
        await conn.execute(f"ALTER TABLE {SCHEMA_NAME}.inventory ENABLE ROW LEVEL SECURITY")
        await conn.execute(f"ALTER TABLE {SCHEMA_NAME}.customers ENABLE ROW LEVEL SECURITY")
        
        # Enable RLS on reference tables that store managers should have full access to
        # Note: These tables will have permissive policies allowing all authenticated users
        await conn.execute(f"ALTER TABLE {SCHEMA_NAME}.stores ENABLE ROW LEVEL SECURITY")
        await conn.execute(f"ALTER TABLE {SCHEMA_NAME}.categories ENABLE ROW LEVEL SECURITY") 
        await conn.execute(f"ALTER TABLE {SCHEMA_NAME}.product_types ENABLE ROW LEVEL SECURITY")
        await conn.execute(f"ALTER TABLE {SCHEMA_NAME}.products ENABLE ROW LEVEL SECURITY")
        await conn.execute(f"ALTER TABLE {SCHEMA_NAME}.product_image_embeddings ENABLE ROW LEVEL SECURITY")
        await conn.execute(f"ALTER TABLE {SCHEMA_NAME}.product_description_embeddings ENABLE ROW LEVEL SECURITY")
        
        # Create RLS policies for orders - store managers can only see orders from their store
        await conn.execute(f"DROP POLICY IF EXISTS store_manager_orders ON {SCHEMA_NAME}.orders")
        await conn.execute(f"""
            CREATE POLICY store_manager_orders ON {SCHEMA_NAME}.orders
            FOR ALL TO PUBLIC
            USING (
                -- Super manager has access to all rows
                current_setting('app.current_rls_user_id', true) = '{SUPER_MANAGER_UUID}'
                OR
                -- Store managers can only see orders from their store
                EXISTS (
                    SELECT 1 FROM {SCHEMA_NAME}.stores s 
                    WHERE s.store_id = {SCHEMA_NAME}.orders.store_id 
                    AND s.rls_user_id::text = current_setting('app.current_rls_user_id', true)
                )
            )
        """)
        
        # Create RLS policies for order_items - direct store access for better performance
        await conn.execute(f"DROP POLICY IF EXISTS store_manager_order_items ON {SCHEMA_NAME}.order_items")
        await conn.execute(f"""
            CREATE POLICY store_manager_order_items ON {SCHEMA_NAME}.order_items
            FOR ALL TO PUBLIC
            USING (
                -- Super manager has access to all rows
                current_setting('app.current_rls_user_id', true) = '{SUPER_MANAGER_UUID}'
                OR
                -- Store managers can only see order items from their store
                EXISTS (
                    SELECT 1 FROM {SCHEMA_NAME}.stores s 
                    WHERE s.store_id = {SCHEMA_NAME}.order_items.store_id 
                    AND s.rls_user_id::text = current_setting('app.current_rls_user_id', true)
                )
            )
        """)
        
        # Create RLS policies for inventory - store managers can only see their store's inventory
        await conn.execute(f"DROP POLICY IF EXISTS store_manager_inventory ON {SCHEMA_NAME}.inventory")
        await conn.execute(f"""
            CREATE POLICY store_manager_inventory ON {SCHEMA_NAME}.inventory
            FOR ALL TO PUBLIC
            USING (
                -- Super manager has access to all rows
                current_setting('app.current_rls_user_id', true) = '{SUPER_MANAGER_UUID}'
                OR
                -- Store managers can only see their store's inventory
                EXISTS (
                    SELECT 1 FROM {SCHEMA_NAME}.stores s 
                    WHERE s.store_id = {SCHEMA_NAME}.inventory.store_id 
                    AND s.rls_user_id::text = current_setting('app.current_rls_user_id', true)
                )
            )
        """)
        
        # For customers, they can only see customers assigned to their store
        await conn.execute(f"DROP POLICY IF EXISTS store_manager_customers ON {SCHEMA_NAME}.customers")
        await conn.execute(f"""
            CREATE POLICY store_manager_customers ON {SCHEMA_NAME}.customers
            FOR ALL TO PUBLIC
            USING (
                -- Super manager has access to all rows
                current_setting('app.current_rls_user_id', true) = '{SUPER_MANAGER_UUID}'
                OR
                -- Store managers can only see customers assigned to their store
                EXISTS (
                    SELECT 1 FROM {SCHEMA_NAME}.stores s 
                    WHERE s.store_id = {SCHEMA_NAME}.customers.primary_store_id 
                    AND s.rls_user_id::text = current_setting('app.current_rls_user_id', true)
                )
                OR
                -- Also allow access to customers who have ordered from their store (backward compatibility)
                EXISTS (
                    SELECT 1 FROM {SCHEMA_NAME}.orders o
                    JOIN {SCHEMA_NAME}.stores s ON o.store_id = s.store_id
                    WHERE o.customer_id = {SCHEMA_NAME}.customers.customer_id
                    AND s.rls_user_id::text = current_setting('app.current_rls_user_id', true)
                )
            )
        """)
        
        # Create permissive RLS policies for reference tables that all authenticated users should access
        
        # Stores table - managers can see all stores (needed for reference)
        await conn.execute(f"DROP POLICY IF EXISTS all_users_stores ON {SCHEMA_NAME}.stores")
        await conn.execute(f"""
            CREATE POLICY all_users_stores ON {SCHEMA_NAME}.stores
            FOR ALL TO PUBLIC
            USING (true)
        """)
        
        # Categories table - all users can see all categories
        await conn.execute(f"DROP POLICY IF EXISTS all_users_categories ON {SCHEMA_NAME}.categories")
        await conn.execute(f"""
            CREATE POLICY all_users_categories ON {SCHEMA_NAME}.categories
            FOR ALL TO PUBLIC
            USING (true)
        """)
        
        # Product types table - all users can see all product types
        await conn.execute(f"DROP POLICY IF EXISTS all_users_product_types ON {SCHEMA_NAME}.product_types")
        await conn.execute(f"""
            CREATE POLICY all_users_product_types ON {SCHEMA_NAME}.product_types
            FOR ALL TO PUBLIC
            USING (true)
        """)
        
        # Products table - all users can see all products
        await conn.execute(f"DROP POLICY IF EXISTS all_users_products ON {SCHEMA_NAME}.products")
        await conn.execute(f"""
            CREATE POLICY all_users_products ON {SCHEMA_NAME}.products
            FOR ALL TO PUBLIC
            USING (true)
        """)
        
        # Product image embeddings table - all users can see all product image embeddings
        await conn.execute(f"DROP POLICY IF EXISTS all_users_product_image_embeddings ON {SCHEMA_NAME}.product_image_embeddings")
        await conn.execute(f"""
            CREATE POLICY all_users_product_image_embeddings ON {SCHEMA_NAME}.product_image_embeddings
            FOR ALL TO PUBLIC
            USING (true)
        """)
        
        # Product description embeddings table - all users can see all product description embeddings
        await conn.execute(f"DROP POLICY IF EXISTS all_users_product_description_embeddings ON {SCHEMA_NAME}.product_description_embeddings")
        await conn.execute(f"""
            CREATE POLICY all_users_product_description_embeddings ON {SCHEMA_NAME}.product_description_embeddings
            FOR ALL TO PUBLIC
            USING (true)
        """)
        
        logging.info("Row Level Security policies created successfully!")
        
        # Grant permissions to store_manager role
        await setup_store_manager_permissions(conn)
        
        logging.info("Database schema created successfully!")
    except Exception as e:
        logging.error(f"Error creating database schema: {e}")
        raise

async def setup_store_manager_permissions(conn):
    """Setup permissions for store_manager user to access the retail schema and tables"""
    try:
        logging.info("Setting up store_manager permissions...")
        
        # Check if store_manager role exists, create if it doesn't
        role_exists = await conn.fetchval(
            "SELECT 1 FROM pg_roles WHERE rolname = 'store_manager'"
        )
        
        if not role_exists:
            await conn.execute("CREATE ROLE store_manager LOGIN")
            logging.info("Created store_manager role")
        else:
            logging.info("store_manager role already exists")
        
        # Grant usage on the retail schema
        await conn.execute(f"GRANT USAGE ON SCHEMA {SCHEMA_NAME} TO store_manager")
        
        # Grant SELECT permissions on all tables in the retail schema
        await conn.execute(f"GRANT SELECT ON ALL TABLES IN SCHEMA {SCHEMA_NAME} TO store_manager")
        
        # Grant permissions on sequences (for SERIAL columns)
        await conn.execute(f"GRANT USAGE ON ALL SEQUENCES IN SCHEMA {SCHEMA_NAME} TO store_manager")
        
        # Grant permissions for future tables (in case new tables are added)
        await conn.execute(f"ALTER DEFAULT PRIVILEGES IN SCHEMA {SCHEMA_NAME} GRANT SELECT ON TABLES TO store_manager")
        await conn.execute(f"ALTER DEFAULT PRIVILEGES IN SCHEMA {SCHEMA_NAME} GRANT USAGE ON SEQUENCES TO store_manager")
        
        # Do not grant INSERT, UPDATE, DELETE permissions to store_manager (SELECT only)
        
        logging.info("Store manager permissions granted successfully!")
        logging.info("Store manager can now:")
        logging.info("  - Access the retail schema")
        logging.info("  - SELECT, INSERT, UPDATE, DELETE on all tables")
        logging.info("  - Row Level Security policies will filter data based on rls_user_id")
        
    except Exception as e:
        logging.error(f"Error setting up store_manager permissions: {e}")
        raise

async def batch_insert(conn, query: str, data: List[Tuple], batch_size: int = 1000):
    """Insert data in batches using asyncio"""
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        await conn.executemany(query, batch)

async def insert_customers(conn, num_customers: int = 100000):
    """Insert customer data into the database"""
    try:
        logging.info(f"Generating {num_customers:,} customers...")
        
        # Get store IDs for assignment
        store_rows = await conn.fetch(f"SELECT store_id, store_name FROM {SCHEMA_NAME}.stores")
        store_ids = [row['store_id'] for row in store_rows]
        
        if not store_ids:
            raise Exception("No stores found! Please insert stores first.")
        
        customers_data = []
        
        for i in range(1, num_customers + 1):
            first_name = fake.first_name().replace("'", "''")  # Escape single quotes
            last_name = fake.last_name().replace("'", "''")
            email = f"{first_name.lower()}.{last_name.lower()}.{i}@example.com"
            phone = generate_phone_number()
            
            # Assign every customer to a store based on weighted distribution
            # Use the same weighted store choice as orders for consistency
            preferred_store_name = weighted_store_choice()
            primary_store_id = None
            for row in store_rows:
                if row['store_name'] == preferred_store_name:
                    primary_store_id = row['store_id']
                    break
            
            # Fallback to first store if lookup fails (should not happen)
            if primary_store_id is None:
                primary_store_id = store_rows[0]['store_id']
            
            customers_data.append((first_name, last_name, email, phone, primary_store_id))
        
        await batch_insert(conn, f"INSERT INTO {SCHEMA_NAME}.customers (first_name, last_name, email, phone, primary_store_id) VALUES ($1, $2, $3, $4, $5)", customers_data)
        
        # Log customer distribution by store
        distribution = await conn.fetch(f"""
            SELECT s.store_name, COUNT(c.customer_id) as customer_count,
                   ROUND(100.0 * COUNT(c.customer_id) / {num_customers}, 1) as percentage
            FROM {SCHEMA_NAME}.stores s
            LEFT JOIN {SCHEMA_NAME}.customers c ON s.store_id = c.primary_store_id
            GROUP BY s.store_id, s.store_name
            ORDER BY customer_count DESC
        """)
        
        no_store_count = await conn.fetchval(f"SELECT COUNT(*) FROM {SCHEMA_NAME}.customers WHERE primary_store_id IS NULL")
        
        logging.info("Customer distribution by store:")
        for row in distribution:
            logging.info(f"  {row['store_name']}: {row['customer_count']:,} customers ({row['percentage']}%)")
        if no_store_count > 0:
            logging.info(f"  No primary store: {no_store_count:,} customers ({100.0 * no_store_count / num_customers:.1f}%)")
        else:
            logging.info("  ✅ All customers have been assigned to stores!")
        
        logging.info(f"Successfully inserted {num_customers:,} customers!")
    except Exception as e:
        logging.error(f"Error inserting customers: {e}")
        raise

async def insert_stores(conn):
    """Insert store data into the database"""
    try:
        logging.info("Generating stores...")
        
        stores_data = []
        
        for store_name, store_config in stores.items():
            # Determine if this is an online store
            is_online = "online" in store_name.lower()
            # Get the fixed UUID from the reference data
            rls_user_id = store_config.get('rls_user_id')
            if not rls_user_id:
                raise ValueError(f"No rls_user_id found for store: {store_name}")
            stores_data.append((store_name, rls_user_id, is_online))
        
        await batch_insert(conn, f"INSERT INTO {SCHEMA_NAME}.stores (store_name, rls_user_id, is_online) VALUES ($1, $2, $3)", stores_data)
        
        # Log the manager IDs for workshop purposes
        rows = await conn.fetch(f"SELECT store_name, rls_user_id FROM {SCHEMA_NAME}.stores ORDER BY store_name")
        logging.info("Store Manager IDs (for workshop use):")
        for row in rows:
            logging.info(f"  {row['store_name']}: {row['rls_user_id']}")
        
        logging.info(f"Successfully inserted {len(stores_data):,} stores!")
    except Exception as e:
        logging.error(f"Error inserting stores: {e}")
        raise

async def insert_categories(conn):
    """Insert category data into the database"""
    try:
        logging.info("Generating categories...")
        
        categories_data = []
        
        # Extract unique categories from product data
        for main_category in main_categories.keys():
            categories_data.append((main_category,))
        
        await batch_insert(conn, f"INSERT INTO {SCHEMA_NAME}.categories (category_name) VALUES ($1)", categories_data)
        
        logging.info(f"Successfully inserted {len(categories_data):,} categories!")
    except Exception as e:
        logging.error(f"Error inserting categories: {e}")
        raise

async def insert_product_types(conn):
    """Insert product type data into the database"""
    try:
        logging.info("Generating product types...")
        
        product_types_data = []
        
        # Get category_id mapping
        category_mapping = {}
        rows = await conn.fetch(f"SELECT category_id, category_name FROM {SCHEMA_NAME}.categories")
        for row in rows:
            category_mapping[row['category_name']] = row['category_id']
        
        # Extract product types for each category
        for main_category, subcategories in main_categories.items():
            category_id = category_mapping[main_category]
            for subcategory in subcategories.keys():
                # Skip the seasonal multipliers key
                if subcategory == 'washington_seasonal_multipliers':
                    continue
                
                product_types_data.append((category_id, subcategory))
        
        await batch_insert(conn, f"INSERT INTO {SCHEMA_NAME}.product_types (category_id, type_name) VALUES ($1, $2)", product_types_data)
        
        logging.info(f"Successfully inserted {len(product_types_data):,} product types!")
    except Exception as e:
        logging.error(f"Error inserting product types: {e}")
        raise

async def insert_products(conn):
    """Insert product data into the database"""
    try:
        logging.info("Generating products...")
        
        # Get category and type mappings
        category_mapping = {}
        rows = await conn.fetch(f"SELECT category_id, category_name FROM {SCHEMA_NAME}.categories")
        for row in rows:
            category_mapping[row['category_name']] = row['category_id']
        
        type_mapping = {}
        rows = await conn.fetch(f"SELECT type_id, type_name, category_id FROM {SCHEMA_NAME}.product_types")
        for row in rows:
            type_mapping[(row['category_id'], row['type_name'])] = row['type_id']
        
        products_data = []
        
        for main_category, subcategories in main_categories.items():
            category_id = category_mapping[main_category]
            
            for subcategory, product_list in subcategories.items():
                # Skip the seasonal multipliers key, only process actual product types
                if subcategory == 'washington_seasonal_multipliers':
                    continue
                    
                if not product_list:  # Handle empty product lists
                    continue
                
                type_id = type_mapping.get((category_id, subcategory))
                if not type_id:
                    logging.warning(f"Type ID not found for category {main_category}, type {subcategory}")
                    continue
                    
                for product_details in product_list:
                    product_name = product_details["name"]
                    sku = product_details.get("sku", f"SKU{len(products_data)+1:06d}")  # Fallback if no SKU
                    json_price = product_details["price"]
                    description = product_details["description"]
                    
                    # Treat the JSON price as the cost
                    cost = float(json_price)
                    
                    # Calculate selling price for 33% gross margin
                    # Gross Margin = (Selling Price - Cost) / Selling Price = 0.33
                    # Therefore: Selling Price = Cost / (1 - 0.33) = Cost / 0.67
                    base_price = round(cost / 0.67, 2)
                    
                    products_data.append((sku, product_name, category_id, type_id, cost, base_price, description))
        
        await batch_insert(conn, f"INSERT INTO {SCHEMA_NAME}.products (sku, product_name, category_id, type_id, cost, base_price, product_description) VALUES ($1, $2, $3, $4, $5, $6, $7)", products_data)
        
        logging.info(f"Successfully inserted {len(products_data):,} products!")
        return len(products_data)  # Return the number of products inserted
    except Exception as e:
        logging.error(f"Error inserting products: {e}")
        raise

def get_store_multipliers(store_name):
    """Get order frequency multipliers based on store name"""
    store_data = stores.get(store_name, {
        'customer_distribution_weight': 1,
        'order_frequency_multiplier': 1.0, 
        'order_value_multiplier': 1.0
    })
    return {'orders': store_data.get('order_frequency_multiplier', 1.0)}

def get_yearly_weight(year):
    """Get the weight for each year to create growth pattern"""
    return reference_data['year_weights'].get(str(year), 1.0)

def weighted_year_choice():
    """Choose a year based on growth pattern weights"""
    years = [2020, 2021, 2022, 2023, 2024, 2025, 2026]
    weights = [get_yearly_weight(year) for year in years]
    return random.choices(years, weights=weights, k=1)[0]

async def get_store_id_by_name(conn, store_name):
    """Get store_id for a given store name"""
    row = await conn.fetchrow(f"SELECT store_id FROM {SCHEMA_NAME}.stores WHERE store_name = $1", store_name)
    return row['store_id'] if row else 1  # Default to store_id 1 if not found

def choose_seasonal_product_category(month):
    """Choose a category based on Washington State seasonal multipliers"""
    categories = []
    weights = []
    
    for category_name, category_data in main_categories.items():
        # Skip if no seasonal multipliers defined for this category
        if 'washington_seasonal_multipliers' not in category_data:
            categories.append(category_name)
            weights.append(1.0)  # Default weight
        else:
            seasonal_multipliers = category_data['washington_seasonal_multipliers']
            # Use month index (0-11) to get the multiplier
            seasonal_weight = seasonal_multipliers[month - 1]  # month is 1-12, array is 0-11
            categories.append(category_name)
            weights.append(seasonal_weight)
    
    return random.choices(categories, weights=weights, k=1)[0]

def choose_product_type(main_category):
    """Choose a product type within a category with equal weights"""
    product_types = []
    for key in main_categories[main_category].keys():
        if isinstance(main_categories[main_category][key], list):
            product_types.append(key)
    
    if not product_types:
        logging.warning(f"No product types found for category: {main_category}")
        return None
    return random.choice(product_types)

def extract_products_with_embeddings(product_data: Dict) -> List[Tuple[str, str, List[float]]]:
    """
    Extract products with image embeddings from the JSON structure.
    
    Returns:
        List of tuples: (sku, image_path, image_embedding)
    """
    products_with_embeddings = []
    
    for category_name, category_data in product_data.get('main_categories', {}).items():
        for product_type, products in category_data.items():
            # Skip non-product keys like seasonal multipliers
            if not isinstance(products, list):
                continue
                
            for product in products:
                if isinstance(product, dict):
                    sku = product.get('sku')
                    image_path = product.get('image_path')
                    image_embedding = product.get('image_embedding')
                    
                    if sku and image_path and image_embedding:
                        products_with_embeddings.append((sku, image_path, image_embedding))
                    else:
                        logging.debug(f"Skipping product with missing data: SKU={sku}")
    
    logging.info(f"Found {len(products_with_embeddings)} products with embeddings")
    return products_with_embeddings

async def get_product_id_by_sku(conn: asyncpg.Connection, sku: str) -> Optional[int]:
    """Get product_id for a given SKU"""
    try:
        result = await conn.fetchval(
            f"SELECT product_id FROM {SCHEMA_NAME}.products WHERE sku = $1",
            sku
        )
        return result
    except Exception as e:
        logging.error(f"Error getting product_id for SKU {sku}: {e}")
        return None

async def insert_product_embedding(
    conn: asyncpg.Connection, 
    product_id: int, 
    image_path: str, 
    image_embedding: List[float]
) -> bool:
    """Insert a product embedding record"""
    try:
        # Store just the image filename without any path prefix
        image_url = os.path.basename(image_path)
        
        # Convert the embedding list to a vector string format
        embedding_str = f"[{','.join([str(x) for x in image_embedding])}]"
        
        await conn.execute(
            f"""
            INSERT INTO {SCHEMA_NAME}.product_image_embeddings 
            (product_id, image_url, image_embedding) 
            VALUES ($1, $2, $3::vector)
            """,
            product_id, image_url, embedding_str
        )
        return True
    except Exception as e:
        logging.error(f"Error inserting embedding for product_id {product_id}: {e}")
        return False

async def clear_existing_embeddings(conn: asyncpg.Connection) -> None:
    """Clear all existing product image embeddings"""
    try:
        result = await conn.execute(f"DELETE FROM {SCHEMA_NAME}.product_image_embeddings")
        logging.info(f"Cleared existing embeddings: {result}")
    except Exception as e:
        logging.error(f"Error clearing existing embeddings: {e}")
        raise

async def populate_product_image_embeddings(conn: asyncpg.Connection, clear_existing: bool = False, batch_size: int = 100) -> None:
    """Populate product image embeddings from product_data.json"""
    
    logging.info("Loading product data for embeddings...")
    products_with_embeddings = extract_products_with_embeddings(product_data)
    
    if not products_with_embeddings:
        logging.warning("No products with embeddings found in the data")
        return
    
    try:
        # Clear existing embeddings if requested
        if clear_existing:
            logging.info("Clearing existing product embeddings...")
            await clear_existing_embeddings(conn)
        
        # Process products in batches
        inserted_count = 0
        skipped_count = 0
        error_count = 0
        
        for i in range(0, len(products_with_embeddings), batch_size):
            batch = products_with_embeddings[i:i + batch_size]
            
            logging.info(f"Processing embeddings batch {i//batch_size + 1}/{(len(products_with_embeddings) + batch_size - 1)//batch_size}")
            
            for sku, image_path, image_embedding in batch:
                # Get product_id for this SKU
                product_id = await get_product_id_by_sku(conn, sku)
                
                if product_id is None:
                    logging.debug(f"Product not found for SKU: {sku}")
                    skipped_count += 1
                    continue
                
                # Insert the embedding
                if await insert_product_embedding(conn, product_id, image_path, image_embedding):
                    inserted_count += 1
                else:
                    error_count += 1
        
        # Summary
        logging.info("Product embeddings population complete!")
        logging.info(f"  Inserted: {inserted_count}")
        logging.info(f"  Skipped (product not found): {skipped_count}")
        logging.info(f"  Errors: {error_count}")
        logging.info(f"  Total processed: {len(products_with_embeddings)}")
        
    except Exception as e:
        logging.error(f"Error populating product embeddings: {e}")
        raise

async def verify_embeddings_table(conn: asyncpg.Connection) -> None:
    """Verify the product_image_embeddings table exists and show sample data"""
    try:
        # Check table existence
        table_exists = await conn.fetchval(
            """
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = $1 AND table_name = 'product_image_embeddings'
            )
            """,
            SCHEMA_NAME
        )
        
        if not table_exists:
            logging.error(f"Table {SCHEMA_NAME}.product_image_embeddings does not exist!")
            return
        
        # Get row count
        count = await conn.fetchval(f"SELECT COUNT(*) FROM {SCHEMA_NAME}.product_image_embeddings")
        if count is None:
            count = 0
        logging.info(f"Product image embeddings table has {count} records")
        
        # Show sample data
        if count > 0:
            sample = await conn.fetch(
                f"""
                SELECT pe.product_id, p.sku, p.product_name, pe.image_url,
                       vector_dims(pe.image_embedding) as embedding_dimension
                FROM {SCHEMA_NAME}.product_image_embeddings pe
                JOIN {SCHEMA_NAME}.products p ON pe.product_id = p.product_id
                LIMIT 5
                """
            )
            
            logging.info("Sample embeddings data:")
            for row in sample:
                logging.info(f"  Product ID: {row['product_id']}, SKU: {row['sku']}, "
                           f"Product: {row['product_name'][:50]}..., "
                           f"Embedding dim: {row['embedding_dimension']}")
        
    except Exception as e:
        logging.error(f"Error verifying embeddings table: {e}")

def extract_products_with_description_embeddings(product_data: Dict) -> List[Tuple[str, List[float]]]:
    """
    Extract products with description embeddings from the JSON structure.
    
    Returns:
        List of tuples: (sku, description_embedding)
    """
    products_with_description_embeddings = []
    
    for _category_name, category_data in product_data.get('main_categories', {}).items():
        for _product_type, products in category_data.items():
            # Skip non-product keys like seasonal multipliers
            if not isinstance(products, list):
                continue
                
            for product in products:
                if isinstance(product, dict):
                    sku = product.get('sku')
                    description_embedding = product.get('description_embedding')
                    
                    if sku and description_embedding:
                        products_with_description_embeddings.append((sku, description_embedding))
                    else:
                        logging.debug(f"Skipping product with missing description embedding: SKU={sku}")
    
    logging.info(f"Found {len(products_with_description_embeddings)} products with description embeddings")
    return products_with_description_embeddings

async def insert_product_description_embedding(
    conn: asyncpg.Connection, 
    product_id: int, 
    description_embedding: List[float]
) -> bool:
    """Insert a product description embedding record"""
    try:
        # Convert the embedding list to a vector string format
        embedding_str = f"[{','.join([str(x) for x in description_embedding])}]"
        
        await conn.execute(
            f"""
            INSERT INTO {SCHEMA_NAME}.product_description_embeddings 
            (product_id, description_embedding) 
            VALUES ($1, $2::vector)
            """,
            product_id, embedding_str
        )
        return True
    except Exception as e:
        logging.error(f"Error inserting description embedding for product_id {product_id}: {e}")
        return False

async def clear_existing_description_embeddings(conn: asyncpg.Connection) -> None:
    """Clear all existing product description embeddings"""
    try:
        result = await conn.execute(f"DELETE FROM {SCHEMA_NAME}.product_description_embeddings")
        logging.info(f"Cleared existing description embeddings: {result}")
    except Exception as e:
        logging.error(f"Error clearing existing description embeddings: {e}")
        raise

async def populate_product_description_embeddings(conn: asyncpg.Connection, clear_existing: bool = False, batch_size: int = 100) -> None:
    """Populate product description embeddings from product_data.json"""
    
    logging.info("Loading product data for description embeddings...")
    products_with_description_embeddings = extract_products_with_description_embeddings(product_data)
    
    if not products_with_description_embeddings:
        logging.warning("No products with description embeddings found in the data")
        return
    
    try:
        # Clear existing description embeddings if requested
        if clear_existing:
            logging.info("Clearing existing product description embeddings...")
            await clear_existing_description_embeddings(conn)
        
        # Process products in batches
        inserted_count = 0
        skipped_count = 0
        error_count = 0
        
        for i in range(0, len(products_with_description_embeddings), batch_size):
            batch = products_with_description_embeddings[i:i + batch_size]
            
            logging.info(f"Processing description embeddings batch {i//batch_size + 1}/{(len(products_with_description_embeddings) + batch_size - 1)//batch_size}")
            
            for sku, description_embedding in batch:
                # Get product_id for this SKU
                product_id = await get_product_id_by_sku(conn, sku)
                
                if product_id is None:
                    logging.debug(f"Product not found for SKU: {sku}")
                    skipped_count += 1
                    continue
                
                # Insert the description embedding
                if await insert_product_description_embedding(conn, product_id, description_embedding):
                    inserted_count += 1
                else:
                    error_count += 1
        
        # Summary
        logging.info("Product description embeddings population complete!")
        logging.info(f"  Inserted: {inserted_count}")
        logging.info(f"  Skipped (product not found): {skipped_count}")
        logging.info(f"  Errors: {error_count}")
        logging.info(f"  Total processed: {len(products_with_description_embeddings)}")
        
    except Exception as e:
        logging.error(f"Error populating product description embeddings: {e}")
        raise

async def verify_description_embeddings_table(conn: asyncpg.Connection) -> None:
    """Verify the product_description_embeddings table exists and show sample data"""
    try:
        # Check table existence
        table_exists = await conn.fetchval(
            """
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = $1 AND table_name = 'product_description_embeddings'
            )
            """,
            SCHEMA_NAME
        )
        
        if not table_exists:
            logging.error(f"Table {SCHEMA_NAME}.product_description_embeddings does not exist!")
            return
        
        # Get row count
        count = await conn.fetchval(f"SELECT COUNT(*) FROM {SCHEMA_NAME}.product_description_embeddings")
        if count is None:
            count = 0
        logging.info(f"Product description embeddings table has {count} records")
        
        # Show sample data
        if count > 0:
            sample = await conn.fetch(
                f"""
                SELECT pe.product_id, p.sku, p.product_name,
                       vector_dims(pe.description_embedding) as embedding_dimension
                FROM {SCHEMA_NAME}.product_description_embeddings pe
                JOIN {SCHEMA_NAME}.products p ON pe.product_id = p.product_id
                LIMIT 5
                """
            )
            
            logging.info("Sample description embeddings data:")
            for row in sample:
                logging.info(f"  Product ID: {row['product_id']}, SKU: {row['sku']}, "
                           f"Product: {row['product_name'][:50]}..., "
                           f"Embedding dim: {row['embedding_dimension']}")
        
    except Exception as e:
        logging.error(f"Error verifying description embeddings table: {e}")

async def insert_inventory(conn):
    """Insert inventory data distributed across stores based on customer distribution weights and seasonal trends"""
    try:
        logging.info("Generating inventory with seasonal considerations...")
        
        # Get all stores and products with category information
        stores_data = await conn.fetch(f"SELECT store_id, store_name FROM {SCHEMA_NAME}.stores")
        products_data = await conn.fetch(f"""
            SELECT p.product_id, c.category_name 
            FROM {SCHEMA_NAME}.products p
            JOIN {SCHEMA_NAME}.categories c ON p.category_id = c.category_id
        """)
        
        # Build category to seasonal multiplier mapping (using average across year for base inventory)
        category_seasonal_avg = {}
        for category_name, category_data in main_categories.items():
            if 'washington_seasonal_multipliers' in category_data:
                seasonal_multipliers = category_data['washington_seasonal_multipliers']
                # Use average seasonal multiplier for inventory planning
                avg_multiplier = sum(seasonal_multipliers) / len(seasonal_multipliers)
                category_seasonal_avg[category_name] = avg_multiplier
            else:
                category_seasonal_avg[category_name] = 1.0  # Default multiplier
        
        inventory_data = []
        
        for store in stores_data:
            store_id = store['store_id']
            store_name = store['store_name']
            
            # Get store configuration for inventory distribution
            store_config = stores.get(store_name, {})
            base_stock_multiplier = store_config.get('customer_distribution_weight', 1.0)
            
            for product in products_data:
                product_id = product['product_id']
                category_name = product['category_name']
                
                # Get seasonal multiplier for this category
                seasonal_multiplier = category_seasonal_avg.get(category_name, 1.0)
                
                # Generate stock level based on store weight, seasonal trends, and random variation
                base_stock = random.randint(10, 100)
                stock_level = int(base_stock * base_stock_multiplier * seasonal_multiplier * random.uniform(0.5, 1.5))
                stock_level = max(1, stock_level)  # Ensure at least 1 item in stock
                
                inventory_data.append((store_id, product_id, stock_level))
        
        await batch_insert(conn, f"INSERT INTO {SCHEMA_NAME}.inventory (store_id, product_id, stock_level) VALUES ($1, $2, $3)", inventory_data)
        
        logging.info(f"Successfully inserted {len(inventory_data):,} inventory records with seasonal adjustments!")
        
    except Exception as e:
        logging.error(f"Error inserting inventory: {e}")
        raise

async def build_product_lookup(conn):
    """Build a lookup table mapping (main_category, product_type, product_name) to product_id"""
    product_lookup = {}
    
    # Get all products with their category and type information
    rows = await conn.fetch(f"""
        SELECT p.product_id, p.product_name, c.category_name, pt.type_name
        FROM {SCHEMA_NAME}.products p
        JOIN {SCHEMA_NAME}.categories c ON p.category_id = c.category_id
        JOIN {SCHEMA_NAME}.product_types pt ON p.type_id = pt.type_id
    """)
    
    for row in rows:
        key = (row['category_name'], row['type_name'], row['product_name'])
        product_lookup[key] = row['product_id']
    
    logging.info(f"Built product lookup with {len(product_lookup)} products")
    return product_lookup

async def insert_orders(conn, num_customers: int = 100000, product_lookup: Optional[Dict] = None):
    """Insert order data into the database with separate orders and order_items tables"""
    
    # Build product lookup if not provided
    if product_lookup is None:
        product_lookup = await build_product_lookup(conn)
    
    logging.info(f"Generating orders for {num_customers:,} customers...")
    
    # Get available product IDs for faster random selection and build category mapping
    product_rows = await conn.fetch(f"""
        SELECT p.product_id, p.cost, p.base_price, c.category_name 
        FROM {SCHEMA_NAME}.products p
        JOIN {SCHEMA_NAME}.categories c ON p.category_id = c.category_id
    """)
    
    product_prices = {row['product_id']: float(row['base_price']) for row in product_rows}
    available_product_ids = list(product_prices.keys())
    
    # Build category to product ID mapping for seasonal selection
    category_products = {}
    for row in product_rows:
        category_name = row['category_name']
        if category_name not in category_products:
            category_products[category_name] = []
        category_products[category_name].append(row['product_id'])
    
    logging.info(f"Built category mapping with {len(category_products)} categories")
    
    total_orders = 0
    orders_data = []
    order_items_data = []
    
    for customer_id in range(1, num_customers + 1):
        # Determine store preference for this customer
        preferred_store = weighted_store_choice()
        store_id = await get_store_id_by_name(conn, preferred_store)
        
        # Get store multipliers
        store_multipliers = get_store_multipliers(preferred_store)
        order_frequency = store_multipliers['orders']
        
        # Determine number of orders for this customer (weighted by store)
        base_orders = random.choices([0, 1, 2, 3, 4, 5], weights=[20, 40, 20, 10, 7, 3], k=1)[0]
        num_orders = max(1, int(base_orders * order_frequency))
        
        for _ in range(num_orders):
            total_orders += 1
            order_id = total_orders
            
            # Generate order date with yearly growth pattern
            year = weighted_year_choice()
            month = random.randint(1, 12)
            
            # Use seasonal category selection for realistic patterns
            selected_category = None
            if seasonal_categories:
                # Choose category based on seasonal multipliers for this month
                # Increase seasonal bias by selecting seasonal category with higher probability
                if random.random() < 0.85:  # 85% seasonal selection
                    selected_category = choose_seasonal_product_category(month)
                else:
                    selected_category = random.choice(list(main_categories.keys()))
            else:
                # No seasonal trends available, use random category selection
                selected_category = random.choice(list(main_categories.keys()))
            
            # Generate random day within the month
            if month == 2:  # February
                max_day = 28 if year % 4 != 0 else 29
            elif month in [4, 6, 9, 11]:  # April, June, September, November
                max_day = 30
            else:
                max_day = 31
            
            day = random.randint(1, max_day)
            order_date = date(year, month, day)
            
            orders_data.append((customer_id, store_id, order_date))
            
            # Generate order items for this order
            num_items = random.choices([1, 2, 3, 4, 5], weights=[40, 30, 15, 10, 5], k=1)[0]
            
            for _ in range(num_items):
                # Select product based on seasonal category preferences
                if seasonal_categories and selected_category in category_products:
                    # Use seasonally-appropriate products with 90% probability (increased from 70%)
                    if random.random() < 0.9:
                        product_id = random.choice(category_products[selected_category])
                    else:
                        # 10% chance to select from any category (for variety)
                        product_id = random.choice(available_product_ids)
                else:
                    # No seasonal data available or category not found, use random selection
                    product_id = random.choice(available_product_ids)
                    
                base_price = product_prices[product_id]
                
                # Generate quantity and pricing
                quantity = random.choices([1, 2, 3, 4, 5], weights=[60, 25, 10, 3, 2], k=1)[0]
                unit_price = base_price * random.uniform(0.8, 1.2)  # Price variation
                
                # Apply discounts occasionally
                discount_percent = 0
                discount_amount = 0
                if random.random() < 0.15:  # 15% chance of discount
                    discount_percent = random.choice([5, 10, 15, 20, 25])
                    discount_amount = (unit_price * quantity * discount_percent) / 100
                
                total_amount = (unit_price * quantity) - discount_amount
                
                order_items_data.append((
                    order_id, store_id, product_id, quantity, unit_price, 
                    discount_percent, discount_amount, total_amount
                ))
        
        # Batch insert every 1000 customers to manage memory
        if customer_id % 1000 == 0:
            if orders_data:
                await batch_insert(conn, f"""
                    INSERT INTO {SCHEMA_NAME}.orders (customer_id, store_id, order_date) 
                    VALUES ($1, $2, $3)
                """, orders_data)
                orders_data = []
            
            if order_items_data:
                await batch_insert(conn, f"""
                    INSERT INTO {SCHEMA_NAME}.order_items 
                    (order_id, store_id, product_id, quantity, unit_price, discount_percent, discount_amount, total_amount) 
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                """, order_items_data)
                order_items_data = []
            
            if customer_id % 5000 == 0:
                logging.info(f"Processed {customer_id:,} customers, generated {total_orders:,} orders")
    
    # Insert remaining data
    if orders_data:
        await batch_insert(conn, f"""
            INSERT INTO {SCHEMA_NAME}.orders (customer_id, store_id, order_date) 
            VALUES ($1, $2, $3)
        """, orders_data)
    
    if order_items_data:
        await batch_insert(conn, f"""
            INSERT INTO {SCHEMA_NAME}.order_items 
            (order_id, store_id, product_id, quantity, unit_price, discount_percent, discount_amount, total_amount) 
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        """, order_items_data)
    
    logging.info(f"Successfully inserted {total_orders:,} orders!")
    
    # Get order items count
    order_items_count = await conn.fetchval(f"SELECT COUNT(*) FROM {SCHEMA_NAME}.order_items")
    logging.info(f"Successfully inserted {order_items_count:,} order items!")

async def verify_database_contents(conn):
    """Verify database contents and show key statistics"""
    
    logging.info("\n" + "=" * 60)
    logging.info("DATABASE VERIFICATION & STATISTICS")
    logging.info("=" * 60)
    
    # Store distribution verification
    logging.info("\n🏪 STORE SALES DISTRIBUTION:")
    rows = await conn.fetch(f"""
        SELECT s.store_name, 
               COUNT(o.order_id) as orders,
               ROUND(SUM(oi.total_amount)/1000.0, 1) || 'K' as revenue,
               ROUND(100.0 * COUNT(o.order_id) / (SELECT COUNT(*) FROM {SCHEMA_NAME}.orders), 1) || '%' as order_pct
        FROM {SCHEMA_NAME}.orders o 
        JOIN {SCHEMA_NAME}.stores s ON o.store_id = s.store_id
        JOIN {SCHEMA_NAME}.order_items oi ON o.order_id = oi.order_id
        GROUP BY s.store_id, s.store_name
        ORDER BY SUM(oi.total_amount) DESC
    """)
    
    logging.info("   Store               Orders     Revenue    % of Orders")
    logging.info("   " + "-" * 50)
    for row in rows:
        logging.info(f"   {row['store_name']:<18} {row['orders']:>6}     ${row['revenue']:>6}    {row['order_pct']:>6}")
    
    # Year-over-year growth verification
    logging.info("\n📈 YEAR-OVER-YEAR GROWTH PATTERN:")
    rows = await conn.fetch(f"""
        SELECT EXTRACT(YEAR FROM o.order_date) as year,
               COUNT(DISTINCT o.order_id) as orders,
               ROUND(SUM(oi.total_amount)/1000.0, 1) || 'K' as revenue
        FROM {SCHEMA_NAME}.orders o
        JOIN {SCHEMA_NAME}.order_items oi ON o.order_id = oi.order_id
        GROUP BY EXTRACT(YEAR FROM o.order_date)
        ORDER BY year
    """)
    
    logging.info("   Year    Orders     Revenue    Growth")
    logging.info("   " + "-" * 35)
    prev_revenue = None
    for row in rows:
        revenue_num = float(row['revenue'].replace('K', ''))
        growth = ""
        if prev_revenue is not None:
            growth_pct = ((revenue_num - prev_revenue) / prev_revenue) * 100
            growth = f"{growth_pct:+.1f}%"
        logging.info(f"   {int(row['year'])}    {row['orders']:>6}     ${row['revenue']:>6}    {growth:>6}")
        prev_revenue = revenue_num
    
    # Product category distribution
    logging.info("\n🛍️  TOP PRODUCT CATEGORIES:")
    rows = await conn.fetch(f"""
        SELECT c.category_name,
               COUNT(DISTINCT o.order_id) as orders,
               ROUND(SUM(oi.total_amount)/1000.0, 1) || 'K' as revenue
        FROM {SCHEMA_NAME}.categories c
        JOIN {SCHEMA_NAME}.products p ON c.category_id = p.category_id
        JOIN {SCHEMA_NAME}.order_items oi ON p.product_id = oi.product_id
        JOIN {SCHEMA_NAME}.orders o ON oi.order_id = o.order_id
        GROUP BY c.category_id, c.category_name
        ORDER BY SUM(oi.total_amount) DESC
        LIMIT 5
    """)
    
    logging.info("   Category             Orders     Revenue")
    logging.info("   " + "-" * 40)
    for row in rows:
        logging.info(f"   {row['category_name']:<18} {row['orders']:>6}     ${row['revenue']:>6}")
    
    # Final summary
    customers = await conn.fetchval(f"SELECT COUNT(*) FROM {SCHEMA_NAME}.customers")
    products = await conn.fetchval(f"SELECT COUNT(*) FROM {SCHEMA_NAME}.products")
    orders = await conn.fetchval(f"SELECT COUNT(*) FROM {SCHEMA_NAME}.orders")
    order_items = await conn.fetchval(f"SELECT COUNT(*) FROM {SCHEMA_NAME}.order_items")
    embeddings = await conn.fetchval(f"SELECT COUNT(*) FROM {SCHEMA_NAME}.product_image_embeddings")
    total_revenue = await conn.fetchval(f"SELECT SUM(total_amount) FROM {SCHEMA_NAME}.order_items")
    
    # Gross margin analysis
    logging.info("\n💰 GROSS MARGIN ANALYSIS:")
    margin_stats = await conn.fetch(f"""
        SELECT 
            COUNT(*) as product_count,
            AVG(cost) as avg_cost,
            AVG(base_price) as avg_selling_price,
            AVG((base_price - cost) / base_price * 100) as avg_gross_margin_percent,
            MIN((base_price - cost) / base_price * 100) as min_gross_margin_percent,
            MAX((base_price - cost) / base_price * 100) as max_gross_margin_percent
        FROM {SCHEMA_NAME}.products
    """)
    
    if margin_stats:
        stats = margin_stats[0]
        logging.info(f"   Average Cost:           ${stats['avg_cost']:.2f}")
        logging.info(f"   Average Selling Price:  ${stats['avg_selling_price']:.2f}")
        logging.info(f"   Average Gross Margin:   {stats['avg_gross_margin_percent']:.1f}%")
        logging.info(f"   Margin Range:           {stats['min_gross_margin_percent']:.1f}% - {stats['max_gross_margin_percent']:.1f}%")
    
    # Calculate total cost and gross profit from actual sales
    sales_margin = await conn.fetchrow(f"""
        SELECT 
            SUM(oi.total_amount) as total_revenue,
            SUM(p.cost * oi.quantity) as total_cost,
            SUM(oi.total_amount) - SUM(p.cost * oi.quantity) as total_gross_profit
        FROM {SCHEMA_NAME}.order_items oi
        JOIN {SCHEMA_NAME}.products p ON oi.product_id = p.product_id
    """)
    
    if sales_margin and sales_margin['total_revenue']:
        actual_margin_pct = (sales_margin['total_gross_profit'] / sales_margin['total_revenue']) * 100
        logging.info(f"   Actual Sales Margin:    {actual_margin_pct:.1f}%")
        logging.info(f"   Total Cost of Goods:    ${sales_margin['total_cost']:.2f}")
        logging.info(f"   Total Gross Profit:     ${sales_margin['total_gross_profit']:.2f}")

    logging.info("\n✅ DATABASE SUMMARY:")
    logging.info(f"   Customers:          {customers:>8,}")
    logging.info(f"   Products:           {products:>8,}")
    logging.info(f"   Product Embeddings: {embeddings:>8,}")
    logging.info(f"   Orders:             {orders:>8,}")
    logging.info(f"   Order Items:        {order_items:>8,}")
    if total_revenue and orders:
        logging.info(f"   Total Revenue:      ${total_revenue/1000:.1f}K")
        logging.info(f"   Avg Order:          ${total_revenue/orders:.2f}")
        logging.info(f"   Orders/Customer:    {orders/customers:.1f}")
        logging.info(f"   Items/Order:        {order_items/orders:.1f}")

async def verify_seasonal_patterns(conn):
    """Verify that orders and inventory follow seasonal patterns from product_data.json"""
    
    logging.info("\n" + "=" * 60)
    logging.info("🌱 SEASONAL PATTERNS VERIFICATION")
    logging.info("=" * 60)
    
    try:
        # Test 1: Order seasonality by category and month
        logging.info("\n📊 ORDER SEASONALITY BY CATEGORY:")
        logging.info("   Testing if orders follow seasonal multipliers from product_data.json")
        
        # Get actual orders by month and category
        rows = await conn.fetch(f"""
            SELECT c.category_name,
                   EXTRACT(MONTH FROM o.order_date) as month,
                   COUNT(DISTINCT o.order_id) as order_count,
                   ROUND(AVG(oi.total_amount), 2) as avg_order_value
            FROM {SCHEMA_NAME}.orders o
            JOIN {SCHEMA_NAME}.order_items oi ON o.order_id = oi.order_id
            JOIN {SCHEMA_NAME}.products p ON oi.product_id = p.product_id
            JOIN {SCHEMA_NAME}.categories c ON p.category_id = c.category_id
            GROUP BY c.category_name, EXTRACT(MONTH FROM o.order_date)
            HAVING COUNT(DISTINCT o.order_id) > 0
            ORDER BY c.category_name, month
        """)
        
        # Organize data by category
        category_data = {}
        for row in rows:
            category = row['category_name']
            month = int(row['month'])
            if category not in category_data:
                category_data[category] = {}
            category_data[category][month] = {
                'order_count': row['order_count'],
                'avg_order_value': float(row['avg_order_value'])
            }
        
        # Compare with seasonal multipliers
        seasonal_matches = 0
        total_seasonal_categories = 0
        
        month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                       "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        
        for category_name, category_config in main_categories.items():
            if 'washington_seasonal_multipliers' not in category_config:
                continue
                
            total_seasonal_categories += 1
            seasonal_multipliers = category_config['washington_seasonal_multipliers']
            
            if category_name not in category_data:
                logging.warning(f"   ⚠️  No orders found for seasonal category: {category_name}")
                continue
            
            # Find peak and low months from data
            data_months = category_data[category_name]
            if len(data_months) < 6:  # Need reasonable sample size
                logging.warning(f"   ⚠️  Insufficient data for {category_name} ({len(data_months)} months)")
                continue
            
            # Get peak months from multipliers and data
            multiplier_peak_month = seasonal_multipliers.index(max(seasonal_multipliers)) + 1
            multiplier_low_month = seasonal_multipliers.index(min(seasonal_multipliers)) + 1
            
            data_peak_month = max(data_months.keys(), key=lambda m: data_months[m]['order_count'])
            data_low_month = min(data_months.keys(), key=lambda m: data_months[m]['order_count'])
            
            # Check if peaks align (within 3 months tolerance for seasonality to account for data variation)
            peak_match = abs(multiplier_peak_month - data_peak_month) <= 3 or \
                        abs(multiplier_peak_month - data_peak_month) >= 9  # Account for year wraparound
            
            low_match = abs(multiplier_low_month - data_low_month) <= 3 or \
                       abs(multiplier_low_month - data_low_month) >= 9
            
            # Also check if the actual seasonal trend direction is correct (high vs low months)
            data_peak_count = data_months[data_peak_month]['order_count']
            data_low_count = data_months[data_low_month]['order_count']
            
            # Verify the trend direction is correct (peak > low by reasonable margin)
            trend_correct = data_peak_count > data_low_count * 1.1  # At least 10% difference
            
            if (peak_match or low_match) and trend_correct:
                seasonal_matches += 1
                status = "✅"
            elif peak_match or low_match or trend_correct:
                seasonal_matches += 0.5  # Partial credit for trend direction
                status = "⚠️ "
            else:
                status = "❌"
            
            logging.info(f"   {status} {category_name}:")
            logging.info(f"      Expected peak: {month_names[multiplier_peak_month-1]} ({max(seasonal_multipliers):.1f})")
            logging.info(f"      Actual peak:   {month_names[data_peak_month-1]} ({data_months[data_peak_month]['order_count']} orders)")
            logging.info(f"      Expected low:  {month_names[multiplier_low_month-1]} ({min(seasonal_multipliers):.1f})")
            logging.info(f"      Actual low:    {month_names[data_low_month-1]} ({data_months[data_low_month]['order_count']} orders)")
        
        # Test 2: Inventory seasonality
        logging.info("\n📦 INVENTORY SEASONALITY:")
        logging.info("   Testing if inventory levels reflect seasonal patterns")
        
        # Initialize inventory tracking variables
        inventory_matches = 0
        total_inventory_categories = 0
        inventory_match_rate = 0
        
        # Get average inventory by category
        inventory_rows = await conn.fetch(f"""
            SELECT c.category_name,
                   AVG(i.stock_level) as avg_stock,
                   COUNT(*) as product_count
            FROM {SCHEMA_NAME}.inventory i
            JOIN {SCHEMA_NAME}.products p ON i.product_id = p.product_id
            JOIN {SCHEMA_NAME}.categories c ON p.category_id = c.category_id
            GROUP BY c.category_name
            ORDER BY avg_stock DESC
        """)
        
        # Calculate expected inventory ratios based on seasonal averages
        expected_inventory = {}
        for category_name, category_config in main_categories.items():
            if 'washington_seasonal_multipliers' in category_config:
                seasonal_multipliers = category_config['washington_seasonal_multipliers']
                avg_multiplier = sum(seasonal_multipliers) / len(seasonal_multipliers)
                expected_inventory[category_name] = avg_multiplier
        
        # Compare actual vs expected inventory ratios
        inventory_data = {row['category_name']: float(row['avg_stock']) for row in inventory_rows}
        
        if expected_inventory and inventory_data:
            # Normalize both to relative ratios
            base_expected = min(expected_inventory.values())
            base_actual = min(inventory_data.values())
            
            for category_name in expected_inventory:
                if category_name not in inventory_data:
                    continue
                    
                total_inventory_categories += 1
                expected_ratio = expected_inventory[category_name] / base_expected
                actual_ratio = inventory_data[category_name] / base_actual
                
                # Allow 30% tolerance for inventory matching
                ratio_diff = abs(expected_ratio - actual_ratio) / expected_ratio
                if ratio_diff <= 0.3:
                    inventory_matches += 1
                    status = "✅"
                else:
                    status = "❌"
                
                logging.info(f"   {status} {category_name}:")
                logging.info(f"      Expected ratio: {expected_ratio:.2f}")
                logging.info(f"      Actual ratio:   {actual_ratio:.2f}")
                logging.info(f"      Avg stock:      {inventory_data[category_name]:.1f}")
        
        # Calculate inventory match rate
        if total_inventory_categories > 0:
            inventory_match_rate = (inventory_matches / total_inventory_categories) * 100
        
        # Test 3: Monthly order distribution
        logging.info("\n📈 MONTHLY ORDER DISTRIBUTION:")
        monthly_totals = await conn.fetch(f"""
            SELECT EXTRACT(MONTH FROM o.order_date) as month,
                   COUNT(DISTINCT o.order_id) as total_orders
            FROM {SCHEMA_NAME}.orders o
            GROUP BY EXTRACT(MONTH FROM o.order_date)
            ORDER BY month
        """)
        
        if monthly_totals:
            total_orders = sum(row['total_orders'] for row in monthly_totals)
            logging.info("   Month    Orders    % of Total")
            logging.info("   " + "-" * 30)
            for row in monthly_totals:
                month_num = int(row['month'])
                pct = (row['total_orders'] / total_orders) * 100
                logging.info(f"   {month_names[month_num-1]:<6} {row['total_orders']:>8}    {pct:>6.1f}%")
        
        # Summary
        logging.info("\n🎯 SEASONAL VERIFICATION SUMMARY:")
        if total_seasonal_categories > 0:
            order_match_rate = (seasonal_matches / total_seasonal_categories) * 100
            logging.info(f"   Order seasonality match rate: {seasonal_matches}/{total_seasonal_categories} ({order_match_rate:.1f}%)")
        
        if total_inventory_categories > 0:
            logging.info(f"   Inventory seasonality match rate: {inventory_matches}/{total_inventory_categories} ({inventory_match_rate:.1f}%)")
        
        # Overall assessment
        if total_seasonal_categories > 0 and seasonal_matches >= total_seasonal_categories * 0.7:
            logging.info("   ✅ SEASONAL PATTERNS VERIFIED: Orders follow expected seasonal trends")
        else:
            logging.info("   ⚠️  SEASONAL PATTERNS PARTIAL: Some discrepancies found in seasonal trends")
        
        if inventory_match_rate >= 70:
            logging.info("   ✅ INVENTORY SEASONALITY VERIFIED: Stock levels reflect seasonal patterns")
        else:
            logging.info("   ⚠️  INVENTORY SEASONALITY PARTIAL: Some discrepancies in seasonal stock levels")
            
    except Exception as e:
        logging.error(f"Error verifying seasonal patterns: {e}")
        raise

async def generate_postgresql_database(num_customers: int = 50000):
    """Generate complete PostgreSQL database"""
    try:
        # Create connection
        conn = await create_connection()
        
        try:
            # Drop existing tables to start fresh (optional)
            logging.info("Dropping existing tables if they exist...")
            await conn.execute(f"DROP SCHEMA IF EXISTS {SCHEMA_NAME} CASCADE")
            
            await create_database_schema(conn)
            await insert_stores(conn)
            await insert_categories(conn)
            await insert_product_types(conn)
            await insert_customers(conn, num_customers)
            await insert_products(conn)
            
            # Populate product embeddings from product_data.json
            logging.info("\n" + "=" * 50)
            logging.info("POPULATING PRODUCT EMBEDDINGS")
            logging.info("=" * 50)
            await populate_product_image_embeddings(conn, clear_existing=True)
            await populate_product_description_embeddings(conn, clear_existing=True)
            
            # Verify embeddings were populated
            logging.info("\n" + "=" * 50)
            logging.info("VERIFYING PRODUCT EMBEDDINGS")
            logging.info("=" * 50)
            await verify_embeddings_table(conn)
            await verify_description_embeddings_table(conn)
            
            # Insert inventory data
            logging.info("\n" + "=" * 50)
            logging.info("INSERTING INVENTORY DATA")
            logging.info("=" * 50)
            await insert_inventory(conn)
            
            # Insert order data
            logging.info("\n" + "=" * 50)
            logging.info("INSERTING ORDER DATA")
            logging.info("=" * 50)
            await insert_orders(conn, num_customers)
            
            # Verify the database was created and has data
            logging.info("\n" + "=" * 50)
            logging.info("FINAL DATABASE VERIFICATION")
            logging.info("=" * 50)
            await verify_database_contents(conn)
            
            # Verify seasonal patterns are working
            await verify_seasonal_patterns(conn)
            
            logging.info("\n" + "=" * 50)
            logging.info("DATABASE GENERATION COMPLETE")
            logging.info("=" * 50)
            
            logging.info("Database generation completed successfully.")
        except Exception as e:
            logging.error(f"Error during database generation: {e}")
            raise
        finally:
            await conn.close()
            logging.info("Database connection closed.")

    except Exception as e:
        logging.error(f"Failed to generate database: {e}")
        raise

async def show_database_stats():
    """Show database statistics"""
    
    logging.info("\n" + "=" * 40)
    logging.info("DATABASE STATISTICS")
    logging.info("=" * 40)
    
    conn = await create_connection()
    
    try:
        # Get table row counts
        customers_count = await conn.fetchval(f"SELECT COUNT(*) FROM {SCHEMA_NAME}.customers")
        products_count = await conn.fetchval(f"SELECT COUNT(*) FROM {SCHEMA_NAME}.products")
        orders_count = await conn.fetchval(f"SELECT COUNT(*) FROM {SCHEMA_NAME}.orders")
        order_items_count = await conn.fetchval(f"SELECT COUNT(*) FROM {SCHEMA_NAME}.order_items")
        embeddings_count = await conn.fetchval(f"SELECT COUNT(*) FROM {SCHEMA_NAME}.product_image_embeddings")
        
        # Get revenue information
        total_revenue = await conn.fetchval(f"SELECT SUM(total_amount) FROM {SCHEMA_NAME}.order_items")
        if total_revenue is None:
            total_revenue = 0
            
        # Count indexes
        index_count = await conn.fetchval(f"""
            SELECT COUNT(*) FROM pg_indexes 
            WHERE schemaname = '{SCHEMA_NAME}' AND indexname LIKE 'idx_%'
        """)
        
        # Get database size
        db_size = await conn.fetchval(f"""
            SELECT pg_size_pretty(pg_database_size('{POSTGRES_CONFIG['database']}'))
        """)
        
        logging.info(f"Database Size: {db_size}")
        logging.info(f"Customers: {customers_count:,}")
        logging.info(f"Products: {products_count:,}")
        logging.info(f"Product Embeddings: {embeddings_count:,}")
        logging.info(f"Orders: {orders_count:,}")
        logging.info(f"Order Items: {order_items_count:,}")
        logging.info(f"Total Revenue: ${total_revenue:,.2f}")
        if orders_count > 0:
            logging.info(f"Average Order Value: ${total_revenue/orders_count:.2f}")
            logging.info(f"Orders per Customer: {orders_count/customers_count:.1f}")
            logging.info(f"Items per Order: {order_items_count/orders_count:.1f}")
        logging.info(f"Performance Indexes: {index_count}")
        
        # Show sample embeddings if they exist
        if embeddings_count > 0:
            await verify_embeddings_table(conn)
        
    finally:
        await conn.close()

async def main():
    """Main function to handle command line arguments"""
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description='Generate PostgreSQL database with product embeddings')
    parser.add_argument('--show-stats', action='store_true', 
                       help='Show database statistics instead of generating')
    parser.add_argument('--embeddings-only', action='store_true',
                       help='Only populate product embeddings (database must already exist)')
    parser.add_argument('--verify-embeddings', action='store_true',
                       help='Only verify embeddings table and show sample data')
    parser.add_argument('--verify-seasonal', action='store_true',
                       help='Only verify seasonal patterns in existing database')
    parser.add_argument('--clear-embeddings', action='store_true',
                       help='Clear existing embeddings before populating (used with --embeddings-only)')
    parser.add_argument('--batch-size', type=int, default=100,
                       help='Batch size for processing embeddings (default: 100)')
    parser.add_argument('--num-customers', type=int, default=50000,
                       help='Number of customers to generate (default: 50000)')
    
    args = parser.parse_args()
    
    try:
        if args.show_stats:
            # Show database statistics
            await show_database_stats()
        elif args.verify_embeddings:
            # Verify embeddings only
            conn = await create_connection()
            try:
                await verify_embeddings_table(conn)
                await verify_description_embeddings_table(conn)
            finally:
                await conn.close()
        elif args.verify_seasonal:
            # Verify seasonal patterns only
            conn = await create_connection()
            try:
                await verify_seasonal_patterns(conn)
            finally:
                await conn.close()
        elif args.embeddings_only:
            # Populate embeddings only
            conn = await create_connection()
            try:
                await populate_product_image_embeddings(conn, clear_existing=args.clear_embeddings, batch_size=args.batch_size)
                await populate_product_description_embeddings(conn, clear_existing=args.clear_embeddings, batch_size=args.batch_size)
                await verify_embeddings_table(conn)
                await verify_description_embeddings_table(conn)
            finally:
                await conn.close()
        else:
            # Generate the complete database
            logging.info(f"Database will be created at {POSTGRES_CONFIG['host']}:{POSTGRES_CONFIG['port']}/{POSTGRES_CONFIG['database']}")
            logging.info(f"Schema: {SCHEMA_NAME}")
            await generate_postgresql_database(num_customers=args.num_customers)
            
            logging.info("\nDatabase generated successfully!")
            logging.info(f"Host: {POSTGRES_CONFIG['host']}:{POSTGRES_CONFIG['port']}")
            logging.info(f"Database: {POSTGRES_CONFIG['database']}")
            logging.info(f"Schema: {SCHEMA_NAME}")
            logging.info(f"To view statistics: python {sys.argv[0]} --show-stats")
            logging.info(f"To populate embeddings only: python {sys.argv[0]} --embeddings-only")
            logging.info(f"To verify embeddings: python {sys.argv[0]} --verify-embeddings")
            logging.info(f"To verify seasonal patterns: python {sys.argv[0]} --verify-seasonal")
            
    except Exception as e:
        logging.error(f"Failed to complete operation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Check if required packages are available
    try:
        from dotenv import load_dotenv
        from faker import Faker
    except ImportError as e:
        logging.error(f"Required library not found: {e}")
        logging.error("Please install required packages with: pip install -r requirements_postgres.txt")
        exit(1)
    
    asyncio.run(main())


# =============================================================================
# ROW LEVEL SECURITY HELPER FUNCTIONS FOR WORKSHOP/DEMO
# =============================================================================

async def demo_row_level_security():
    """
    Demonstration function showing how Row Level Security works with store managers.
    
    This function shows how to:
    1. Set a manager context
    2. Query data that will be filtered by RLS policies
    3. Switch to a different manager and see different results
    
    Usage for workshop:
        python -c "import asyncio; from generate_zava_postgres import demo_row_level_security; asyncio.run(demo_row_level_security())"
    """
    conn = await create_connection()
    
    try:
        # Get all stores and their manager IDs
        stores_info = await conn.fetch(f"""
            SELECT store_name, rls_user_id 
            FROM {SCHEMA_NAME}.stores 
            ORDER BY store_name
        """)
        
        print("\n" + "=" * 60)
        print("ROW LEVEL SECURITY DEMONSTRATION")
        print("=" * 60)
        
        print("\nAvailable stores and their manager IDs:")
        for store in stores_info:
            print(f"  {store['store_name']}: {store['rls_user_id']}")
        
        # Demo with first two stores
        if len(stores_info) >= 2:
            store1 = stores_info[0]
            store2 = stores_info[1]
            
            print(f"\n--- Demonstrating RLS for {store1['store_name']} ---")
            await demo_manager_view(conn, store1['rls_user_id'], store1['store_name'])
            
            print(f"\n--- Demonstrating RLS for {store2['store_name']} ---")
            await demo_manager_view(conn, store2['rls_user_id'], store2['store_name'])
            
        print("\n" + "=" * 60)
        print("RLS DEMONSTRATION COMPLETE")
        print("=" * 60)
        
    finally:
        await conn.close()

async def demo_manager_view(conn, rls_user_id: str, store_name: str):
    """
    Demonstrate what a specific store manager can see with RLS enabled.
    """
    # Set the manager context
    await conn.execute("SELECT set_config('app.current_rls_user_id', $1, false)", rls_user_id)
    
    # Query orders (should only see orders from their store)
    orders = await conn.fetchval(f"""
        SELECT COUNT(*) FROM {SCHEMA_NAME}.orders
    """)
    
    # Query customers with breakdown
    direct_customers = await conn.fetchval(f"""
        SELECT COUNT(*) FROM {SCHEMA_NAME}.customers 
        WHERE primary_store_id IS NOT NULL
    """)
    
    indirect_customers = await conn.fetchval(f"""
        SELECT COUNT(*) FROM {SCHEMA_NAME}.customers 
        WHERE primary_store_id IS NULL
    """)
    
    total_customers = await conn.fetchval(f"""
        SELECT COUNT(*) FROM {SCHEMA_NAME}.customers
    """)
    
    # Query inventory (should only see their store's inventory)
    inventory_items = await conn.fetchval(f"""
        SELECT COUNT(*) FROM {SCHEMA_NAME}.inventory
    """)
    
    # Get total revenue
    total_revenue = await conn.fetchval(f"""
        SELECT COALESCE(SUM(oi.total_amount), 0)
        FROM {SCHEMA_NAME}.order_items oi
        JOIN {SCHEMA_NAME}.orders o ON oi.order_id = o.order_id
    """)
    
    print(f"  Manager ID: {rls_user_id}")
    print(f"  Store: {store_name}")
    print(f"  Visible Orders: {orders:,}")
    print(f"  Visible Customers: {total_customers:,}")
    print(f"    - Directly assigned: {direct_customers:,}")
    print(f"    - Discovered via orders: {indirect_customers:,}")
    print(f"  Visible Inventory Items: {inventory_items:,}")
    print(f"  Total Revenue: ${total_revenue:,.2f}")

async def test_customer_security():
    """
    Test the customer security model by demonstrating different access patterns.
    """
    conn = await create_connection()
    
    try:
        print("\n" + "=" * 60)
        print("CUSTOMER SECURITY MODEL TEST")
        print("=" * 60)
        
        # Get store information
        stores_info = await conn.fetch(f"""
            SELECT s.store_name, s.rls_user_id,
                   COUNT(c.customer_id) as assigned_customers
            FROM {SCHEMA_NAME}.stores s
            LEFT JOIN {SCHEMA_NAME}.customers c ON s.store_id = c.primary_store_id
            GROUP BY s.store_id, s.store_name, s.rls_user_id
            ORDER BY assigned_customers DESC
        """)
        
        print("\nCustomer assignment summary:")
        for store in stores_info:
            print(f"  {store['store_name']}: {store['assigned_customers']:,} directly assigned customers")
        
        # Test with the first store
        if stores_info:
            test_store = stores_info[0]
            print(f"\n--- Testing access for {test_store['store_name']} ---")
            
            # Set manager context
            await conn.execute("SELECT set_config('app.current_rls_user_id', $1, false)", test_store['rls_user_id'])
            
            # Test direct customer access
            direct_access = await conn.fetch(f"""
                SELECT customer_id, first_name, last_name, email, primary_store_id
                FROM {SCHEMA_NAME}.customers 
                WHERE primary_store_id IS NOT NULL
                LIMIT 3
            """)
            
            print("  Direct customer access (assigned to store):")
            for customer in direct_access:
                print(f"    - {customer['first_name']} {customer['last_name']} ({customer['email']}) - Store ID: {customer['primary_store_id']}")
            
            # Test indirect customer access (through orders)
            indirect_access = await conn.fetch(f"""
                SELECT DISTINCT c.customer_id, c.first_name, c.last_name, c.email, c.primary_store_id
                FROM {SCHEMA_NAME}.customers c
                WHERE c.primary_store_id IS NULL
                LIMIT 3
            """)
            
            if indirect_access:
                print("  Indirect customer access (discovered via orders):")
                for customer in indirect_access:
                    store_ref = customer['primary_store_id'] if customer['primary_store_id'] else "No primary store"
                    print(f"    - {customer['first_name']} {customer['last_name']} ({customer['email']}) - {store_ref}")
            else:
                print("  No indirect customers visible (haven't ordered from this store)")
            
            # Test with a different manager
            if len(stores_info) > 1:
                other_store = stores_info[1]
                print(f"\n--- Switching to {other_store['store_name']} ---")
                await conn.execute("SELECT set_config('app.current_rls_user_id', $1, false)", other_store['rls_user_id'])
                
                visible_customers = await conn.fetchval(f"SELECT COUNT(*) FROM {SCHEMA_NAME}.customers")
                print(f"  Customers visible to {other_store['store_name']} manager: {visible_customers:,}")
        
        print("\n" + "=" * 60)
        print("CUSTOMER SECURITY TEST COMPLETE")
        print("=" * 60)
        
    finally:
        await conn.close()

async def set_manager_context(rls_user_id: str):
    """
    Helper function to set the manager context for RLS.
    
    Usage in your application:
        await set_manager_context("12345678-1234-1234-1234-123456789012")
    """
    conn = await create_connection()
    try:
        await conn.execute("SELECT set_config('app.current_rls_user_id', $1, false)", rls_user_id)
        print(f"Manager context set to: {rls_user_id}")
    finally:
        await conn.close()

async def get_manager_ids():
    """
    Helper function to get all manager IDs for workshop use.
    
    Returns a dictionary mapping store names to manager IDs.
    """
    conn = await create_connection()
    try:
        stores = await conn.fetch(f"""
            SELECT store_name, rls_user_id::text as rls_user_id
            FROM {SCHEMA_NAME}.stores 
            ORDER BY store_name
        """)
        return {store['store_name']: store['rls_user_id'] for store in stores}
    finally:
        await conn.close()


# Workshop example usage:
#
# 1. Get manager IDs:
#    manager_ids = asyncio.run(get_manager_ids())
#    print(manager_ids)
#
# 2. Demo RLS:
#    asyncio.run(demo_row_level_security())
#
# 3. Set context in your app:
#    asyncio.run(set_manager_context("your-manager-id-here"))
#
# 4. Then all subsequent queries will be filtered by RLS policies
