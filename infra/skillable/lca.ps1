# =========================
# VM Life Cycle Action (PowerShell)
# Pull outputs from ARM/Bicep deployment and write .env
# =========================

# --- logging to both Skillable log + file ---
$logDir  = "C:\logs"
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir | Out-Null }
$logFile = Join-Path $logDir "vm-init_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"
"[$(Get-Date -Format s)] VM LCA start" | Tee-Object -FilePath $logFile

function Log { param([string]$m) $ts="[$(Get-Date -Format s)] $m"; $ts | Tee-Object -FilePath $logFile -Append }

# --- Skillable tokens / lab values ---
$UniqueSuffix  = "@lab.LabInstance.Id"
$TenantId      = "@lab.CloudSubscription.TenantId"
$AppId         = "@lab.CloudSubscription.AppId"
$Secret        = "@lab.CloudSubscription.AppSecret"
$SubId         = "@lab.CloudSubscription.Id"

# Resource group where your template deployed (via alias rg-zava-agent-wks)
$ResourceGroup = "@lab.CloudResourceGroup(rg-zava-agent-wks).Name"

# Template PARAMETER (✅ supported by Skillable token macros)
$AzurePgPassword = "@lab.CloudResourceTemplate(WRK540-AITour2026).Parameters[postgresAdminPassword]"

# --- Azure login (service principal) ---
Log "Authenticating to Azure tenant $TenantId, subscription $SubId"
$sec  = ConvertTo-SecureString $Secret -AsPlainText -Force
$cred = [pscredential]::new($AppId, $sec)
Connect-AzAccount -ServicePrincipal -Tenant $TenantId -Credential $cred -Subscription $SubId | Out-Null
$ctx = Get-AzContext
Log "Logged in as: $($ctx.Account) | Sub: $($ctx.Subscription.Name) ($($ctx.Subscription.Id))"


######################################################
# Foundry Roles

# $username = "@lab.CloudPortalCredential(User1).Username"

# New-AzRoleAssignment -SignInName $username -RoleDefinitionName "Azure AI Developer" -Scope "/subscriptions/$subId/resourceGroups/rg-agent-workshop"
# New-AzRoleAssignment -SignInName $username -RoleDefinitionName "Cognitive Services User" -Scope "/subscriptions/$subId"

######################################################
# Allow IP Address of Current Machine

$PostgresServerName = "pg-zava-agent-wks-$UniqueSuffix"
$ResourceGroup      = "@lab.CloudResourceGroup(rg-zava-agent-wks).Name"

$CurrentIP = (Invoke-RestMethod -Uri "https://api.ipify.org" -Method Get).Trim()
$RuleName  = "allow-current-ip-@lab.LabInstance.Id"
New-AzPostgreSqlFlexibleServerFirewallRule `
  -Name $RuleName `
  -ResourceGroupName $ResourceGroup `
  -ServerName $PostgresServerName `
  -StartIPAddress $CurrentIP `
  -EndIPAddress   $CurrentIP | Out-Null

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
$GPT_MODEL_DEPLOYMENT_NAME       = "gpt-4o-mini"
$EMBEDDING_MODEL_DEPLOYMENT_NAME = "text-embedding-3-small"

# Derive Azure OpenAI endpoint from Projects endpoint
$azureOpenAIEndpoint = $projectsEndpoint -replace 'api/projects/.*$',''

# Example app DB URL (adjust creds/db if your app differs)
$PostgresUrl = "postgresql://store_manager:StoreManager123!@${AzurePgHost}:${AzurePgPort}/zava?sslmode=require"

# --- Write .env for your Python app ---
$ENV_FILE_PATH = "C:\Users\Admin\aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol\src\python\workshop\.env"
$workshopDir   = Split-Path -Parent $ENV_FILE_PATH
if (-not (Test-Path $workshopDir)) { New-Item -ItemType Directory -Path $workshopDir -Force | Out-Null }
if (Test-Path $ENV_FILE_PATH) { Remove-Item -Path $ENV_FILE_PATH -Force }

@"
PROJECT_ENDPOINT="$projectsEndpoint"
AZURE_OPENAI_ENDPOINT="$azureOpenAIEndpoint"
GPT_MODEL_DEPLOYMENT_NAME="$GPT_MODEL_DEPLOYMENT_NAME"
EMBEDDING_MODEL_DEPLOYMENT_NAME="$EMBEDDING_MODEL_DEPLOYMENT_NAME"
APPLICATIONINSIGHTS_CONNECTION_STRING="$applicationInsightsConnectionString"
POSTGRES_URL="$PostgresUrl"
"@ | Set-Content -Path $ENV_FILE_PATH -Encoding UTF8

Log "Created .env at $ENV_FILE_PATH"
Log "VM LCA complete."