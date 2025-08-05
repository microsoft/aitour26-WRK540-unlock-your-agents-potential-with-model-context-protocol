# Row Level Security (RLS) Implementation Guide

## Overview

This PostgreSQL database implements Row Level Security (RLS) to ensure that store managers can only access data related to their specific store. This is perfect for multi-tenant applications where data isolation is crucial.

## How It Works

### Database Schema Changes

1. **Store Table Enhanced**: Added `rls_user_id` (UUID) and `is_online` (boolean) columns
   ```sql
   CREATE TABLE retail.stores (
       store_id SERIAL PRIMARY KEY,
       store_name TEXT UNIQUE NOT NULL,
       rls_user_id UUID NOT NULL DEFAULT gen_random_uuid(),
       is_online BOOLEAN NOT NULL DEFAULT false
   );
   ```

2. **Customer Table Enhanced**: Added `primary_store_id` foreign key to establish store relationship
   ```sql
   CREATE TABLE retail.customers (
       customer_id SERIAL PRIMARY KEY,
       first_name TEXT NOT NULL,
       last_name TEXT NOT NULL,
       email TEXT UNIQUE NOT NULL,
       phone TEXT,
       primary_store_id INTEGER,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       FOREIGN KEY (primary_store_id) REFERENCES retail.stores (store_id)
   );
   ```

3. **RLS Policies Created**: Policies ensure managers only see their store's data
   - **Orders**: Only orders from manager's store
   - **Order Items**: Only items from orders in manager's store  
   - **Customers**: Only customers assigned to manager's store OR who have ordered from their store
   - **Inventory**: Only inventory for manager's store

### Customer Security Model

The customer table uses a **hybrid approach** for maximum flexibility:

```sql
-- Enhanced customer policy with both direct and indirect relationships
CREATE POLICY store_manager_customers ON retail.customers
FOR ALL TO PUBLIC
USING (
    -- Direct relationship: customers assigned to this store
    EXISTS (
        SELECT 1 FROM retail.stores s 
        WHERE s.store_id = retail.customers.primary_store_id 
        AND s.rls_user_id::text = current_setting('app.current_rls_user_id', true)
    )
    OR
    -- Indirect relationship: customers who have ordered from this store
    EXISTS (
        SELECT 1 FROM retail.orders o
        JOIN retail.stores s ON o.store_id = s.store_id
        WHERE o.customer_id = retail.customers.customer_id
        AND s.rls_user_id::text = current_setting('app.current_rls_user_id', true)
    )
);
```

**What this enables:**
- ✅ **Prospective Customers**: Store managers can see customers assigned to their store before they place orders
- ✅ **Walk-in Customers**: Customers discovered through orders are also visible
- ✅ **Flexible Assignment**: 80% of customers are assigned to stores, 20% remain unassigned (online-only, legacy, etc.)
- ✅ **Realistic Business Model**: Customers can register at a store before purchasing

### Security Model Benefits

The RLS policies use PostgreSQL's `current_setting()` function to check the current manager context:

```sql
-- Example policy for orders
CREATE POLICY store_manager_orders ON retail.orders
FOR ALL TO PUBLIC
USING (
    EXISTS (
        SELECT 1 FROM retail.stores s 
        WHERE s.store_id = retail.orders.store_id 
        AND s.rls_user_id::text = current_setting('app.current_rls_user_id', true)
    )
);
```

## Workshop Usage

### 1. Generate Database with RLS

```bash
# Generate the complete database with RLS enabled
python generate_zava_postgres.py

# The script will output manager IDs for each store like:
# Store Manager IDs (for workshop use):
#   Zava Retail Bellevue: 12345678-1234-1234-1234-123456789012
#   Zava Retail Seattle: 87654321-4321-4321-4321-210987654321
```

### 2. Demo RLS in Action

```python
import asyncio
from generate_zava_postgres import demo_row_level_security

# Run the complete RLS demonstration
asyncio.run(demo_row_level_security())
```

This will show:
- All available stores and their manager IDs
- How many orders/customers/inventory each manager can see
- Revenue visible to each manager

### 3. Get Manager IDs Programmatically

