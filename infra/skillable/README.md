# Deploy to Azure

## Convert main.bicep to main.parameters.json

From VS Code, you can use the Bicep extension to easily convert your Bicep files to JSON parameters files.

1. Open the Command Palette (F1) and search for "Bicep: Export Template".
2. Select the "Bicep: Export Template" command.
3. Choose the "Export to parameters file" option.
4. Save the generated `main.parameters.json` file.

This repository contains Azure infrastructure templates for deploying AI Foundry services with PostgreSQL database support.

**Note**: PostgreSQL deployment is mandatory and will always be included in the infrastructure deployment.

## Prerequisites

- Azure CLI installed and logged in
- Appropriate Azure subscription permissions
- PostgreSQL client tools (for database initialization)

## Configuration

**First, generate a random 8-character suffix:**

```powershell
$UNIQUE_SUFFIX = -join ((1..4) | ForEach {'{0:x2}' -f (Get-Random -Max 256)})
Write-Host "Your unique suffix: $UNIQUE_SUFFIX"
$POSTGRES_PASSWORD = 'SecurePassword123!'
```

### Required Parameters

The following parameters are passed directly on the command line:

- **location**: Azure region for deployment (e.g., "westus")
- **uniqueSuffix**: Unique 4-character identifier (use the generated `$UNIQUE_SUFFIX` variable)
- **postgresAdminPassword**: Secure password for PostgreSQL admin user (use the `$POSTGRES_PASSWORD` variable)

## Deployment Steps

### 1. Create Resource Group

```powershell
az group create --name "rg-zava-agent-wks-$UNIQUE_SUFFIX" --location "West US"
```

### 2. Deploy Infrastructure

```powershell
az deployment group create `
  --resource-group "rg-zava-agent-wks-$UNIQUE_SUFFIX" `
  --template-file main.bicep `
  --parameters location="westus" uniqueSuffix="$UNIQUE_SUFFIX" postgresAdminPassword="$POSTGRES_PASSWORD"
```

### 3. Initialize PostgreSQL Database

After infrastructure deployment, you can initialize the database with sample data. The initialization script will automatically:

- Add your current IP address to the PostgreSQL firewall rules
- Connect to the Azure PostgreSQL server
- Create the `zava` database and required users
- Install the pgvector extension
- Restore sample data (if backup file exists)

```bash
# Install PostgreSQL client tools (if not already installed)

# macOS (using Homebrew)
brew install postgresql@17

# Windows (using winget)
winget install PostgreSQL.PostgreSQL.17
```

#### Run Database Initialization

```powershell
# Run database initialization with your unique suffix
./init-db-azure.ps1 -UniqueSuffix $UNIQUE_SUFFIX -AzurePgPassword $POSTGRES_PASSWORD
```

**What the script does:**

1. **Firewall Configuration**: Automatically detects your current public IP address and adds it to the PostgreSQL server firewall rules
2. **Database Setup**: Creates the `zava` database and configures users with proper permissions
3. **Extensions**: Installs the pgvector extension for vector operations
4. **Data Restoration**: Restores sample retail data if backup files are available

**Note**: The script uses the same `$UNIQUE_SUFFIX` from your deployment to automatically construct the correct server names and connection details.

## Infrastructure Components

The `main-deploy.bicep` template deploys:

- **AI Foundry Hub & Project**: For AI/ML workloads
- **Model Deployments**: GPT-4o and text-embedding-3-small
- **PostgreSQL Flexible Server**: With pgvector extension support
- **Application Insights**: For monitoring and telemetry
- **Storage Account**: For AI Foundry data storage
- **Key Vault**: For secure credential management

## Post-Deployment

1. **Database Access**: The PostgreSQL server is configured with firewall rules for your current IP
2. **AI Services**: Access the AI Foundry hub through the Azure portal
3. **Monitoring**: View metrics and logs in Application Insights

## Troubleshooting

### AI Model Quota Issues

If you encounter quota limit errors during deployment, you may need to clean up existing model deployments:

```powershell
# List all Cognitive Services accounts (including soft-deleted ones)
az cognitiveservices account list --query "[].{Name:name, Location:location, ResourceGroup:resourceGroup, Kind:kind}"

