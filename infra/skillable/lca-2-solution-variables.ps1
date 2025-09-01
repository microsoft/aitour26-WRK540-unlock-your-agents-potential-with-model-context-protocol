# LCA Metadata
# Delay: 30 seconds

# =========================
# VM Life Cycle Action (PowerShell)
# Pull outputs from ARM/Bicep deployment and write .env
# =========================

# --- logging to both Skillable log + file ---
$logDir = "C:\logs"
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir | Out-Null }
$logFile = Join-Path $logDir "vm-init_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"
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

#######################################################
# Create .env

# --- Find deployment and read OUTPUTS (cannot use @lab ... Outputs[..]) ---
# Prefer RG-scope deployments (most common with Skillable templates)
$deployment = Get-AzResourceGroupDeployment -ResourceGroupName $ResourceGroup `
| Sort-Object Timestamp | Select-Object -First 1

if (-not $deployment) {
  Log "No RG-scope deployments found in $ResourceGroup. Trying subscription-scope..."
  $deployment = Get-AzDeployment | Sort-Object Timestamp -Descending | Select-Object -First 1
}

if (-not $deployment) {
  throw "Could not locate any ARM/Bicep deployments to read outputs from."
}

$scope = if ([string]::IsNullOrEmpty($deployment.Location)) { 'subscription' } else { $deployment.Location }
Log "Using deployment: $($deployment.DeploymentName) | Scope: $scope"

# $deployment.Outputs is already a PowerShell object (Dictionary)
$outs = $deployment.Outputs

# Expecting outputs named like your template:
# - projectsEndpoint
# - applicationInsightsConnectionString
$projectsEndpoint = $outs.projectsEndpoint.value
$applicationInsightsConnectionString = $outs.applicationInsightsConnectionString.value

if (-not $projectsEndpoint) { throw "Deployment output 'projectsEndpoint' not found." }
if (-not $applicationInsightsConnectionString) { throw "Deployment output 'applicationInsightsConnectionString' not found." }

Log "projectsEndpoint = $projectsEndpoint"
# (don’t log secrets/connection strings fully in real student labs)
Log "applicationInsightsConnectionString captured."

# --- Derive additional values for your app ---
$PostgresServerName = "pg-zava-agent-wks-$UniqueSuffix"
$AzurePgHost = "$PostgresServerName.postgres.database.azure.com"
$AzurePgPort = 5432

# If you keep these static for the workshop:
$GPT_MODEL_DEPLOYMENT_NAME = "gpt-4o-mini"
$EMBEDDING_MODEL_DEPLOYMENT_NAME = "text-embedding-3-small"

# Derive Azure OpenAI endpoint from Projects endpoint
$azureOpenAIEndpoint = $projectsEndpoint -replace 'api/projects/.*$', ''

# Example app DB URL (adjust creds/db if your app differs)
$PostgresUrl = "postgresql://store_manager:StoreManager123!@${AzurePgHost}:${AzurePgPort}/zava?sslmode=require"

$workshopRoot = "C:\Users\Admin\aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol\src"

# --- Write .env for your Python app ---
$ENV_FILE_PATH = Join-Path $workshopRoot "python\workshop\.env"
$workshopDir = Split-Path -Parent $ENV_FILE_PATH
if (-not (Test-Path $workshopDir)) { New-Item -ItemType Directory -Path $workshopDir -Force | Out-Null }
if (Test-Path $ENV_FILE_PATH) { Remove-Item -Path $ENV_FILE_PATH -Force }

@"

PROJECT_ENDPOINT="$projectsEndpoint"
AZURE_OPENAI_ENDPOINT="$azureOpenAIEndpoint"
GPT_MODEL_DEPLOYMENT_NAME="$GPT_MODEL_DEPLOYMENT_NAME"
EMBEDDING_MODEL_DEPLOYMENT_NAME="$EMBEDDING_MODEL_DEPLOYMENT_NAME"
APPLICATIONINSIGHTS_CONNECTION_STRING="$applicationInsightsConnectionString"
POSTGRES_URL="$PostgresUrl"
AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED="true"

"@ | Set-Content -Path $ENV_FILE_PATH -Encoding UTF8

Log "Created .env at $ENV_FILE_PATH"

# Read expected outputs with null checks for resources.txt
$aiFoundryName = if ($outs.aiFoundryName) { $outs.aiFoundryName.value } else { $null }
$aiProjectName = if ($outs.aiProjectName) { $outs.aiProjectName.value } else { $null }
$applicationInsightsName = if ($outs.applicationInsightsName) { $outs.applicationInsightsName.value } else { $null }

# Write resources summary
$RESOURCES_FILE_PATH = Join-Path $workshopDir "resources.txt"
if (Test-Path $RESOURCES_FILE_PATH) { Remove-Item -Path $RESOURCES_FILE_PATH -Force }

@(
  "Azure AI Foundry Resources:",
  "- Resource Group Name: $ResourceGroup",
  "- AI Project Name: $aiProjectName",
  "- Foundry Resource Name: $aiFoundryName",
  "- Application Insights Name: $applicationInsightsName"
) | Out-File -FilePath $RESOURCES_FILE_PATH -Encoding utf8

Log "Created resources.txt at $RESOURCES_FILE_PATH"

# --- Attempt to set .NET user-secrets for C# project (if present) ---
Log "Configure dotnet user-secrets on VM"

# Log what we found
Log "Deployment outputs - aiFoundryName: $aiFoundryName, aiProjectName: $aiProjectName, applicationInsightsName: $applicationInsightsName"

# C# project path (match deploy.ps1 relative project)
$CSHARP_PROJECT_PATH = Join-Path $workshopRoot "csharp\McpAgentWorkshop.AppHost\McpAgentWorkshop.AppHost.csproj"
$CSHARP_RESOURCES_FILE_PATH = Join-Path $workshopRoot "csharp\resources.txt"

# Write resources summary for C# project
if (Test-Path $CSHARP_RESOURCES_FILE_PATH) { Remove-Item -Path $CSHARP_RESOURCES_FILE_PATH -Force }

@(
  "Azure AI Foundry Resources:",
  "- Resource Group Name: $ResourceGroup",
  "- AI Project Name: $aiProjectName",
  "- Foundry Resource Name: $aiFoundryName",
  "- Application Insights Name: $applicationInsightsName"
) | Out-File -FilePath $CSHARP_RESOURCES_FILE_PATH -Encoding utf8

Log "Created C# resources.txt at $CSHARP_RESOURCES_FILE_PATH"

if (Test-Path $CSHARP_PROJECT_PATH) {
  Log "Found C# project at $CSHARP_PROJECT_PATH; setting user-secrets"

  # Validate required values before setting secrets
  if (-not $aiFoundryName -or -not $aiProjectName -or -not $applicationInsightsName) {
    Log "Warning: Some deployment outputs are missing. Continuing with available values..."
  }

  Log "Setting user-secret: Parameters:FoundryEndpoint"
  dotnet user-secrets set "Parameters:FoundryEndpoint" "$projectsEndpoint" --project "$CSHARP_PROJECT_PATH"
  
  Log "Setting user-secret: Parameters:ChatModelDeploymentName"
  dotnet user-secrets set "Parameters:ChatModelDeploymentName" $GPT_MODEL_DEPLOYMENT_NAME --project "$CSHARP_PROJECT_PATH"
  
  Log "Setting user-secret: Parameters:EmbeddingModelDeploymentName"
  dotnet user-secrets set "Parameters:EmbeddingModelDeploymentName" $EMBEDDING_MODEL_DEPLOYMENT_NAME --project "$CSHARP_PROJECT_PATH"
  
  Log "Setting user-secret: Parameters:AzureOpenAIEndpoint"
  dotnet user-secrets set "Parameters:AzureOpenAIEndpoint" "$azureOpenAIEndpoint" --project "$CSHARP_PROJECT_PATH"
  
  # Only set these if they have values
  if ($aiProjectName) {
    Log "Setting user-secret: Parameters:FoundryProjectName"
    dotnet user-secrets set "Parameters:FoundryProjectName" "$aiProjectName" --project "$CSHARP_PROJECT_PATH"
  }
  else {
    Log "Skipping Parameters:FoundryProjectName - aiProjectName is null/empty"
  }
  
  if ($aiFoundryName) {
    Log "Setting user-secret: Parameters:FoundryResourceName"
    dotnet user-secrets set "Parameters:FoundryResourceName" "$aiFoundryName" --project "$CSHARP_PROJECT_PATH"
  }
  else {
    Log "Skipping Parameters:FoundryResourceName - aiFoundryName is null/empty"
  }
  
  if ($applicationInsightsName) {
    Log "Setting user-secret: Parameters:ApplicationInsightsName"
    dotnet user-secrets set "Parameters:ApplicationInsightsName" "$applicationInsightsName" --project "$CSHARP_PROJECT_PATH"
  }
  else {
    Log "Skipping Parameters:ApplicationInsightsName - applicationInsightsName is null/empty"
  }
  
  Log "Setting user-secret: Parameters:ResourceGroupName"
  dotnet user-secrets set "Parameters:ResourceGroupName" "$ResourceGroup" --project "$CSHARP_PROJECT_PATH"
  
  Log "Setting user-secret: Parameters:PostgresName"
  dotnet user-secrets set "Parameters:PostgresName" "$PostgresServerName" --project "$CSHARP_PROJECT_PATH"

  Log "Setting user-secret: Azure:ResourceGroup"
  dotnet user-secrets set "Azure:ResourceGroup" "$ResourceGroup" --project "$CSHARP_PROJECT_PATH"
  
  # Use deployment location if available; fall back to westus
  $deployLocation = if ($deployment.Location) { $deployment.Location } else { "westus" }
  Log "Setting user-secret: Azure:Location (value: $deployLocation)"
  dotnet user-secrets set "Azure:Location" "$deployLocation" --project "$CSHARP_PROJECT_PATH"
  
  Log "Setting user-secret: Azure:SubscriptionId"
  dotnet user-secrets set "Azure:SubscriptionId" "$SubId" --project "$CSHARP_PROJECT_PATH"

  Log "Setting ConnectionStrings:Postgres"
  $pgConnectionString = "Host=$AzurePgHost;Port=$AzurePgPort;Database=zava;Username=store_manager;Password=StoreManager123!;SSL Mode=Require;Trust Server Certificate=true;"
  dotnet user-secrets set "ConnectionStrings:Postgres" "$pgConnectionString" --project "$CSHARP_PROJECT_PATH"

  Log "Setting Parameters:UniqueSuffix"
  dotnet user-secrets set "Parameters:UniqueSuffix" "$UniqueSuffix" --project "$CSHARP_PROJECT_PATH"
}
else {
  Log "C# project not found at expected location: $CSHARP_PROJECT_PATH. Skipping user-secrets configuration."
}

Log "VM LCA complete."