```python
import asyncio
from generate_zava_postgres import get_manager_ids

# Get all manager IDs
manager_ids = asyncio.run(get_manager_ids())
print(manager_ids)
# Output: {'Zava Retail Seattle': '12345...', 'Zava Retail Bellevue': '67890...'}
```

### 4. Set Manager Context in Your Application

```python
import asyncpg
import asyncio

async def query_as_manager(rls_user_id: str):
    conn = await asyncpg.connect(
        host='localhost', 
        database='zava', 
        user='postgres', 
        password='P@ssw0rd!'
    )
    
    try:
        # Set the manager context - THIS IS THE KEY STEP
        await conn.execute(
            "SELECT set_config('app.current_rls_user_id', $1, false)", 
            rls_user_id
        )
        
        # Now all queries will be filtered by RLS
        orders = await conn.fetch("SELECT * FROM retail.orders LIMIT 10")
        customers = await conn.fetch("SELECT * FROM retail.customers LIMIT 10")
        
        print(f"Manager {rls_user_id} can see {len(orders)} orders")
        print(f"Manager {rls_user_id} can see {len(customers)} customers")
        
    finally:
        await conn.close()

# Usage
asyncio.run(query_as_manager("12345678-1234-1234-1234-123456789012"))
```

## Workshop Scenarios

### Scenario 1: Store Manager Dashboard
```python
async def store_manager_dashboard(rls_user_id: str):
    conn = await create_connection()
    
    # Set manager context
    await conn.execute("SELECT set_config('app.current_rls_user_id', $1, false)", rls_user_id)
    
    # Get dashboard data - all queries automatically filtered by RLS
    stats = await conn.fetchrow("""
        SELECT 
            COUNT(DISTINCT o.order_id) as total_orders,
            COUNT(DISTINCT c.customer_id) as total_customers,
            SUM(oi.total_amount) as total_revenue,
            COUNT(DISTINCT inv.product_id) as inventory_items
        FROM retail.orders o
        JOIN retail.customers c ON o.customer_id = c.customer_id
        JOIN retail.order_items oi ON o.order_id = oi.order_id
        JOIN retail.inventory inv ON TRUE  -- Cross join to count inventory
    """)
    
    return stats
```

### Scenario 2: Multi-Manager Comparison
```python
async def compare_managers():
    managers = await get_manager_ids()
    
    for store_name, rls_user_id in managers.items():
        stats = await store_manager_dashboard(rls_user_id)
        print(f"{store_name}: {stats['total_orders']} orders, ${stats['total_revenue']:,.2f} revenue")
```

## Security Benefits

1. **Automatic Filtering**: No need to add WHERE clauses to every query
2. **Application-Level Transparency**: Your app code doesn't change
3. **Database-Level Enforcement**: Security can't be bypassed by malicious code
4. **Audit-Friendly**: Clear separation of data access by role

## Workshop Learning Objectives

By the end of this workshop, participants will understand:

1. How to implement Row Level Security in PostgreSQL
2. How to use session variables for context setting
3. How RLS policies work with complex joins
4. Why database-level security is more robust than application-level filtering
5. Real-world multi-tenant application patterns

## Quick Commands for Workshop

```bash
# 1. Generate database
python generate_zava_postgres.py

# 2. Demo RLS
python -c "import asyncio; from generate_zava_postgres import demo_row_level_security; asyncio.run(demo_row_level_security())"

# 3. Get manager IDs
python -c "import asyncio; from generate_zava_postgres import get_manager_ids; print(asyncio.run(get_manager_ids()))"

# 4. Show stats
python generate_zava_postgres.py --show-stats
```

## Troubleshooting

### No Data Visible
If queries return no results, check:
1. Manager context is set: `SELECT current_setting('app.current_rls_user_id', true)`
2. Manager ID exists in stores table
3. RLS policies are enabled: `SELECT * FROM pg_policies WHERE tablename = 'orders'`

### Wrong Data Visible  
If seeing data from other stores:
1. Verify RLS is enabled: `SELECT relrowsecurity FROM pg_class WHERE relname = 'orders'`
2. Check manager ID format (should be UUID string)
3. Verify policy logic with `EXPLAIN` plans
