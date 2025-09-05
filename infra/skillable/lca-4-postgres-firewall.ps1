# LCA Metadata
# Delay: 20 seconds

# =========================
# VM Life Cycle Action (PowerShell)
# Pull outputs from ARM/Bicep deployment and write .env
# =========================

# Set error action preference to stop on any error
$ErrorActionPreference = "Stop"


# --- logging to both Skillable log + file ---
$logDir = "C:\logs"
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir | Out-Null }
$logFile = Join-Path $logDir "vm-init-pg-firewall-$(Get-Date -Format 'yyyyMMdd_HHmmss').log"
"[$(Get-Date -Format s)] VM LCA start" | Tee-Object -FilePath $logFile

function Log { param([string]$m) $ts = "[$(Get-Date -Format s)] $m"; $ts | Tee-Object -FilePath $logFile -Append }

# --- Skillable tokens / lab values ---
$UniqueSuffix = "@lab.LabInstance.Id"
$TenantId = "@lab.CloudSubscription.TenantId"
$AppId = "@lab.CloudSubscription.AppId"
$Secret = "@lab.CloudSubscription.AppSecret"
$SubId = "@lab.CloudSubscription.Id"

# Resource group where your template deployed (via alias rg-zava-agent-wks)
$ResourceGroup = "@lab.CloudResourceGroup(rg-zava-agent-wks).Name"

# Template PARAMETER (✅ supported by Skillable token macros)
$AzurePgPassword = "@lab.CloudResourceTemplate(WRK540-AITour2026).Parameters[postgresAdminPassword]"

# --- Azure login (service principal) ---
Log "Authenticating to Azure tenant $TenantId, subscription $SubId"
$sec = ConvertTo-SecureString $Secret -AsPlainText -Force
$cred = [pscredential]::new($AppId, $sec)
Connect-AzAccount -ServicePrincipal -Tenant $TenantId -Credential $cred -Subscription $SubId | Out-Null
$ctx = Get-AzContext
Log "Logged in as: $($ctx.Account) | Sub: $($ctx.Subscription.Name) ($($ctx.Subscription.Id))"

$PostgresServerName = "pg-zava-agent-wks-$UniqueSuffix"
$ResourceGroup = "@lab.CloudResourceGroup(rg-zava-agent-wks).Name"

