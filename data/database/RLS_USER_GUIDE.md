# PostgreSQL User Configuration for RLS Testing

This document explains how to use the two different PostgreSQL users in this workshop.

## Available Users

### 1. `postgres` (Superuser)

- **Username**: `postgres`
- **Password**: `P@ssw0rd!`
- **Privileges**: Superuser (bypasses RLS by default)
- **Use case**: Database administration, schema creation, data generation
- **Created**: Automatically by PostgreSQL

### 2. `store_manager` (Regular User)

- **Username**: `store_manager`
- **Password**: `StoreManager123!`
- **Privileges**: Regular user (RLS policies apply)
- **Use case**: Testing RLS policies, simulating application user access
- **Created**: Automatically by `init-db.sh` during database initialization

## Database Initialization

The `store_manager` user is automatically created when the PostgreSQL database is initialized. This happens through the `init-db.sh` script which:

1. Creates the `zava` database
2. Installs the `pgvector` extension
3. **Creates the `store_manager` user with proper permissions**
4. Restores backup data if available
5. Re-grants permissions after restoration

To verify the user was created properly, you can run:

```bash
# Test the store_manager user creation
/workspace/scripts/test_store_manager.sh
```

## Connection Examples

### Python (asyncpg)

```python
import asyncpg

# Connect as postgres (superuser)
POSTGRES_CONFIG = {
    'host': 'db',
    'port': 5432,
    'user': 'postgres',
    'password': 'P@ssw0rd!',
    'database': 'zava'
}

# Connect as store_manager (regular user for RLS testing)
STORE_MANAGER_CONFIG = {
    'host': 'db',
    'port': 5432,
    'user': 'store_manager',
    'password': 'StoreManager123!',
    'database': 'zava'
}

# Example connection
conn = await asyncpg.connect(**STORE_MANAGER_CONFIG)
```

### psql Command Line

```bash
# Connect as postgres
psql -h db -p 5432 -U postgres -d zava

# Connect as store_manager
psql -h db -p 5432 -U store_manager -d zava
```

## Testing Row Level Security (RLS)

### Step 1: Connect as store_manager
The store_manager user has RLS policies applied, so you'll only see data for stores managed by the current manager context.

### Step 2: Set Manager Context
Before querying, you need to set which store manager you're acting as:

```sql
-- Set the manager context (use any rls_user_id from the stores table)
SELECT set_config('app.current_rls_user_id', '741421a9-0bb8-47bd-9aa3-29162e361fd8', false);
```

### Step 3: Query with RLS Applied
Now when you query, you'll only see data for that manager's store:

```sql
-- This will only return customers for the specified manager's store
SELECT * FROM retail.customers LIMIT 10;

-- This will only return orders for the specified manager's store
SELECT * FROM retail.orders LIMIT 10;

-- This will only return inventory for the specified manager's store
SELECT * FROM retail.inventory LIMIT 10;
```

## Available Store Manager IDs

Run this query to see all available manager IDs:

```sql
SELECT store_id, store_name, rls_user_id, is_online
FROM retail.stores
ORDER BY store_name;
```

Example output:
```
store_id |      store_name      |              rls_user_id              | is_online
---------+----------------------+--------------------------------------+-----------
      1  | Zava Retail Bellevue | efb77123-0003-45d0-86a5-af068b6cb13f | f
      2  | Zava Retail Everett  | deec7d60-8058-4c7f-b33b-41d1cc1c4db3 | f
      3  | Zava Retail Kirkland | 0d4ad565-0277-438e-bb09-cd068b0f013c | f
      4  | Zava Retail Online   | 067c3dcf-4b1f-4046-88b5-8a18eb7fc371 | t
      5  | Zava Retail Redmond  | 569d3720-361d-418c-a9a6-096044758f90 | f
      6  | Zava Retail Seattle  | 741421a9-0bb8-47bd-9aa3-29162e361fd8 | f
      7  | Zava Retail Spokane  | e263de8c-a9f3-4d66-ab21-ff0e98866c29 | f
      8  | Zava Retail Tacoma   | e6b08e42-ac92-4cdc-8905-2a24797ee6a0 | f
```

## Quick Test Scripts

### Option 1: Full RLS Test
```bash
cd /workspace/src/shared/data/database
python test_rls_with_store_manager.py
```

### Option 2: Simple Connection Test
```bash
cd /workspace/src/shared/data/database
python connect_as_store_manager.py
```

## RLS Policy Details

The following tables have RLS policies applied:

1. **customers**: Users can only see customers assigned to their store or customers who have ordered from their store
2. **orders**: Users can only see orders from their store
3. **order_items**: Users can only see order items from their store
4. **inventory**: Users can only see inventory for their store

## Troubleshooting

### Issue: Getting 0 results when querying
**Solution**: Make sure you've set the manager context:
```sql
SELECT set_config('app.current_rls_user_id', 'YOUR_MANAGER_ID_HERE', false);
```

### Issue: RLS not working (seeing all data)
**Cause**: You're connected as a superuser (postgres)
**Solution**: Connect as store_manager user instead

### Issue: Permission denied errors
**Cause**: The store_manager user doesn't have the required permissions
**Solution**: Check that the user was created properly by connecting as postgres and running:
```sql
SELECT usename, usesuper FROM pg_user WHERE usename = 'store_manager';
```

## Example Workflow

```python
import asyncpg

async def test_rls():
    # Connect as store_manager
    conn = await asyncpg.connect(
        host='db', port=5432, user='store_manager', 
        password='StoreManager123!', database='zava'
    )
    
    # Set manager context
    await conn.execute(
        "SELECT set_config('app.current_rls_user_id', $1, false)", 
        '741421a9-0bb8-47bd-9aa3-29162e361fd8'  # Seattle store manager
    )
    
    # Query data (will be filtered by RLS)
    customers = await conn.fetch("SELECT * FROM retail.customers LIMIT 5")
    print(f"Found {len(customers)} customers for this manager")
    
    await conn.close()
```
