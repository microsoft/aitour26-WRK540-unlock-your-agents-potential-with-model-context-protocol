"""
Customer Sales Database Generator for Microsoft SQL Server

This script generates a comprehensive customer sales database with optimized indexing
and product embeddings support for Microsoft SQL Server.

DATA FILE STRUCTURE:
- product_data.json: Contains all product information (main_categories with products)
- reference_data.json: Contains store configurations (weights, year weights)

SQL SERVER CONNECTION:
- Requires Microsoft SQL Server 2019+ 
- Uses pyodbc for connections
- Targets retail schema in zava database

FEATURES:
- Complete database generation with customers, products, stores, orders
- Product image embeddings population from product_data.json
- Product description embeddings population from product_data.json
- Performance-optimized indexes
- Row Level Security (RLS) with security policies
- Comprehensive statistics and verification
- Note: Vector embeddings use VARBINARY format (SQL Server 2022+ VECTOR support available)

USAGE:
    python generate_zava_sql_server.py                     # Generate complete database
    python generate_zava_sql_server.py --show-stats        # Show database statistics
    python generate_zava_sql_server.py --embeddings-only   # Populate embeddings only
    python generate_zava_sql_server.py --verify-embeddings # Verify embeddings tables
    python generate_zava_sql_server.py --help              # Show all options
"""

import argparse
import json
import logging
import os
import pickle
import random
import sys
from datetime import date
from typing import Dict, List, Optional, Tuple

import pyodbc
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