# List model deployments in a specific Cognitive Services account
az cognitiveservices account deployment list --name <cognitive-services-account-name> --resource-group <resource-group-name>

# Delete a specific model deployment
az cognitiveservices account deployment delete --name <deployment-name> --resource-group <resource-group-name> --account-name <cognitive-services-account-name>

# Check current quota usage
az cognitiveservices usage list --location <location> --subscription <subscription-id>
```

### Purging Soft-Deleted AI Models and Accounts

AI models and Cognitive Services accounts are soft-deleted and count against quota even after deletion:

```powershell
# List account names and locations of soft-deleted accounts
az cognitiveservices account list-deleted --query "[].{Name:name, Location:location}" --output table

# Purge a soft-deleted Cognitive Services account (permanently removes it)
az cognitiveservices account purge `
  --location "westus" `
  --resource-group "rg-zava-agent-wks-$UNIQUE_SUFFIX" `
  --name <cognitive-services-account-name>

# Alternative: Use REST API to purge soft-deleted account
az rest --method delete `
  --url "https://management.azure.com/subscriptions/<subscription-id>/providers/Microsoft.CognitiveServices/locations/<location>/resourceGroups/<resource-group>/deletedAccounts/<account-name>?api-version=2021-04-30"
```

**Important Notes:**

- Soft-deleted resources still count against your quota limits
- Purging permanently deletes the resource and cannot be undone
- You may need to wait 48-72 hours after purging before quota is fully released
- If you're still hitting quota limits, consider requesting a quota increase through the Azure portal

### Purging Existing Cognitive Services Resources

If you encounter quota limits or need to clean up soft-deleted Cognitive Services resources, you can purge them using:

```powershell
# List deleted Cognitive Services accounts
az cognitiveservices account list-deleted --query "[].{Name:name, Location:location}" --output table

# Purge a specific deleted account (replace with your subscription ID, location, and resource name)
az cognitiveservices account purge `
  --location "West US" `
  --resource-group "rg-zava-agent-wks-$UNIQUE_SUFFIX" `
  --name your-cognitiveservices-account-name
```

**Note**: Purging permanently deletes the resource and cannot be undone. This is typically needed when redeploying with the same resource names or when hitting subscription quotas.

## Cleanup

### Delete All Resources (Recommended)

To remove all deployed resources at once:

```powershell
# Delete the entire resource group (removes all contained resources)
az group delete --name "rg-zava-agent-wks-$UNIQUE_SUFFIX" --yes --no-wait
```

### Delete Individual Resources (If Needed)

If you need to delete specific resources while keeping others:

```powershell
# Delete AI Foundry resources
az ml workspace delete --name <workspace-name> --resource-group "rg-zava-agent-wks-$UNIQUE_SUFFIX"
az cognitiveservices account delete --name <ai-services-name> --resource-group "rg-zava-agent-wks-$UNIQUE_SUFFIX"

# Delete PostgreSQL server
az postgres flexible-server delete --name <postgres-server-name> --resource-group "rg-zava-agent-wks-$UNIQUE_SUFFIX" --yes

# Delete storage account
az storage account delete --name <storage-account-name> --resource-group "rg-zava-agent-wks-$UNIQUE_SUFFIX" --yes

# Delete Application Insights
az monitor app-insights component delete --app <app-insights-name> --resource-group "rg-zava-agent-wks-$UNIQUE_SUFFIX"

# Delete Key Vault (with purge protection)
az keyvault delete --name <keyvault-name> --resource-group "rg-zava-agent-wks-$UNIQUE_SUFFIX"
az keyvault purge --name <keyvault-name> --location "West US"
```

### Verify Cleanup

```powershell
# Check if resource group is empty
az resource list --resource-group "rg-zava-agent-wks-$UNIQUE_SUFFIX"

# Check for any remaining Cognitive Services (soft-deleted)
az cognitiveservices account list-deleted

# Check for any remaining Key Vaults (soft-deleted)
az keyvault list-deleted
```

**Note**: Some Azure services (like Cognitive Services and Key Vault) have soft-delete protection. Use the purge commands from the Troubleshooting section if you need to permanently remove them.
