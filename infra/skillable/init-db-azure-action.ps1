
# Set error action preference to stop on any error
$ErrorActionPreference = "Stop"

$UniqueSuffix     = "@lab.LabInstance.Id"
# $AzurePgPassword  = "@lab.CloudResourceTemplate(WRK540-AITour2026).Parameters[postgresAdminPassword]"
$AzurePgPassword  = "SecurePassword123!"
# $TenantId         = "@lab.CloudSubscription.TenantId"
# $AppId            = "@lab.CloudSubscription.AppId"
# $Secret           = "@lab.CloudSubscription.AppSecret"
# $SubId            = "@lab.CloudSubscription.Id"



Write-Host "🎯 Using UNIQUE_SUFFIX: $UniqueSuffix" -ForegroundColor Yellow
Write-Host ""

# Verify the PostgreSQL server exists
# $PostgresServerName = "pg-zava-agent-wks-$UniqueSuffix"
# $ResourceGroup = "rg-zava-agent-wks-$UniqueSuffix"


Write-Host ""

$PsqlVersion = & psql --version
Write-Host "✅ PostgreSQL client tools found: $PsqlVersion" -ForegroundColor Green

# Set up Azure PostgreSQL connection parameters using naming convention
$AzurePgHost = "pg-zava-agent-wks-$UniqueSuffix.postgres.database.azure.com"
$AzurePgUser = if ($env:AZURE_PG_USER) { $env:AZURE_PG_USER } else { "azureuser" }
$AzurePgPassword = if ($AzurePgPassword) { $AzurePgPassword } elseif ($env:AZURE_PG_PASSWORD) { $env:AZURE_PG_PASSWORD } else { $null }
$AzurePgDatabase = if ($env:AZURE_PG_DATABASE) { $env:AZURE_PG_DATABASE } else { "postgres" }
$AzurePgPort = if ($env:AZURE_PG_PORT) { $env:AZURE_PG_PORT } else { "5432" }

Write-Host "📡 Host: $AzurePgHost" -ForegroundColor Yellow
Write-Host "👤 User: $AzurePgUser" -ForegroundColor Yellow
Write-Host ""

# Set up environment variables for PostgreSQL connection
$env:PGHOST = $AzurePgHost
$env:PGPORT = $AzurePgPort
$env:PGUSER = $AzurePgUser
$env:PGPASSWORD = $AzurePgPassword
$env:PGDATABASE = $AzurePgDatabase
$env:PGSSLMODE = "require"

Write-Host "🔗 Connecting to Azure PostgreSQL..." -ForegroundColor Cyan
Write-Host "   Host: $AzurePgHost" -ForegroundColor Gray
Write-Host "   User: $AzurePgUser" -ForegroundColor Gray
Write-Host "   SSL: Required" -ForegroundColor Gray

# Test connection
Write-Host "🧪 Testing database connection..." -ForegroundColor Cyan
try {
    $null = & psql -c "SELECT version();" 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Connection failed"
    }
    Write-Host "✅ Connection successful!" -ForegroundColor Green
}
catch {
    Write-Host "❌ Failed to connect to Azure PostgreSQL" -ForegroundColor Red
    Write-Host "💡 Please check your connection parameters and network access" -ForegroundColor Cyan
    exit 1
}

# Create the zava database
Write-Host "📦 Creating 'zava' database..." -ForegroundColor Cyan
try {
    $DatabaseExists = & psql -lqt | Select-String "zava"
    if (-not $DatabaseExists) {
        & psql -c "CREATE DATABASE zava;"
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to create database"
        }
        Write-Host "✅ Created database 'zava'" -ForegroundColor Green
    }
    else {
        Write-Host "✅ Database 'zava' already exists" -ForegroundColor Green
    }
}
catch {
    Write-Host "❌ Failed to create database: $_" -ForegroundColor Red
    exit 1
}

# Grant privileges and switch to zava database
& psql -c "GRANT ALL PRIVILEGES ON DATABASE zava TO $AzurePgUser;"
$env:PGDATABASE = "zava"

# Install pgvector extension
Write-Host "🔧 Installing pgvector extension..." -ForegroundColor Cyan
try {
    & psql -c "CREATE EXTENSION IF NOT EXISTS vector;"
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to create extension"
    }
}
catch {
    Write-Host "⚠️  Failed to install pgvector extension (this may be normal if not available)" -ForegroundColor Yellow
}

# Create store_manager user
Write-Host "👤 Creating 'store_manager' user..." -ForegroundColor Cyan
$CreateUserSQL = @"
DO `$`$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_user WHERE usename = 'store_manager') THEN
        CREATE USER store_manager WITH PASSWORD 'StoreManager123!';
        GRANT CONNECT ON DATABASE zava TO store_manager;
        RAISE NOTICE 'Created store_manager user successfully';
    ELSE
        RAISE NOTICE 'store_manager user already exists';
    END IF;
END `$`$;
"@