# SQL Server connection configuration
SQL_SERVER_CONFIG = {
    'server': 'localhost',  # Host machine IP address
    'database': 'zava',
    'driver': '{ODBC Driver 17 for SQL Server}',
    'trusted_connection': 'yes',  # Use Windows authentication
    # For SQL Server authentication, use:
    # 'uid': 'your_username',
    # 'pwd': 'your_password',
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

def create_connection():
    """Create SQL Server connection"""
    try:
        # Build connection string
        conn_str = (
            f"DRIVER={SQL_SERVER_CONFIG['driver']};"
            f"SERVER={SQL_SERVER_CONFIG['server']};"
            f"DATABASE={SQL_SERVER_CONFIG['database']};"
        )
        
        # Add authentication
        if 'trusted_connection' in SQL_SERVER_CONFIG:
            conn_str += f"Trusted_Connection={SQL_SERVER_CONFIG['trusted_connection']};"
        else:
            conn_str += f"UID={SQL_SERVER_CONFIG['uid']};PWD={SQL_SERVER_CONFIG['pwd']};"
        
        conn = pyodbc.connect(conn_str)
        logging.info(f"Connected to SQL Server at {SQL_SERVER_CONFIG['server']}")
        return conn
    except Exception as e:
        logging.error(f"Failed to connect to SQL Server: {e}")
        raise

def create_database_schema(conn):
    """Create database schema, tables and indexes"""
    try:
        cursor = conn.cursor()
        
        # Create schema if it doesn't exist
        cursor.execute(f"""
            IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = N'{SCHEMA_NAME}')
            BEGIN
                EXEC('CREATE SCHEMA [{SCHEMA_NAME}]')
            END
        """)
        logging.info(f"Schema '{SCHEMA_NAME}' created or already exists")
        
        # Create stores table
        cursor.execute(f"""
            IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{SCHEMA_NAME}' AND TABLE_NAME = 'stores')
            CREATE TABLE {SCHEMA_NAME}.stores (
                store_id INT IDENTITY(1,1) PRIMARY KEY,
                store_name NVARCHAR(255) UNIQUE NOT NULL,
                rls_user_id UNIQUEIDENTIFIER NOT NULL,
                is_online BIT NOT NULL DEFAULT 0
            )
        """)
        
        # Create customers table
        cursor.execute(f"""
            IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{SCHEMA_NAME}' AND TABLE_NAME = 'customers')
            CREATE TABLE {SCHEMA_NAME}.customers (
                customer_id INT IDENTITY(1,1) PRIMARY KEY,
                first_name NVARCHAR(255) NOT NULL,
                last_name NVARCHAR(255) NOT NULL,
                email NVARCHAR(255) UNIQUE NOT NULL,
                phone NVARCHAR(50),
                primary_store_id INT,
                created_at DATETIME2 DEFAULT GETDATE(),
                FOREIGN KEY (primary_store_id) REFERENCES {SCHEMA_NAME}.stores (store_id)
            )
        """)
        
        # Create categories table
        cursor.execute(f"""
            IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{SCHEMA_NAME}' AND TABLE_NAME = 'categories')
            CREATE TABLE {SCHEMA_NAME}.categories (
                category_id INT IDENTITY(1,1) PRIMARY KEY,
                category_name NVARCHAR(255) NOT NULL UNIQUE
            )
        """)
        
        # Create product_types table
        cursor.execute(f"""
            IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{SCHEMA_NAME}' AND TABLE_NAME = 'product_types')
            CREATE TABLE {SCHEMA_NAME}.product_types (
                type_id INT IDENTITY(1,1) PRIMARY KEY,
                category_id INT NOT NULL,
                type_name NVARCHAR(255) NOT NULL,
                FOREIGN KEY (category_id) REFERENCES {SCHEMA_NAME}.categories (category_id)
            )
        """)
        
        # Create products table with cost and selling price for 33% gross margin
        cursor.execute(f"""
            IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{SCHEMA_NAME}' AND TABLE_NAME = 'products')
            CREATE TABLE {SCHEMA_NAME}.products (
                product_id INT IDENTITY(1,1) PRIMARY KEY,
                sku NVARCHAR(100) UNIQUE NOT NULL,
                product_name NVARCHAR(500) NOT NULL,
                category_id INT NOT NULL,
                type_id INT NOT NULL,
                cost DECIMAL(10,2) NOT NULL,
                base_price DECIMAL(10,2) NOT NULL,
                gross_margin_percent DECIMAL(5,2) DEFAULT 33.00,
                product_description NVARCHAR(MAX) NOT NULL,
                FOREIGN KEY (category_id) REFERENCES {SCHEMA_NAME}.categories (category_id),
                FOREIGN KEY (type_id) REFERENCES {SCHEMA_NAME}.product_types (type_id)
            )
        """)
        
        # Create inventory table
        cursor.execute(f"""
            IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{SCHEMA_NAME}' AND TABLE_NAME = 'inventory')
            CREATE TABLE {SCHEMA_NAME}.inventory (
                store_id INT NOT NULL,
                product_id INT NOT NULL,
                stock_level INT NOT NULL,
                PRIMARY KEY (store_id, product_id),
                FOREIGN KEY (store_id) REFERENCES {SCHEMA_NAME}.stores (store_id),
                FOREIGN KEY (product_id) REFERENCES {SCHEMA_NAME}.products (product_id)
            )
        """)
        
        # Create orders table (header only)
        cursor.execute(f"""
            IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{SCHEMA_NAME}' AND TABLE_NAME = 'orders')
            CREATE TABLE {SCHEMA_NAME}.orders (
                order_id INT IDENTITY(1,1) PRIMARY KEY,
                customer_id INT NOT NULL,
                store_id INT NOT NULL,
                order_date DATE NOT NULL,
                FOREIGN KEY (customer_id) REFERENCES {SCHEMA_NAME}.customers (customer_id),
                FOREIGN KEY (store_id) REFERENCES {SCHEMA_NAME}.stores (store_id)
            )
        """)
        
        # Create order_items table (line items)
        cursor.execute(f"""
            IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{SCHEMA_NAME}' AND TABLE_NAME = 'order_items')
            CREATE TABLE {SCHEMA_NAME}.order_items (
                order_item_id INT IDENTITY(1,1) PRIMARY KEY,
                order_id INT NOT NULL,
                store_id INT NOT NULL,
                product_id INT NOT NULL,
                quantity INT NOT NULL,
                unit_price DECIMAL(10,2) NOT NULL,
                discount_percent INT DEFAULT 0,
                discount_amount DECIMAL(10,2) DEFAULT 0,
                total_amount DECIMAL(10,2) NOT NULL,
                FOREIGN KEY (order_id) REFERENCES {SCHEMA_NAME}.orders (order_id),
                FOREIGN KEY (store_id) REFERENCES {SCHEMA_NAME}.stores (store_id),
                FOREIGN KEY (product_id) REFERENCES {SCHEMA_NAME}.products (product_id)
            )
        """)
        
        # Create product_image_embeddings table for image data
        # Note: SQL Server 2022+ supports VECTOR type, for earlier versions use VARBINARY(MAX)
        cursor.execute(f"""
            IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{SCHEMA_NAME}' AND TABLE_NAME = 'product_image_embeddings')
            CREATE TABLE {SCHEMA_NAME}.product_image_embeddings (
                product_id INT PRIMARY KEY,
                image_url NVARCHAR(500) NOT NULL,
                image_embedding VARBINARY(MAX), -- For SQL Server 2022+ use: VECTOR(512)
                created_at DATETIME2 DEFAULT GETDATE(),
                FOREIGN KEY (product_id) REFERENCES {SCHEMA_NAME}.products (product_id)
            )
        """)
        
        # Create product_description_embeddings table for text embeddings
        cursor.execute(f"""
            IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{SCHEMA_NAME}' AND TABLE_NAME = 'product_description_embeddings')
            CREATE TABLE {SCHEMA_NAME}.product_description_embeddings (
                product_id INT PRIMARY KEY,
                description_embedding VARBINARY(MAX), -- For SQL Server 2022+ use: VECTOR(1536)
                created_at DATETIME2 DEFAULT GETDATE(),
                FOREIGN KEY (product_id) REFERENCES {SCHEMA_NAME}.products (product_id)
            )
        """)
        
        conn.commit()
        logging.info("Database tables created successfully!")
        
        # Create performance indexes
        create_indexes(conn)
        
        # Note: Row Level Security setup removed for compatibility
        logging.info("Skipping Row Level Security setup for compatibility")
        
        logging.info("Database schema created successfully!")
    except Exception as e:
        logging.error(f"Error creating database schema: {e}")
        conn.rollback()
        raise

def create_indexes(conn):
    """Create performance indexes for SQL Server"""
    try:
        cursor = conn.cursor()
        logging.info("Creating performance indexes...")
        
        # Helper function to create index if it doesn't exist
        def create_index_if_not_exists(index_name, table_name, columns):
            try:
                cursor.execute(f"""
                    IF NOT EXISTS (SELECT name FROM sys.indexes WHERE name = N'{index_name}')
                    CREATE INDEX {index_name} ON {SCHEMA_NAME}.{table_name} ({columns})
                """)
            except Exception as e:
                logging.warning(f"Could not create index {index_name}: {e}")
        
        # Category and type indexes
        create_index_if_not_exists('idx_categories_name', 'categories', 'category_name')
        create_index_if_not_exists('idx_product_types_category', 'product_types', 'category_id')
        create_index_if_not_exists('idx_product_types_name', 'product_types', 'type_name')
        
        # Product indexes
        create_index_if_not_exists('idx_products_sku', 'products', 'sku')
        create_index_if_not_exists('idx_products_category', 'products', 'category_id')
        create_index_if_not_exists('idx_products_type', 'products', 'type_id')
        create_index_if_not_exists('idx_products_price', 'products', 'base_price')
        create_index_if_not_exists('idx_products_cost', 'products', 'cost')
        create_index_if_not_exists('idx_products_margin', 'products', 'gross_margin_percent')
        
        # Inventory indexes
        create_index_if_not_exists('idx_inventory_product', 'inventory', 'product_id')
        create_index_if_not_exists('idx_inventory_store', 'inventory', 'store_id')
        
        # Store indexes
        create_index_if_not_exists('idx_stores_name', 'stores', 'store_name')
        
        # Order indexes
        create_index_if_not_exists('idx_orders_customer', 'orders', 'customer_id')
        create_index_if_not_exists('idx_orders_store', 'orders', 'store_id')
        create_index_if_not_exists('idx_orders_date', 'orders', 'order_date')
        create_index_if_not_exists('idx_orders_customer_date', 'orders', 'customer_id, order_date')
        create_index_if_not_exists('idx_orders_store_date', 'orders', 'store_id, order_date')
        
        # Order items indexes
        create_index_if_not_exists('idx_order_items_order', 'order_items', 'order_id')
        create_index_if_not_exists('idx_order_items_store', 'order_items', 'store_id')
        create_index_if_not_exists('idx_order_items_product', 'order_items', 'product_id')
        create_index_if_not_exists('idx_order_items_total', 'order_items', 'total_amount')
        
        # Product image embeddings indexes
        create_index_if_not_exists('idx_product_image_embeddings_url', 'product_image_embeddings', 'image_url')
        
        # Covering indexes for aggregation queries
        create_index_if_not_exists('idx_order_items_covering', 'order_items', 'order_id, store_id, product_id, total_amount, quantity')
        create_index_if_not_exists('idx_products_covering', 'products', 'category_id, type_id, product_id, sku, cost, base_price')
        create_index_if_not_exists('idx_products_sku_covering', 'products', 'sku, product_id, product_name, cost, base_price')
        
        # Customer indexes
        create_index_if_not_exists('idx_customers_email', 'customers', 'email')
        create_index_if_not_exists('idx_customers_primary_store', 'customers', 'primary_store_id')
        
        conn.commit()
        logging.info("Performance indexes created successfully!")
    except Exception as e:
        logging.error(f"Error creating indexes: {e}")
        conn.rollback()
        raise

def setup_row_level_security(conn):
    """Setup Row Level Security for SQL Server"""
    try:
        cursor = conn.cursor()
        logging.info("Setting up Row Level Security policies...")
        logging.info(f"Super Manager UUID (access to all rows): {SUPER_MANAGER_UUID}")
        
        # Enable RLS on tables that should be restricted by store manager
        cursor.execute(f"ALTER TABLE {SCHEMA_NAME}.orders ENABLE ROW LEVEL SECURITY")
        cursor.execute(f"ALTER TABLE {SCHEMA_NAME}.order_items ENABLE ROW LEVEL SECURITY")
        cursor.execute(f"ALTER TABLE {SCHEMA_NAME}.inventory ENABLE ROW LEVEL SECURITY")
        cursor.execute(f"ALTER TABLE {SCHEMA_NAME}.customers ENABLE ROW LEVEL SECURITY")
        
        # Create security function for RLS
        cursor.execute(f"""
            CREATE OR ALTER FUNCTION {SCHEMA_NAME}.fn_securitypredicate(@store_id INT)
            RETURNS TABLE
            WITH SCHEMABINDING
            AS
            RETURN SELECT 1 AS fn_securitypredicate_result
            WHERE 
                SESSION_CONTEXT(N'rls_user_id') = '{SUPER_MANAGER_UUID}'
                OR EXISTS (
                    SELECT 1 FROM {SCHEMA_NAME}.stores s 
                    WHERE s.store_id = @store_id 
                    AND CAST(s.rls_user_id AS NVARCHAR(36)) = SESSION_CONTEXT(N'rls_user_id')
                )
        """)
        
        # Create security policies for orders
        cursor.execute(f"""
            IF EXISTS (SELECT * FROM sys.security_policies WHERE name = N'store_manager_orders_policy')
                DROP SECURITY POLICY {SCHEMA_NAME}.store_manager_orders_policy
        """)
        cursor.execute(f"""
            CREATE SECURITY POLICY {SCHEMA_NAME}.store_manager_orders_policy
            ADD FILTER PREDICATE {SCHEMA_NAME}.fn_securitypredicate(store_id) ON {SCHEMA_NAME}.orders,
            ADD BLOCK PREDICATE {SCHEMA_NAME}.fn_securitypredicate(store_id) ON {SCHEMA_NAME}.orders AFTER INSERT,
            ADD BLOCK PREDICATE {SCHEMA_NAME}.fn_securitypredicate(store_id) ON {SCHEMA_NAME}.orders AFTER UPDATE
            WITH (STATE = ON)
        """)
        
        # Create security policies for order_items
        cursor.execute(f"""
            IF EXISTS (SELECT * FROM sys.security_policies WHERE name = N'store_manager_order_items_policy')
                DROP SECURITY POLICY {SCHEMA_NAME}.store_manager_order_items_policy
        """)
        cursor.execute(f"""
            CREATE SECURITY POLICY {SCHEMA_NAME}.store_manager_order_items_policy
            ADD FILTER PREDICATE {SCHEMA_NAME}.fn_securitypredicate(store_id) ON {SCHEMA_NAME}.order_items,
            ADD BLOCK PREDICATE {SCHEMA_NAME}.fn_securitypredicate(store_id) ON {SCHEMA_NAME}.order_items AFTER INSERT,
            ADD BLOCK PREDICATE {SCHEMA_NAME}.fn_securitypredicate(store_id) ON {SCHEMA_NAME}.order_items AFTER UPDATE
            WITH (STATE = ON)
        """)
        
        # Create security policies for inventory
        cursor.execute(f"""
            IF EXISTS (SELECT * FROM sys.security_policies WHERE name = N'store_manager_inventory_policy')
                DROP SECURITY POLICY {SCHEMA_NAME}.store_manager_inventory_policy
        """)
        cursor.execute(f"""
            CREATE SECURITY POLICY {SCHEMA_NAME}.store_manager_inventory_policy
            ADD FILTER PREDICATE {SCHEMA_NAME}.fn_securitypredicate(store_id) ON {SCHEMA_NAME}.inventory,
            ADD BLOCK PREDICATE {SCHEMA_NAME}.fn_securitypredicate(store_id) ON {SCHEMA_NAME}.inventory AFTER INSERT,
            ADD BLOCK PREDICATE {SCHEMA_NAME}.fn_securitypredicate(store_id) ON {SCHEMA_NAME}.inventory AFTER UPDATE
            WITH (STATE = ON)
        """)
        
        # Create customer security function (different logic for customers)
        cursor.execute(f"""
            CREATE OR ALTER FUNCTION {SCHEMA_NAME}.fn_customer_securitypredicate(@primary_store_id INT)
            RETURNS TABLE
            WITH SCHEMABINDING
            AS
            RETURN SELECT 1 AS fn_securitypredicate_result
            WHERE 
                SESSION_CONTEXT(N'rls_user_id') = '{SUPER_MANAGER_UUID}'
                OR EXISTS (
                    SELECT 1 FROM {SCHEMA_NAME}.stores s 
                    WHERE s.store_id = @primary_store_id 
                    AND CAST(s.rls_user_id AS NVARCHAR(36)) = SESSION_CONTEXT(N'rls_user_id')
                )
        """)
        
        # Create security policies for customers
        cursor.execute(f"""
            IF EXISTS (SELECT * FROM sys.security_policies WHERE name = N'store_manager_customers_policy')
                DROP SECURITY POLICY {SCHEMA_NAME}.store_manager_customers_policy
        """)
        cursor.execute(f"""
            CREATE SECURITY POLICY {SCHEMA_NAME}.store_manager_customers_policy
            ADD FILTER PREDICATE {SCHEMA_NAME}.fn_customer_securitypredicate(primary_store_id) ON {SCHEMA_NAME}.customers,
            ADD BLOCK PREDICATE {SCHEMA_NAME}.fn_customer_securitypredicate(primary_store_id) ON {SCHEMA_NAME}.customers AFTER INSERT,
            ADD BLOCK PREDICATE {SCHEMA_NAME}.fn_customer_securitypredicate(primary_store_id) ON {SCHEMA_NAME}.customers AFTER UPDATE
            WITH (STATE = ON)
        """)
        
        conn.commit()
        logging.info("Row Level Security policies created successfully!")
    except Exception as e:
        logging.error(f"Error setting up Row Level Security: {e}")
        conn.rollback()
        raise

def setup_store_manager_permissions(conn):
    """Setup permissions for store_manager user to access the retail schema and tables"""
    try:
        cursor = conn.cursor()
        logging.info("Setting up store_manager permissions...")
        
        # Check if store_manager login exists, create if it doesn't
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sys.server_principals WHERE name = 'store_manager')
            BEGIN
                CREATE LOGIN store_manager WITH PASSWORD = 'StoreManager123!', CHECK_POLICY = OFF
            END
        """)
        
        # Check if store_manager user exists in database, create if it doesn't
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sys.database_principals WHERE name = 'store_manager')
            BEGIN
                CREATE USER store_manager FOR LOGIN store_manager
            END
        """)
        
        # Grant permissions on the retail schema
        cursor.execute(f"GRANT SELECT, INSERT, UPDATE, DELETE ON SCHEMA::{SCHEMA_NAME} TO store_manager")
        
        # Grant execute permissions on security functions
        cursor.execute(f"GRANT SELECT ON {SCHEMA_NAME}.fn_securitypredicate TO store_manager")
        cursor.execute(f"GRANT SELECT ON {SCHEMA_NAME}.fn_customer_securitypredicate TO store_manager")
        
        conn.commit()
        logging.info("Store manager permissions granted successfully!")
        logging.info("Store manager can now:")
        logging.info("  - Access the retail schema")
        logging.info("  - SELECT, INSERT, UPDATE, DELETE on all tables")
        logging.info("  - Row Level Security policies will filter data based on rls_user_id")
        
    except Exception as e:
        logging.error(f"Error setting up store_manager permissions: {e}")
        conn.rollback()
        raise