# Set IP range 0.0.0.0 to 255.255.255.255
$StartIP = "0.0.0.0"
$EndIP = "255.255.255.255"
$RuleName = "allow-range-all"
Log "Adding firewall rule for IP range: $StartIP to $EndIP"
New-AzPostgreSqlFlexibleServerFirewallRule `
  -Name $RuleName `
  -ResourceGroupName $ResourceGroup `
  -ServerName $PostgresServerName `
  -StartIPAddress $StartIP `
  -EndIPAddress   $EndIP | Out-Null




Log "Restoring PG Database"

$PsqlVersion = & psql --version
Log "PostgreSQL client tools found: $PsqlVersion"

# Set up Azure PostgreSQL connection parameters using naming convention
$AzurePgHost = "pg-zava-agent-wks-$UniqueSuffix.postgres.database.azure.com"
$AzurePgUser = if ($env:AZURE_PG_USER) { $env:AZURE_PG_USER } else { "azureuser" }
$AzurePgPassword = if ($AzurePgPassword) { $AzurePgPassword } elseif ($env:AZURE_PG_PASSWORD) { $env:AZURE_PG_PASSWORD } else { $null }
$AzurePgDatabase = if ($env:AZURE_PG_DATABASE) { $env:AZURE_PG_DATABASE } else { "postgres" }
$AzurePgPort = if ($env:AZURE_PG_PORT) { $env:AZURE_PG_PORT } else { "5432" }

Log "Host: $AzurePgHost"
Log "User: $AzurePgUser"
Log ""

# Set up environment variables for PostgreSQL connection
$env:PGHOST = $AzurePgHost
$env:PGPORT = $AzurePgPort
$env:PGUSER = $AzurePgUser
$env:PGPASSWORD = $AzurePgPassword
$env:PGDATABASE = $AzurePgDatabase
$env:PGSSLMODE = "require"

Log "Connecting to Azure PostgreSQL..."
Log "   Host: $AzurePgHost"
Log "   User: $AzurePgUser"
Log "   SSL: Required"

# Test connection
Log "Testing database connection..."
try {
    $null = & psql -c "SELECT version();" 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Connection failed"
    }
    Log "Connection successful"
}
catch {
    Log "Failed to connect to Azure PostgreSQL"
    Log "Please check your connection parameters and network access"
    exit 1
}

# Create the zava database
Log "Creating 'zava' database..."
try {
    $DatabaseExists = & psql -lqt | Select-String "zava"
    if (-not $DatabaseExists) {
        & psql -c "CREATE DATABASE zava;"
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to create database"
        }
        Log "Created database 'zava'"
    }
    else {
        Log "Database 'zava' already exists"
    }
}
catch {
    Log "Failed to create database: $_"
    exit 1
}

# Grant privileges and switch to zava database
& psql -c "GRANT ALL PRIVILEGES ON DATABASE zava TO $AzurePgUser;"
$env:PGDATABASE = "zava"

# Install pgvector extension
Log "Installing pgvector extension..."
try {
    & psql -c "CREATE EXTENSION IF NOT EXISTS vector;"
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to create extension"
    }
}
catch {
    Log "Failed to install pgvector extension (this may be normal if not available)"
}

# Create store_manager user
Log "Creating 'store_manager' user..."
$CreateUserSQL = @'
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_user WHERE usename = 'store_manager') THEN
        CREATE USER store_manager WITH PASSWORD 'StoreManager123!';
        GRANT CONNECT ON DATABASE zava TO store_manager;
        RAISE NOTICE 'Created store_manager user successfully';
    ELSE
        RAISE NOTICE 'store_manager user already exists';
    END IF;
END $$;
'@

try {
    $CreateUserSQL | & psql
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to create user"
    }
}
catch {
    Log "Failed to create store_manager user: $_"
}

# Check for backup file and restore if found
$BackupFile = "C:\Users\Admin\aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol\scripts\backups\zava_retail_2025_07_21_postgres_rls.backup"

Log "Checking for backup files..."
if (Test-Path $BackupFile) {
    Log "Found backup file: $BackupFile"
    
    $BackupSize = (Get-Item $BackupFile).Length
    Log "Backup file size: $BackupSize bytes"
    
    # Validate backup file
    try {
        $null = & pg_restore -l $BackupFile 2>$null
        if ($LASTEXITCODE -ne 0) {
            throw "Invalid backup file"
        }
        Log "Backup file is valid"
        
        # Restore backup (pg_restore exit code 1 is normal for warnings)
        Log "Restoring backup..."
        & pg_restore --dbname="zava" --no-owner --no-privileges $BackupFile 2>$null
        $RestoreExitCode = $LASTEXITCODE
        
        if ($RestoreExitCode -eq 0 -or $RestoreExitCode -eq 1) {
            Log "Backup restored successfully"
            
            # Grant comprehensive permissions to store_manager for RLS
            Log "Setting up store_manager permissions for RLS..."
            $PermissionsSQL = @'
-- Grant schema usage
GRANT USAGE ON SCHEMA retail TO store_manager;

-- Grant permissions on all tables and sequences  
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA retail TO store_manager;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA retail TO store_manager;

-- Grant default privileges for future objects
ALTER DEFAULT PRIVILEGES IN SCHEMA retail GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO store_manager;
ALTER DEFAULT PRIVILEGES IN SCHEMA retail GRANT USAGE, SELECT ON SEQUENCES TO store_manager;
'@
            
            try {
                $PermissionsSQL | & psql
            }
            catch {
                Log "Some permission grants may have failed (this is often normal)"
            }
            
            # Verify the restoration
            try {
                $TableCountResult = & psql -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'retail';"
                $TableCount = $TableCountResult.Trim()
                Log "Found $TableCount tables in retail schema"
                
                # Check for data in key tables
                $StoresCountResult = & psql -t -c "SELECT COUNT(*) FROM retail.stores;" 2>$null
                $StoresCount = if ($LASTEXITCODE -eq 0) { $StoresCountResult.Trim() } else { "0" }
                
                $ProductsCountResult = & psql -t -c "SELECT COUNT(*) FROM retail.products;" 2>$null
                $ProductsCount = if ($LASTEXITCODE -eq 0) { $ProductsCountResult.Trim() } else { "0" }
                
                Log "Data check: $StoresCount stores, $ProductsCount products"
            }
            catch {
                Log "Could not verify table counts"
            }
        }
        else {
            Log "Backup restoration failed, but database is still functional"
        }
    }
    catch {
        Log "Backup file appears to be invalid: $_"
    }
}
else {
    Log "No backup file found at $BackupFile"
}

Log "Zava PostgreSQL Database initialization completed on Azure!"
Log "Database: zava"
Log "Host: $AzurePgHost"
Log "Users: $AzurePgUser (admin), store_manager (for testing)"
Log "Extensions: pgvector"
Log "SSL: Required"
Log ""
Log "Connect using:"
Log "   Environment variables:"
Log "   `$env:PGHOST = '$AzurePgHost'; `$env:PGPORT = '$AzurePgPort'; `$env:PGUSER = '$AzurePgUser'"
Log "   `$env:PGPASSWORD = '$AzurePgPassword'; `$env:PGDATABASE = 'zava'; `$env:PGSSLMODE = 'require'"
Log "   psql"
Log ""
Log "PostgreSQL Connection URL (store_manager):"
Log "   postgresql://store_manager:StoreManager123!@$AzurePgHost`:$AzurePgPort/zava?sslmode=require"