try {
    $CreateUserSQL | & psql
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to create user"
    }
}
catch {
    Write-Host "⚠️  Failed to create store_manager user: $_" -ForegroundColor Yellow
}

# Check for backup file and restore if found
$BackupFile = "C:\Users\Admin\aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol\scripts\backups\zava_retail_2025_07_21_postgres_rls.backup"

Write-Host "🔍 Checking for backup files..." -ForegroundColor Cyan
if (Test-Path $BackupFile) {
    Write-Host "📂 Found backup file: $BackupFile" -ForegroundColor Green
    
    $BackupSize = (Get-Item $BackupFile).Length
    Write-Host "📊 Backup file size: $BackupSize bytes" -ForegroundColor Gray
    
    # Validate backup file
    try {
        $null = & pg_restore -l $BackupFile 2>$null
        if ($LASTEXITCODE -ne 0) {
            throw "Invalid backup file"
        }
        Write-Host "✅ Backup file is valid" -ForegroundColor Green
        
        # Restore backup (pg_restore exit code 1 is normal for warnings)
        Write-Host "🚀 Restoring backup..." -ForegroundColor Cyan
        & pg_restore --dbname="zava" --no-owner --no-privileges $BackupFile 2>$null
        $RestoreExitCode = $LASTEXITCODE
        
        if ($RestoreExitCode -eq 0 -or $RestoreExitCode -eq 1) {
            Write-Host "✅ Backup restored successfully" -ForegroundColor Green
            
            # Grant comprehensive permissions to store_manager for RLS
            Write-Host "🔑 Setting up store_manager permissions for RLS..." -ForegroundColor Cyan
            $PermissionsSQL = @"
-- Grant schema usage
GRANT USAGE ON SCHEMA retail TO store_manager;

-- Grant permissions on all tables and sequences  
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA retail TO store_manager;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA retail TO store_manager;

-- Grant default privileges for future objects
ALTER DEFAULT PRIVILEGES IN SCHEMA retail GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO store_manager;
ALTER DEFAULT PRIVILEGES IN SCHEMA retail GRANT USAGE, SELECT ON SEQUENCES TO store_manager;
"@
            
            try {
                $PermissionsSQL | & psql
            }
            catch {
                Write-Host "⚠️  Some permission grants may have failed (this is often normal)" -ForegroundColor Yellow
            }
            
            # Verify the restoration
            try {
                $TableCountResult = & psql -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'retail';"
                $TableCount = $TableCountResult.Trim()
                Write-Host "✅ Found $TableCount tables in retail schema" -ForegroundColor Green
                
                # Check for data in key tables
                $StoresCountResult = & psql -t -c "SELECT COUNT(*) FROM retail.stores;" 2>$null
                $StoresCount = if ($LASTEXITCODE -eq 0) { $StoresCountResult.Trim() } else { "0" }
                
                $ProductsCountResult = & psql -t -c "SELECT COUNT(*) FROM retail.products;" 2>$null
                $ProductsCount = if ($LASTEXITCODE -eq 0) { $ProductsCountResult.Trim() } else { "0" }
                
                Write-Host "📊 Data check: $StoresCount stores, $ProductsCount products" -ForegroundColor Gray
            }
            catch {
                Write-Host "⚠️  Could not verify table counts" -ForegroundColor Yellow
            }
        }
        else {
            Write-Host "⚠️  Backup restoration failed, but database is still functional" -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "⚠️  Backup file appears to be invalid: $_" -ForegroundColor Yellow
    }
}
else {
    Write-Host "⚠️  No backup file found at $BackupFile" -ForegroundColor Yellow
}

Write-Host "🎉 Zava PostgreSQL Database initialization completed on Azure!" -ForegroundColor Green
Write-Host "📊 Database: zava" -ForegroundColor Gray
Write-Host "🌐 Host: $AzurePgHost" -ForegroundColor Gray
Write-Host "👤 Users: $AzurePgUser (admin), store_manager (for testing)" -ForegroundColor Gray
Write-Host "🔌 Extensions: pgvector" -ForegroundColor Gray
Write-Host "🔒 SSL: Required" -ForegroundColor Gray
Write-Host ""
Write-Host "🔧 Connect using:" -ForegroundColor Cyan
Write-Host "   Environment variables:" -ForegroundColor Gray
Write-Host "   `$env:PGHOST = '$AzurePgHost'; `$env:PGPORT = '$AzurePgPort'; `$env:PGUSER = '$AzurePgUser'" -ForegroundColor Gray
Write-Host "   `$env:PGPASSWORD = '$AzurePgPassword'; `$env:PGDATABASE = 'zava'; `$env:PGSSLMODE = 'require'" -ForegroundColor Gray
Write-Host "   psql" -ForegroundColor Gray
Write-Host "" -ForegroundColor Gray
Write-Host "   PostgreSQL Connection URL (store_manager):" -ForegroundColor Gray
Write-Host "   postgresql://store_manager:StoreManager123!@$AzurePgHost`:$AzurePgPort/zava?sslmode=require" -ForegroundColor Gray