def batch_insert(conn, query: str, data: List[Tuple], batch_size: int = 1000):
    """Insert data in batches using pyodbc"""
    cursor = conn.cursor()
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        cursor.executemany(query, batch)
    conn.commit()

def insert_customers(conn, num_customers: int = 100000):
    """Insert customer data into the database"""
    try:
        logging.info(f"Generating {num_customers:,} customers...")
        
        # Get store IDs for assignment
        cursor = conn.cursor()
        cursor.execute(f"SELECT store_id, store_name FROM {SCHEMA_NAME}.stores")
        store_rows = cursor.fetchall()
        
        if not store_rows:
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
                if row[1] == preferred_store_name:  # row[1] is store_name
                    primary_store_id = row[0]  # row[0] is store_id
                    break
            
            # Fallback to first store if lookup fails (should not happen)
            if primary_store_id is None:
                primary_store_id = store_rows[0][0]
            
            customers_data.append((first_name, last_name, email, phone, primary_store_id))
        
        batch_insert(conn, f"INSERT INTO {SCHEMA_NAME}.customers (first_name, last_name, email, phone, primary_store_id) VALUES (?, ?, ?, ?, ?)", customers_data)
        
        # Log customer distribution by store
        cursor.execute(f"""
            SELECT s.store_name, COUNT(c.customer_id) as customer_count,
                   ROUND(100.0 * COUNT(c.customer_id) / {num_customers}, 1) as percentage
            FROM {SCHEMA_NAME}.stores s
            LEFT JOIN {SCHEMA_NAME}.customers c ON s.store_id = c.primary_store_id
            GROUP BY s.store_id, s.store_name
            ORDER BY customer_count DESC
        """)
        distribution = cursor.fetchall()
        
        cursor.execute(f"SELECT COUNT(*) FROM {SCHEMA_NAME}.customers WHERE primary_store_id IS NULL")
        no_store_count = cursor.fetchone()[0]
        
        logging.info("Customer distribution by store:")
        for row in distribution:
            logging.info(f"  {row[0]}: {row[1]:,} customers ({row[2]}%)")
        if no_store_count > 0:
            logging.info(f"  No primary store: {no_store_count:,} customers ({100.0 * no_store_count / num_customers:.1f}%)")
        else:
            logging.info("  ✅ All customers have been assigned to stores!")
        
        logging.info(f"Successfully inserted {num_customers:,} customers!")
    except Exception as e:
        logging.error(f"Error inserting customers: {e}")
        raise

