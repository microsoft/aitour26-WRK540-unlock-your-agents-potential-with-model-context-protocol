# Deploy to Azure

This repository contains Azure infrastructure templates for deploying AI Foundry services.

## Prerequisites

- Azure CLI installed and logged in
- Appropriate Azure subscription permissions
- PostgreSQL client (`psql`) for database initialization
  - **macOS**: `brew install postgresql`
  - **Windows**: Download from https://www.postgresql.org/download/windows/
  - **Linux**: `sudo apt-get install postgresql-client` (Ubuntu/Debian) or `sudo yum install postgresql` (RHEL/CentOS)

## Configuration

**First, generate a random 8-character suffix:**

```powershell
$chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
$UNIQUE_SUFFIX = -join ((1..8) | ForEach { $chars[(Get-Random -Maximum $chars.Length)] })
Write-Host "Your unique suffix: $UNIQUE_SUFFIX"
```

### Required Parameters

The following parameters are passed directly on the command line:

- **location**: Azure region for deployment (e.g., "westus")
- **uniqueSuffix**: Unique 8-character identifier (use the generated `$UNIQUE_SUFFIX` variable)

## Deployment Steps

### 1. Create Resource Group

```powershell
az group create --name "rg-zava-agent-wks-$UNIQUE_SUFFIX" --location "West US"
```

### 2. Deploy Infrastructure

### ARM Deployment

From the command line, change to the ARM folder.

Run the following command to deploy the ARM template:

```powershell
az deployment group create `
  --name contoso-agent-deployment-$UNIQUE_SUFFIX `
  --resource-group "rg-zava-agent-wks-$UNIQUE_SUFFIX" `
  --template-file template.json `
  --parameters components_appi_name="appi-zava-agent-wks-$UNIQUE_SUFFIX" `
  --parameters accounts_fdy_name="fdy-zava-agent-wks-$UNIQUE_SUFFIX" `
  --parameters flexibleServers_pg_name="pg-zava-agent-wks-$UNIQUE_SUFFIX" `
  --parameters workspaces_law_appi_name="law-appi-zava-agent-wks-$UNIQUE_SUFFIX" `
  --parameters projectName="prj-zava-agent-wks-$UNIQUE_SUFFIX" `
  --parameters administratorLoginPassword="YourSecurePassword123!"
```

### Bicep Deployment

```powershell
az deployment group create `
  --resource-group "rg-contoso-agent-workshop-$UNIQUE_SUFFIX" `
  --template-file skillable.bicep `
  --parameters uniqueSuffix="$UNIQUE_SUFFIX"
```

### Infrastructure Components

The ARM template deploys:

- **AI Foundry Hub & Project**: For AI/ML workloads
- **Model Deployments**: GPT-4o-mini and text-embedding-3-small
- **PostgreSQL Flexible Server**: Database with security configurations
- **Log Analytics Workspace**: For monitoring and logging
- **Application Insights**: For application monitoring

## Post-Deployment

1. **AI Services**: Access the AI Foundry hub through the Azure portal

## Troubleshooting

### PostgreSQL Client (`psql`) Not Found

If you get "Error: psql not found in PATH" when running the database initialization script:

**macOS (Homebrew):**
```bash
# Install PostgreSQL client
brew install postgresql

# Verify installation (in bash/zsh)
psql --version

# If still not found, add to PATH in bash/zsh
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**macOS (PowerShell):**
```powershell
# Add PostgreSQL 17 to PATH for current PowerShell session
$env:PATH += ":/opt/homebrew/Cellar/postgresql@17/17.6/bin"

# Verify installation
psql --version

# Make permanent by adding to PowerShell profile
if (!(Test-Path $PROFILE)) { New-Item -Type File -Path $PROFILE -Force }
Add-Content $PROFILE '$env:PATH += ":/opt/homebrew/Cellar/postgresql@17/17.6/bin"'
```

**Windows:**
1. Download PostgreSQL from <https://www.postgresql.org/download/windows/>
2. Or use package managers:
   ```powershell
   # Using Chocolatey
   choco install postgresql
   
   # Using Scoop
   scoop install postgresql
   ```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt-get update && sudo apt-get install postgresql-client

# CentOS/RHEL/Fedora
sudo yum install postgresql
# or: sudo dnf install postgresql
```

**Alternative: Use Azure Cloud Shell**
If you prefer not to install PostgreSQL locally, use Azure Cloud Shell at <https://shell.azure.com> which has `psql` pre-installed.

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
az cognitiveservices account list-deleted --output json | jq -r '.[] | "\(.name)\t\(.location)\t\(.id | split("/")[8])"' | column -t -s $'\t' -N "Name,Location,ResourceGroup"

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
  --location "westus" `
  --resource-group "rg-zava-agent-wks-$UNIQUE_SUFFIX" `
  --name your-cognitiveservices-account-name

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
az cognitiveservices account delete --name <ai-services-name> --resource-group "rg-zava-agent-wks-$UNIQUE_SUFFIX"
```

### Verify Cleanup

```powershell
# Check if resource group is empty
az resource list --resource-group "rg-zava-agent-wks-$UNIQUE_SUFFIX"

# Check for any remaining Cognitive Services (soft-deleted)
az cognitiveservices account list-deleted
```

**Note**: Some Azure services (like Cognitive Services) have soft-delete protection. Use the purge commands from the Troubleshooting section if you need to permanently remove them.