def insert_stores(conn):
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
        
        batch_insert(conn, f"INSERT INTO {SCHEMA_NAME}.stores (store_name, rls_user_id, is_online) VALUES (?, ?, ?)", stores_data)
        
        # Log the manager IDs for workshop purposes
        cursor = conn.cursor()
        cursor.execute(f"SELECT store_name, rls_user_id FROM {SCHEMA_NAME}.stores ORDER BY store_name")
        rows = cursor.fetchall()
        logging.info("Store Manager IDs (for workshop use):")
        for row in rows:
            logging.info(f"  {row[0]}: {row[1]}")
        
        logging.info(f"Successfully inserted {len(stores_data):,} stores!")
    except Exception as e:
        logging.error(f"Error inserting stores: {e}")
        raise

def insert_categories(conn):
    """Insert category data into the database"""
    try:
        logging.info("Generating categories...")
        
        categories_data = []
        
        # Extract unique categories from product data
        for main_category in main_categories:
            categories_data.append((main_category,))
        
        batch_insert(conn, f"INSERT INTO {SCHEMA_NAME}.categories (category_name) VALUES (?)", categories_data)
        
        logging.info(f"Successfully inserted {len(categories_data):,} categories!")
    except Exception as e:
        logging.error(f"Error inserting categories: {e}")
        raise

def insert_product_types(conn):
    """Insert product type data into the database"""
    try:
        logging.info("Generating product types...")
        
        product_types_data = []
        
        # Get category_id mapping
        cursor = conn.cursor()
        cursor.execute(f"SELECT category_id, category_name FROM {SCHEMA_NAME}.categories")
        category_rows = cursor.fetchall()
        category_mapping = {}
        for row in category_rows:
            category_mapping[row[1]] = row[0]  # row[1] is category_name, row[0] is category_id
        
        # Extract product types for each category
        for main_category, subcategories in main_categories.items():
            category_id = category_mapping[main_category]
            for subcategory in subcategories:
                # Skip the seasonal multipliers key
                if subcategory == 'washington_seasonal_multipliers':
                    continue
                
                product_types_data.append((category_id, subcategory))
        
        batch_insert(conn, f"INSERT INTO {SCHEMA_NAME}.product_types (category_id, type_name) VALUES (?, ?)", product_types_data)
        
        logging.info(f"Successfully inserted {len(product_types_data):,} product types!")
    except Exception as e:
        logging.error(f"Error inserting product types: {e}")
        raise

def insert_products(conn):
    """Insert product data into the database"""
    try:
        logging.info("Generating products...")
        
        # Get category and type mappings
        cursor = conn.cursor()
        cursor.execute(f"SELECT category_id, category_name FROM {SCHEMA_NAME}.categories")
        category_rows = cursor.fetchall()
        category_mapping = {}
        for row in category_rows:
            category_mapping[row[1]] = row[0]  # row[1] is category_name, row[0] is category_id
        
        cursor.execute(f"SELECT type_id, type_name, category_id FROM {SCHEMA_NAME}.product_types")
        type_rows = cursor.fetchall()
        type_mapping = {}
        for row in type_rows:
            type_mapping[(row[2], row[1])] = row[0]  # (category_id, type_name) -> type_id
        
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
        
        batch_insert(conn, f"INSERT INTO {SCHEMA_NAME}.products (sku, product_name, category_id, type_id, cost, base_price, product_description) VALUES (?, ?, ?, ?, ?, ?, ?)", products_data)
        
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

def get_store_id_by_name(conn, store_name):
    """Get store_id for a given store name"""
    cursor = conn.cursor()
    cursor.execute(f"SELECT store_id FROM {SCHEMA_NAME}.stores WHERE store_name = ?", (store_name,))
    row = cursor.fetchone()
    return row[0] if row else 1  # Default to store_id 1 if not found

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

def get_product_id_by_sku(conn, sku: str) -> Optional[int]:
    """Get product_id for a given SKU"""
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT product_id FROM {SCHEMA_NAME}.products WHERE sku = ?", (sku,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        logging.error(f"Error getting product_id for SKU {sku}: {e}")
        return None

def insert_product_embedding(
    conn, 
    product_id: int, 
    image_path: str, 
    image_embedding: List[float]
) -> bool:
    """Insert a product embedding record"""
    try:
        cursor = conn.cursor()
        # Store just the image filename without any path prefix
        image_url = os.path.basename(image_path)
        
        # Convert the embedding list to a binary format for SQL Server
        # Note: SQL Server 2022+ supports VECTOR type, for earlier versions use VARBINARY
        embedding_bytes = pickle.dumps(image_embedding)
        
        cursor.execute(f"""
            INSERT INTO {SCHEMA_NAME}.product_image_embeddings 
            (product_id, image_url, image_embedding) 
            VALUES (?, ?, ?)
        """, (product_id, image_url, embedding_bytes))
        conn.commit()
        return True
    except Exception as e:
        logging.error(f"Error inserting embedding for product_id {product_id}: {e}")
        return False

def clear_existing_embeddings(conn) -> None:
    """Clear all existing product image embeddings"""
    try:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {SCHEMA_NAME}.product_image_embeddings")
        result = cursor.rowcount
        conn.commit()
        logging.info(f"Cleared existing embeddings: {result} rows deleted")
    except Exception as e:
        logging.error(f"Error clearing existing embeddings: {e}")
        raise

def populate_product_image_embeddings(conn, clear_existing: bool = False, batch_size: int = 100) -> None:
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
            clear_existing_embeddings(conn)
        
        # Process products in batches
        inserted_count = 0
        skipped_count = 0
        error_count = 0
        
        for i in range(0, len(products_with_embeddings), batch_size):
            batch = products_with_embeddings[i:i + batch_size]
            
            logging.info(f"Processing embeddings batch {i//batch_size + 1}/{(len(products_with_embeddings) + batch_size - 1)//batch_size}")
            
            for sku, image_path, image_embedding in batch:
                # Get product_id for this SKU
                product_id = get_product_id_by_sku(conn, sku)
                
                if product_id is None:
                    logging.debug(f"Product not found for SKU: {sku}")
                    skipped_count += 1
                    continue
                
                # Insert the embedding
                if insert_product_embedding(conn, product_id, image_path, image_embedding):
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

def verify_embeddings_table(conn) -> None:
    """Verify the product_image_embeddings table exists and show sample data"""
    try:
        cursor = conn.cursor()
        
        # Check table existence
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = ? AND TABLE_NAME = 'product_image_embeddings'
        """, (SCHEMA_NAME,))
        table_exists = cursor.fetchone()[0] > 0
        
        if not table_exists:
            logging.error(f"Table {SCHEMA_NAME}.product_image_embeddings does not exist!")
            return
        
        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM {SCHEMA_NAME}.product_image_embeddings")
        count = cursor.fetchone()[0]
        logging.info(f"Product image embeddings table has {count} records")
        
        # Show sample data
        if count > 0:
            cursor.execute(f"""
                SELECT TOP 5 pe.product_id, p.sku, p.product_name, pe.image_url,
                       LEN(pe.image_embedding) as embedding_size
                FROM {SCHEMA_NAME}.product_image_embeddings pe
                JOIN {SCHEMA_NAME}.products p ON pe.product_id = p.product_id
            """)
            sample = cursor.fetchall()
            
            logging.info("Sample embeddings data:")
            for row in sample:
                logging.info(f"  Product ID: {row[0]}, SKU: {row[1]}, "
                           f"Product: {row[2][:50]}..., "
                           f"Embedding size: {row[4]} bytes")
        
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

def insert_product_description_embedding(
    conn, 
    product_id: int, 
    description_embedding: List[float]
) -> bool:
    """Insert a product description embedding record"""
    try:
        cursor = conn.cursor()
        # Convert the embedding list to binary format for SQL Server
        embedding_bytes = pickle.dumps(description_embedding)
        
        cursor.execute(f"""
            INSERT INTO {SCHEMA_NAME}.product_description_embeddings 
            (product_id, description_embedding) 
            VALUES (?, ?)
        """, (product_id, embedding_bytes))
        conn.commit()
        return True
    except Exception as e:
        logging.error(f"Error inserting description embedding for product_id {product_id}: {e}")
        return False

def clear_existing_description_embeddings(conn) -> None:
    """Clear all existing product description embeddings"""
    try:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {SCHEMA_NAME}.product_description_embeddings")
        result = cursor.rowcount
        conn.commit()
        logging.info(f"Cleared existing description embeddings: {result} rows deleted")
    except Exception as e:
        logging.error(f"Error clearing existing description embeddings: {e}")
        raise

def populate_product_description_embeddings(conn, clear_existing: bool = False, batch_size: int = 100) -> None:
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
            clear_existing_description_embeddings(conn)
        
        # Process products in batches
        inserted_count = 0
        skipped_count = 0
        error_count = 0
        
        for i in range(0, len(products_with_description_embeddings), batch_size):
            batch = products_with_description_embeddings[i:i + batch_size]
            
            logging.info(f"Processing description embeddings batch {i//batch_size + 1}/{(len(products_with_description_embeddings) + batch_size - 1)//batch_size}")
            
            for sku, description_embedding in batch:
                # Get product_id for this SKU
                product_id = get_product_id_by_sku(conn, sku)
                
                if product_id is None:
                    logging.debug(f"Product not found for SKU: {sku}")
                    skipped_count += 1
                    continue
                
                # Insert the description embedding
                if insert_product_description_embedding(conn, product_id, description_embedding):
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

def verify_description_embeddings_table(conn) -> None:
    """Verify the product_description_embeddings table exists and show sample data"""
    try:
        cursor = conn.cursor()
        
        # Check table existence
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = ? AND TABLE_NAME = 'product_description_embeddings'
        """, (SCHEMA_NAME,))
        table_exists = cursor.fetchone()[0] > 0
        
        if not table_exists:
            logging.error(f"Table {SCHEMA_NAME}.product_description_embeddings does not exist!")
            return
        
        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM {SCHEMA_NAME}.product_description_embeddings")
        count = cursor.fetchone()[0]
        logging.info(f"Product description embeddings table has {count} records")
        
        # Show sample data
        if count > 0:
            cursor.execute(f"""
                SELECT TOP 5 pe.product_id, p.sku, p.product_name,
                       LEN(pe.description_embedding) as embedding_size
                FROM {SCHEMA_NAME}.product_description_embeddings pe
                JOIN {SCHEMA_NAME}.products p ON pe.product_id = p.product_id
            """)
            sample = cursor.fetchall()
            
            logging.info("Sample description embeddings data:")
            for row in sample:
                logging.info(f"  Product ID: {row[0]}, SKU: {row[1]}, "
                           f"Product: {row[2][:50]}..., "
                           f"Embedding size: {row[3]} bytes")
        
    except Exception as e:
        logging.error(f"Error verifying description embeddings table: {e}")

def insert_inventory(conn):
    """Insert inventory data distributed across stores based on customer distribution weights and seasonal trends"""
    try:
        logging.info("Generating inventory with seasonal considerations...")
        
        cursor = conn.cursor()
        
        # Get all stores and products with category information
        cursor.execute(f"SELECT store_id, store_name FROM {SCHEMA_NAME}.stores")
        stores_data = cursor.fetchall()
        
        cursor.execute(f"""
            SELECT p.product_id, c.category_name 
            FROM {SCHEMA_NAME}.products p
            JOIN {SCHEMA_NAME}.categories c ON p.category_id = c.category_id
        """)
        products_data = cursor.fetchall()
        
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
            store_id = store[0]  # store_id
            store_name = store[1]  # store_name
            
            # Get store configuration for inventory distribution
            store_config = stores.get(store_name, {})
            base_stock_multiplier = store_config.get('customer_distribution_weight', 1.0)
            
            for product in products_data:
                product_id = product[0]  # product_id
                category_name = product[1]  # category_name
                
                # Get seasonal multiplier for this category
                seasonal_multiplier = category_seasonal_avg.get(category_name, 1.0)
                
                # Generate stock level based on store weight, seasonal trends, and random variation
                base_stock = random.randint(10, 100)
                stock_level = int(base_stock * base_stock_multiplier * seasonal_multiplier * random.uniform(0.5, 1.5))
                stock_level = max(1, stock_level)  # Ensure at least 1 item in stock
                
                inventory_data.append((store_id, product_id, stock_level))
        
        batch_insert(conn, f"INSERT INTO {SCHEMA_NAME}.inventory (store_id, product_id, stock_level) VALUES (?, ?, ?)", inventory_data)
        
        logging.info(f"Successfully inserted {len(inventory_data):,} inventory records with seasonal adjustments!")
        
    except Exception as e:
        logging.error(f"Error inserting inventory: {e}")
        raise

def build_product_lookup(conn):
    """Build a lookup table mapping (main_category, product_type, product_name) to product_id"""
    try:
        logging.info("Building product lookup table...")
        cursor = conn.cursor()
        
        # Get all products with their category and type information
        cursor.execute(f"""
            SELECT p.product_id, p.sku, p.product_name, p.base_price, p.cost,
                   c.category_name, pt.type_name
            FROM {SCHEMA_NAME}.products p
            JOIN {SCHEMA_NAME}.categories c ON p.category_id = c.category_id
            JOIN {SCHEMA_NAME}.product_types pt ON p.type_id = pt.type_id
        """)
        products = cursor.fetchall()
        
        product_lookup = {}
        
        for product in products:
            category = product[5]  # category_name
            product_type = product[6]  # type_name
            
            if category not in product_lookup:
                product_lookup[category] = {}
            
            if product_type not in product_lookup[category]:
                product_lookup[category][product_type] = []
            
            product_lookup[category][product_type].append({
                'product_id': product[0],
                'sku': product[1],
                'name': product[2],
                'price': float(product[3]),
                'cost': float(product[4])
            })
        
        logging.info(f"Built product lookup with {len(products):,} products across {len(product_lookup)} categories")
        return product_lookup
        
    except Exception as e:
        logging.error(f"Error building product lookup: {e}")
        raise

def insert_orders(conn, num_customers: int = 100000, product_lookup: Optional[Dict] = None):
    """Insert order data into the database with separate orders and order_items tables"""
    
    # Build product lookup if not provided
    if product_lookup is None:
        product_lookup = build_product_lookup(conn)
    
    logging.info(f"Generating orders for {num_customers:,} customers...")
    
    # Get available product IDs for faster random selection and build category mapping
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT p.product_id, p.cost, p.base_price, c.category_name 
        FROM {SCHEMA_NAME}.products p
        JOIN {SCHEMA_NAME}.categories c ON p.category_id = c.category_id
    """)
    product_rows = cursor.fetchall()
    
    product_prices = {row[0]: float(row[2]) for row in product_rows}  # product_id: base_price
    available_product_ids = list(product_prices.keys())
    
    # Build category to product ID mapping for seasonal selection
    category_products = {}
    for row in product_rows:
        category_name = row[3]  # category_name
        if category_name not in category_products:
            category_products[category_name] = []
        category_products[category_name].append(row[0])  # product_id
    
    logging.info(f"Built category mapping with {len(category_products)} categories")
    
    total_orders = 0
    orders_data = []
    order_items_data = []
    
    for customer_id in range(1, num_customers + 1):
        # Determine store preference for this customer
        preferred_store = weighted_store_choice()
        store_id = get_store_id_by_name(conn, preferred_store)
        
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
                batch_insert(conn, f"""
                    INSERT INTO {SCHEMA_NAME}.orders (customer_id, store_id, order_date) 
                    VALUES (?, ?, ?)
                """, orders_data)
                orders_data = []
            
            if order_items_data:
                batch_insert(conn, f"""
                    INSERT INTO {SCHEMA_NAME}.order_items 
                    (order_id, store_id, product_id, quantity, unit_price, discount_percent, discount_amount, total_amount) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, order_items_data)
                order_items_data = []
            
            if customer_id % 5000 == 0:
                logging.info(f"Processed {customer_id:,} customers, generated {total_orders:,} orders")
    
    # Insert remaining data
    if orders_data:
        batch_insert(conn, f"""
            INSERT INTO {SCHEMA_NAME}.orders (customer_id, store_id, order_date) 
            VALUES (?, ?, ?)
        """, orders_data)
    
    if order_items_data:
        batch_insert(conn, f"""
            INSERT INTO {SCHEMA_NAME}.order_items 
            (order_id, store_id, product_id, quantity, unit_price, discount_percent, discount_amount, total_amount) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, order_items_data)
    
    logging.info(f"Successfully inserted {total_orders:,} orders!")
    
    # Get order items count
    cursor.execute(f"SELECT COUNT(*) FROM {SCHEMA_NAME}.order_items")
    order_items_count = cursor.fetchone()[0]
    logging.info(f"Successfully inserted {order_items_count:,} order items!")

def verify_database_contents(conn) -> None:
    """Verify database contents and show key statistics"""
    
    logging.info("\n" + "=" * 60)
    logging.info("DATABASE VERIFICATION & STATISTICS")
    logging.info("=" * 60)
    
    cursor = conn.cursor()
    
    # Store distribution verification
    logging.info("\n🏪 STORE SALES DISTRIBUTION:")
    cursor.execute(f"""
        SELECT s.store_name, 
               COUNT(o.order_id) as orders,
               CAST(ROUND(SUM(oi.total_amount)/1000.0, 1) AS VARCHAR) + 'K' as revenue,
               CAST(ROUND(100.0 * COUNT(o.order_id) / (SELECT COUNT(*) FROM {SCHEMA_NAME}.orders), 1) AS VARCHAR) + '%' as order_pct
        FROM {SCHEMA_NAME}.orders o 
        JOIN {SCHEMA_NAME}.stores s ON o.store_id = s.store_id
        JOIN {SCHEMA_NAME}.order_items oi ON o.order_id = oi.order_id
        GROUP BY s.store_id, s.store_name
        ORDER BY SUM(oi.total_amount) DESC
    """)
    rows = cursor.fetchall()
    
    logging.info("   Store               Orders     Revenue    % of Orders")
    logging.info("   " + "-" * 50)
    for row in rows:
        logging.info(f"   {row[0]:<18} {row[1]:>6}     ${row[2]:>6}    {row[3]:>6}")
    
    # Year-over-year growth verification
    logging.info("\n📈 YEAR-OVER-YEAR GROWTH PATTERN:")
    cursor.execute(f"""
        SELECT YEAR(o.order_date) as year,
               COUNT(DISTINCT o.order_id) as orders,
               CAST(ROUND(SUM(oi.total_amount)/1000.0, 1) AS VARCHAR) + 'K' as revenue
        FROM {SCHEMA_NAME}.orders o
        JOIN {SCHEMA_NAME}.order_items oi ON o.order_id = oi.order_id
        GROUP BY YEAR(o.order_date)
        ORDER BY year
    """)
    rows = cursor.fetchall()
    
    logging.info("   Year    Orders     Revenue    Growth")
    logging.info("   " + "-" * 35)
    prev_revenue = None
    for row in rows:
        revenue_num = float(row[2].replace('K', ''))
        growth = ""
        if prev_revenue is not None:
            growth_pct = ((revenue_num - prev_revenue) / prev_revenue) * 100
            growth = f"{growth_pct:+.1f}%"
        logging.info(f"   {int(row[0])}    {row[1]:>6}     ${row[2]:>6}    {growth:>6}")
        prev_revenue = revenue_num
    
    # Product category distribution
    logging.info("\n🛍️  TOP PRODUCT CATEGORIES:")
    cursor.execute(f"""
        SELECT TOP 5 c.category_name,
               COUNT(DISTINCT o.order_id) as orders,
               CAST(ROUND(SUM(oi.total_amount)/1000.0, 1) AS VARCHAR) + 'K' as revenue
        FROM {SCHEMA_NAME}.categories c
        JOIN {SCHEMA_NAME}.products p ON c.category_id = p.category_id
        JOIN {SCHEMA_NAME}.order_items oi ON p.product_id = oi.product_id
        JOIN {SCHEMA_NAME}.orders o ON oi.order_id = o.order_id
        GROUP BY c.category_id, c.category_name
        ORDER BY SUM(oi.total_amount) DESC
    """)
    rows = cursor.fetchall()
    
    logging.info("   Category             Orders     Revenue")
    logging.info("   " + "-" * 40)
    for row in rows:
        logging.info(f"   {row[0]:<18} {row[1]:>6}     ${row[2]:>6}")
    
    # Final summary
    cursor.execute(f"SELECT COUNT(*) FROM {SCHEMA_NAME}.customers")
    customers = cursor.fetchone()[0]
    
    cursor.execute(f"SELECT COUNT(*) FROM {SCHEMA_NAME}.products")
    products = cursor.fetchone()[0]
    
    cursor.execute(f"SELECT COUNT(*) FROM {SCHEMA_NAME}.orders")
    orders = cursor.fetchone()[0]
    
    cursor.execute(f"SELECT COUNT(*) FROM {SCHEMA_NAME}.order_items")
    order_items = cursor.fetchone()[0]
    
    cursor.execute(f"SELECT SUM(total_amount) FROM {SCHEMA_NAME}.order_items")
    total_revenue = cursor.fetchone()[0]
    
    # Gross margin analysis
    logging.info("\n💰 GROSS MARGIN ANALYSIS:")
    cursor.execute(f"""
        SELECT 
            COUNT(*) as product_count,
            AVG(cost) as avg_cost,
            AVG(base_price) as avg_selling_price,
            AVG((base_price - cost) / base_price * 100) as avg_gross_margin_percent,
            MIN((base_price - cost) / base_price * 100) as min_gross_margin_percent,
            MAX((base_price - cost) / base_price * 100) as max_gross_margin_percent
        FROM {SCHEMA_NAME}.products
    """)
    margin_stats = cursor.fetchone()
    
    if margin_stats:
        logging.info(f"   Average Cost:           ${margin_stats[1]:.2f}")
        logging.info(f"   Average Selling Price:  ${margin_stats[2]:.2f}")
        logging.info(f"   Average Gross Margin:   {margin_stats[3]:.1f}%")
        logging.info(f"   Margin Range:           {margin_stats[4]:.1f}% - {margin_stats[5]:.1f}%")
    
    # Calculate total cost and gross profit from actual sales
    cursor.execute(f"""
        SELECT 
            SUM(oi.total_amount) as total_revenue,
            SUM(p.cost * oi.quantity) as total_cost,
            SUM(oi.total_amount) - SUM(p.cost * oi.quantity) as total_gross_profit
        FROM {SCHEMA_NAME}.order_items oi
        JOIN {SCHEMA_NAME}.products p ON oi.product_id = p.product_id
    """)
    sales_margin = cursor.fetchone()
    
    if sales_margin and sales_margin[0]:
        actual_margin_pct = (sales_margin[2] / sales_margin[0]) * 100
        logging.info(f"   Actual Sales Margin:    {actual_margin_pct:.1f}%")
        logging.info(f"   Total Cost of Goods:    ${sales_margin[1]:.2f}")
        logging.info(f"   Total Gross Profit:     ${sales_margin[2]:.2f}")

    logging.info("\n✅ DATABASE SUMMARY:")
    logging.info(f"   Customers:          {customers:>8,}")
    logging.info(f"   Products:           {products:>8,}")
    logging.info(f"   Orders:             {orders:>8,}")
    logging.info(f"   Order Items:        {order_items:>8,}")
    if total_revenue and orders:
        logging.info(f"   Total Revenue:      ${total_revenue/1000:.1f}K")
        logging.info(f"   Avg Order:          ${total_revenue/orders:.2f}")
        logging.info(f"   Orders/Customer:    {orders/customers:.1f}")
        logging.info(f"   Items/Order:        {order_items/orders:.1f}")

def verify_seasonal_patterns(conn):
    """Verify that orders and inventory follow seasonal patterns from product_data.json"""
    
    logging.info("\n" + "=" * 60)
    logging.info("🌱 SEASONAL PATTERNS VERIFICATION")
    logging.info("=" * 60)
    
    try:
        cursor = conn.cursor()
        
        # Test 1: Order seasonality by category and month
        logging.info("\n📊 ORDER SEASONALITY BY CATEGORY:")
        logging.info("   Testing if orders follow seasonal multipliers from product_data.json")
        
        # Get actual orders by month and category
        cursor.execute(f"""
            SELECT c.category_name,
                   MONTH(o.order_date) as month,
                   COUNT(DISTINCT o.order_id) as order_count,
                   ROUND(AVG(oi.total_amount), 2) as avg_order_value
            FROM {SCHEMA_NAME}.orders o
            JOIN {SCHEMA_NAME}.order_items oi ON o.order_id = oi.order_id
            JOIN {SCHEMA_NAME}.products p ON oi.product_id = p.product_id
            JOIN {SCHEMA_NAME}.categories c ON p.category_id = c.category_id
            GROUP BY c.category_name, MONTH(o.order_date)
            HAVING COUNT(DISTINCT o.order_id) > 0
            ORDER BY c.category_name, month
        """)
        rows = cursor.fetchall()
        
        # Organize data by category
        category_data = {}
        for row in rows:
            category = row[0]  # category_name
            month = int(row[1])  # month
            if category not in category_data:
                category_data[category] = {}
            category_data[category][month] = {
                'order_count': row[2],  # order_count
                'avg_order_value': float(row[3])  # avg_order_value
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
        cursor.execute(f"""
            SELECT c.category_name,
                   AVG(CAST(i.stock_level AS FLOAT)) as avg_stock,
                   COUNT(*) as product_count
            FROM {SCHEMA_NAME}.inventory i
            JOIN {SCHEMA_NAME}.products p ON i.product_id = p.product_id
            JOIN {SCHEMA_NAME}.categories c ON p.category_id = c.category_id
            GROUP BY c.category_name
            ORDER BY avg_stock DESC
        """)
        inventory_rows = cursor.fetchall()
        
        # Calculate expected inventory ratios based on seasonal averages
        expected_inventory = {}
        for category_name, category_config in main_categories.items():
            if 'washington_seasonal_multipliers' in category_config:
                seasonal_multipliers = category_config['washington_seasonal_multipliers']
                avg_multiplier = sum(seasonal_multipliers) / len(seasonal_multipliers)
                expected_inventory[category_name] = avg_multiplier
        
        # Compare actual vs expected inventory ratios
        inventory_data = {row[0]: float(row[1]) for row in inventory_rows}  # category_name: avg_stock
        
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
        cursor.execute(f"""
            SELECT MONTH(o.order_date) as month,
                   COUNT(DISTINCT o.order_id) as total_orders
            FROM {SCHEMA_NAME}.orders o
            GROUP BY MONTH(o.order_date)
            ORDER BY month
        """)
        monthly_totals = cursor.fetchall()
        
        if monthly_totals:
            total_orders = sum(row[1] for row in monthly_totals)  # row[1] is total_orders
            logging.info("   Month    Orders    % of Total")
            logging.info("   " + "-" * 30)
            for row in monthly_totals:
                month_num = int(row[0])  # row[0] is month
                order_count = row[1]  # row[1] is total_orders
                pct = (order_count / total_orders) * 100
                logging.info(f"   {month_names[month_num-1]:<6} {order_count:>8}    {pct:>6.1f}%")
        
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

def generate_sql_server_database(num_customers: int = 50000):
    """Generate complete SQL Server database"""
    try:
        # Create connection
        conn = create_connection()
        
        try:
            # Drop existing schema to start fresh (optional)
            logging.info("Dropping existing schema if it exists...")
            cursor = conn.cursor()
            try:
                # Drop all tables in the schema in the correct order due to foreign key constraints
                cursor.execute(f"""
                    IF EXISTS (SELECT * FROM sys.schemas WHERE name = N'{SCHEMA_NAME}')
                    BEGIN
                        -- Drop tables in reverse dependency order
                        IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{SCHEMA_NAME}' AND TABLE_NAME = 'order_items')
                            DROP TABLE [{SCHEMA_NAME}].[order_items]
                        IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{SCHEMA_NAME}' AND TABLE_NAME = 'orders')
                            DROP TABLE [{SCHEMA_NAME}].[orders]
                        IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{SCHEMA_NAME}' AND TABLE_NAME = 'inventory')
                            DROP TABLE [{SCHEMA_NAME}].[inventory]
                        IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{SCHEMA_NAME}' AND TABLE_NAME = 'product_image_embeddings')
                            DROP TABLE [{SCHEMA_NAME}].[product_image_embeddings]
                        IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{SCHEMA_NAME}' AND TABLE_NAME = 'product_description_embeddings')
                            DROP TABLE [{SCHEMA_NAME}].[product_description_embeddings]
                        IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{SCHEMA_NAME}' AND TABLE_NAME = 'products')
                            DROP TABLE [{SCHEMA_NAME}].[products]
                        IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{SCHEMA_NAME}' AND TABLE_NAME = 'product_types')
                            DROP TABLE [{SCHEMA_NAME}].[product_types]
                        IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{SCHEMA_NAME}' AND TABLE_NAME = 'categories')
                            DROP TABLE [{SCHEMA_NAME}].[categories]
                        IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{SCHEMA_NAME}' AND TABLE_NAME = 'customers')
                            DROP TABLE [{SCHEMA_NAME}].[customers]
                        IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{SCHEMA_NAME}' AND TABLE_NAME = 'stores')
                            DROP TABLE [{SCHEMA_NAME}].[stores]
                        -- Drop the schema
                        DROP SCHEMA [{SCHEMA_NAME}]
                    END
                """)
                conn.commit()
                logging.info(f"Existing schema '{SCHEMA_NAME}' and tables dropped successfully")
            except Exception as drop_error:
                logging.info(f"Schema drop completed (some objects may not have existed): {drop_error}")
                conn.rollback()
            
            create_database_schema(conn)
            insert_stores(conn)
            insert_categories(conn)
            insert_product_types(conn)
            insert_customers(conn, num_customers)
            insert_products(conn)
            
            # Insert inventory data
            logging.info("\n" + "=" * 50)
            logging.info("INSERTING INVENTORY DATA")
            logging.info("=" * 50)
            insert_inventory(conn)
            
            # Insert order data
            logging.info("\n" + "=" * 50)
            logging.info("INSERTING ORDER DATA")
            logging.info("=" * 50)
            insert_orders(conn, num_customers)
            
            # Populate product embeddings
            logging.info("\n" + "=" * 50)
            logging.info("POPULATING PRODUCT EMBEDDINGS")
            logging.info("=" * 50)
            
            # Populate image embeddings
            logging.info("Populating product image embeddings...")
            populate_product_image_embeddings(conn, clear_existing=True)
            
            # Populate description embeddings
            logging.info("Populating product description embeddings...")
            populate_product_description_embeddings(conn, clear_existing=True)
            
            # Verify embeddings
            logging.info("Verifying image embeddings...")
            verify_embeddings_table(conn)
            
            logging.info("Verifying description embeddings...")
            verify_description_embeddings_table(conn)
            
            # Verify the database was created and has data
            logging.info("\n" + "=" * 50)
            logging.info("FINAL DATABASE VERIFICATION")
            logging.info("=" * 50)
            verify_database_contents(conn)
            
            logging.info("\n" + "=" * 50)
            logging.info("DATABASE GENERATION COMPLETE")
            logging.info("=" * 50)
            
            logging.info("Database generation completed successfully.")
        except Exception as e:
            logging.error(f"Error during database generation: {e}")
            raise
        finally:
            conn.close()
            logging.info("Database connection closed.")

    except Exception as e:
        logging.error(f"Failed to generate database: {e}")
        raise

def show_database_stats() -> None:
    """Show basic database statistics"""
    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()
        
        logging.info("\n" + "=" * 40)
        logging.info("SQL SERVER DATABASE STATISTICS")
        logging.info("=" * 40)
        
        # Get basic table counts
        tables = ['stores', 'customers', 'categories', 'product_types', 'products', 
                 'inventory', 'orders', 'order_items', 'product_image_embeddings', 'product_description_embeddings']
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {SCHEMA_NAME}.{table}")
            count = cursor.fetchone()[0]
            logging.info(f"{table.replace('_', ' ').title()}: {count:,}")
        
        # Get revenue information
        cursor.execute(f"SELECT SUM(total_amount) FROM {SCHEMA_NAME}.order_items")
        total_revenue = cursor.fetchone()[0]
        
        if total_revenue:
            cursor.execute(f"SELECT COUNT(*) FROM {SCHEMA_NAME}.orders")
            order_count = cursor.fetchone()[0]
            logging.info(f"Total Revenue: ${total_revenue:,.2f}")
            logging.info(f"Average Order Value: ${total_revenue/order_count:.2f}")
        
        logging.info("=" * 40)
        
    except Exception as e:
        logging.error(f"Error getting database stats: {e}")
    finally:
        if conn:
            conn.close()

def main():
    """Main function to handle command line arguments"""
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description='Generate SQL Server database with product embeddings')
    parser.add_argument('--show-stats', action='store_true', 
                       help='Show database statistics instead of generating')
    parser.add_argument('--embeddings-only', action='store_true',
                       help='Only populate product embeddings (database must already exist)')
    parser.add_argument('--verify-embeddings', action='store_true',
                       help='Only verify embeddings tables and show sample data')
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
            show_database_stats()
        elif args.verify_embeddings:
            # Only verify embeddings tables
            logging.info("Verifying embeddings tables...")
            conn = create_connection()
            try:
                verify_embeddings_table(conn)
                verify_description_embeddings_table(conn)
            finally:
                conn.close()
        elif args.embeddings_only:
            # Only populate embeddings
            logging.info("Populating product embeddings only...")
            conn = create_connection()
            try:
                # Populate image embeddings
                logging.info("Populating product image embeddings...")
                populate_product_image_embeddings(conn, clear_existing=args.clear_embeddings, batch_size=args.batch_size)
                
                # Populate description embeddings
                logging.info("Populating product description embeddings...")
                populate_product_description_embeddings(conn, clear_existing=args.clear_embeddings, batch_size=args.batch_size)
                
                # Verify embeddings
                logging.info("Verifying embeddings...")
                verify_embeddings_table(conn)
                verify_description_embeddings_table(conn)
                
                logging.info("Embeddings population completed successfully!")
            finally:
                conn.close()
        else:
            # Generate the complete database
            logging.info(f"Database will be created at {SQL_SERVER_CONFIG['server']}")
            logging.info(f"Database: {SQL_SERVER_CONFIG['database']}")
            logging.info(f"Schema: {SCHEMA_NAME}")
            generate_sql_server_database(num_customers=args.num_customers)
            
            logging.info("\nDatabase generated successfully!")
            logging.info(f"Server: {SQL_SERVER_CONFIG['server']}")
            logging.info(f"Database: {SQL_SERVER_CONFIG['database']}")
            logging.info(f"Schema: {SCHEMA_NAME}")
            logging.info(f"To view statistics: python {sys.argv[0]} --show-stats")
            logging.info(f"To populate embeddings only: python {sys.argv[0]} --embeddings-only")
            logging.info(f"To verify embeddings: python {sys.argv[0]} --verify-embeddings")
            
    except Exception as e:
        logging.error(f"Failed to complete operation: {e}")
        sys.exit(1)

def build_product_lookup(conn):
    """Build a lookup table for products by category and type"""
    try:
        logging.info("Building product lookup table...")
        cursor = conn.cursor()
        
        # Get all products with their category and type information
        cursor.execute(f"""
            SELECT p.product_id, p.sku, p.product_name, p.base_price, p.cost,
                   c.category_name, pt.type_name
            FROM {SCHEMA_NAME}.products p
            JOIN {SCHEMA_NAME}.categories c ON p.category_id = c.category_id
            JOIN {SCHEMA_NAME}.product_types pt ON p.type_id = pt.type_id
        """)
        products = cursor.fetchall()
        
        product_lookup = {}
        
        for product in products:
            category = product[5]  # category_name
            product_type = product[6]  # type_name
            
            if category not in product_lookup:
                product_lookup[category] = {}
            
            if product_type not in product_lookup[category]:
                product_lookup[category][product_type] = []
            
            product_lookup[category][product_type].append({
                'product_id': product[0],
                'sku': product[1],
                'name': product[2],
                'price': float(product[3]),
                'cost': float(product[4])
            })
        
        logging.info(f"Built product lookup with {len(products):,} products across {len(product_lookup)} categories")
        return product_lookup
        
    except Exception as e:
        logging.error(f"Error building product lookup: {e}")
        raise

def insert_inventory(conn):
    """Insert inventory data distributed across stores"""
    try:
        logging.info("Generating inventory...")
        cursor = conn.cursor()
        
        # Get all products and stores
        cursor.execute(f"SELECT product_id FROM {SCHEMA_NAME}.products")
        products = cursor.fetchall()
        
        cursor.execute(f"SELECT store_id FROM {SCHEMA_NAME}.stores")
        stores = cursor.fetchall()
        
        inventory_data = []
        
        for product in products:
            product_id = product[0]
            
            for store in stores:
                store_id = store[0]
                
                # Generate stock level (random between 10-500)
                stock_level = random.randint(10, 500)
                inventory_data.append((store_id, product_id, stock_level))
        
        batch_insert(conn, f"INSERT INTO {SCHEMA_NAME}.inventory (store_id, product_id, stock_level) VALUES (?, ?, ?)", inventory_data)
        
        logging.info(f"Successfully inserted {len(inventory_data):,} inventory records!")
    except Exception as e:
        logging.error(f"Error inserting inventory: {e}")
        raise

if __name__ == "__main__":
    # Check if required packages are available
    try:
        from dotenv import load_dotenv
        from faker import Faker
    except ImportError as e:
        logging.error(f"Required library not found: {e}")
        logging.error("Please install required packages with: pip install pyodbc faker python-dotenv")
        exit(1)
    
    main()


# =============================================================================
# ROW LEVEL SECURITY HELPER FUNCTIONS FOR WORKSHOP/DEMO
# =============================================================================
