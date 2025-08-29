Write-Host "Deploying the Azure resources..."

# --- Parameters (match deploy.sh) ---
$RG_LOCATION = "westus"
$AI_PROJECT_FRIENDLY_NAME = "Zava Agent Service Workshop"
$RESOURCE_PREFIX = "zava-agent-wks"
# unique suffix: lowercase letters + digits, 4 chars (similar to deploy.sh)
$UNIQUE_SUFFIX = -join ((97..122) + (48..57) | Get-Random -Count 4 | ForEach-Object { [char]$_ })

Write-Host "Creating agent workshop resources in resource group: rg-$RESOURCE_PREFIX-$UNIQUE_SUFFIX"
$DEPLOYMENT_NAME = "azure-ai-agent-service-lab-$(Get-Date -Format 'yyyyMMddHHmmss')"

Write-Host "Starting Azure deployment..."
az deployment sub create \
  --name "$DEPLOYMENT_NAME" \
  --location "$RG_LOCATION" \
  --template-file main.bicep \
  --parameters @main.parameters.json \
  --parameters location="$RG_LOCATION" \
  --parameters resourcePrefix="$RESOURCE_PREFIX" \
  --parameters uniqueSuffix="$UNIQUE_SUFFIX" \
  --output json | Out-File -FilePath output.json -Encoding utf8

if ($LASTEXITCODE -ne 0) {
    Write-Host "Deployment failed. Check output.json for details." -ForegroundColor Red
    exit 1
}

if (-not (Test-Path -Path output.json)) {
    Write-Host "Error: output.json not found." -ForegroundColor Red
    exit 1
}

try {
    $jsonData = Get-Content output.json -Raw | ConvertFrom-Json
} catch {
    Write-Host "Failed to parse output.json" -ForegroundColor Red
    Write-Host $_.Exception.Message
    exit 1
}

$outputs = $jsonData.properties.outputs

$PROJECTS_ENDPOINT = $outputs.projectsEndpoint.value
$RESOURCE_GROUP_NAME = $outputs.resourceGroupName.value
$SUBSCRIPTION_ID = $outputs.subscriptionId.value
$AI_FOUNDRY_NAME = $outputs.aiFoundryName.value
$AI_PROJECT_NAME = $outputs.aiProjectName.value
$AZURE_OPENAI_ENDPOINT = ($PROJECTS_ENDPOINT -replace 'api/projects/.*$','')
$APPLICATIONINSIGHTS_CONNECTION_STRING = $outputs.applicationInsightsConnectionString.value
$APPLICATION_INSIGHTS_NAME = $outputs.applicationInsightsName.value

if ([string]::IsNullOrEmpty($PROJECTS_ENDPOINT) -or $PROJECTS_ENDPOINT -eq 'null') {
    Write-Host "Error: projectsEndpoint not found. Possible deployment failure." -ForegroundColor Red
    exit 1
}

# Write .env for workshop (overwrite)
$ENV_FILE_PATH = "../src/python/workshop/.env"

# Ensure directory exists
$envDir = Split-Path -Parent $ENV_FILE_PATH
if (-not (Test-Path $envDir)) { New-Item -ItemType Directory -Path $envDir -Force | Out-Null }

if (Test-Path $ENV_FILE_PATH) { Remove-Item -Path $ENV_FILE_PATH -Force }

@"
PROJECT_ENDPOINT=$PROJECTS_ENDPOINT
AZURE_OPENAI_ENDPOINT=$AZURE_OPENAI_ENDPOINT
GPT_MODEL_DEPLOYMENT_NAME="gpt-4o-mini"
EMBEDDING_MODEL_DEPLOYMENT_NAME="text-embedding-3-small"
APPLICATIONINSIGHTS_CONNECTION_STRING="$APPLICATIONINSIGHTS_CONNECTION_STRING"
AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED="true"
"@ | Out-File -FilePath $ENV_FILE_PATH -Encoding utf8

# Write resources summary
$RESOURCES_FILE_PATH = "../src/python/workshop/resources.txt"
$resDir = Split-Path -Parent $RESOURCES_FILE_PATH
if (-not (Test-Path $resDir)) { New-Item -ItemType Directory -Path $resDir -Force | Out-Null }
if (Test-Path $RESOURCES_FILE_PATH) { Remove-Item -Path $RESOURCES_FILE_PATH -Force }

@(
  "Azure AI Foundry Resources:",
  "- Resource Group Name: $RESOURCE_GROUP_NAME",
  "- AI Project Name: $AI_PROJECT_NAME",
  "- Foundry Resource Name: $AI_FOUNDRY_NAME",
  "- Application Insights Name: $APPLICATION_INSIGHTS_NAME"
) | Out-File -FilePath $RESOURCES_FILE_PATH -Encoding utf8

# Set C# project user-secrets if project exists (match deploy.sh path)
$CSHARP_PROJECT_PATH = "../src/csharp/McpAgentWorkshop.AppHost/McpAgentWorkshop.AppHost.csproj"
if (Test-Path $CSHARP_PROJECT_PATH) {
    dotnet user-secrets set "Parameters:FoundryEndpoint" "$PROJECTS_ENDPOINT" --project "$CSHARP_PROJECT_PATH"
    dotnet user-secrets set "Parameters:ChatModelDeploymentName" "gpt-4o-mini" --project "$CSHARP_PROJECT_PATH"
    dotnet user-secrets set "Parameters:EmbeddingModelDeploymentName" "text-embedding-3-small" --project "$CSHARP_PROJECT_PATH"
    dotnet user-secrets set "Parameters:AzureOpenAIEndpoint" "$AZURE_OPENAI_ENDPOINT" --project "$CSHARP_PROJECT_PATH"
    dotnet user-secrets set "Parameters:FoundryProjectName" "$AI_PROJECT_NAME" --project "$CSHARP_PROJECT_PATH"
    dotnet user-secrets set "Parameters:FoundryResourceName" "$AI_FOUNDRY_NAME" --project "$CSHARP_PROJECT_PATH"
    dotnet user-secrets set "Parameters:ResourceGroupName" "$RESOURCE_GROUP_NAME" --project "$CSHARP_PROJECT_PATH"
    dotnet user-secrets set "Parameters:ApplicationInsightsName" "$APPLICATION_INSIGHTS_NAME" --project "$CSHARP_PROJECT_PATH"
    dotnet user-secrets set "Azure:ResourceGroup" "$RESOURCE_GROUP_NAME" --project "$CSHARP_PROJECT_PATH"
    dotnet user-secrets set "Azure:Location" "$RG_LOCATION" --project "$CSHARP_PROJECT_PATH"
    dotnet user-secrets set "Azure:SubscriptionId" "$SUBSCRIPTION_ID" --project "$CSHARP_PROJECT_PATH"
    dotnet user-secrets set "Parameters:UniqueSuffix" "$UNIQUE_SUFFIX" --project "$CSHARP_PROJECT_PATH"
}

# Clean up output.json
Remove-Item -Path output.json -ErrorAction SilentlyContinue

Write-Host "Adding Azure AI Developer user role"

# Role assignments
$subId = az account show --query id --output tsv
$objectId = az ad signed-in-user show --query id -o tsv

Write-Host "Ensuring Azure AI Developer role assignment..."
try {
    $roleResult = az role assignment create \
      --role "Azure AI Developer" \
      --assignee "$objectId" \
      --scope "/subscriptions/$subId/resourceGroups/$RESOURCE_GROUP_NAME/providers/Microsoft.CognitiveServices/accounts/$AI_FOUNDRY_NAME" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Azure AI Developer role assignment created successfully."
    } elseif ($roleResult -match 'RoleAssignmentExists|already exists') {
        Write-Host "✅ Azure AI Developer role assignment already exists."
    } else {
        Write-Host "❌ User role assignment failed with unexpected error:"; Write-Host $roleResult; exit 1
    }
} catch {
    $err = $_.Exception.Message
    if ($err -match 'RoleAssignmentExists|already exists') {
        Write-Host "✅ Azure AI Developer role assignment already exists."
    } else {
        Write-Host "❌ User role assignment failed: $err"; exit 1
    }
}

Write-Host "Ensuring Azure AI User role assignment..."
$roleResultUser = az role assignment create \
  --assignee "$objectId" \
  --role "Azure AI User" \
  --scope "/subscriptions/$subId/resourceGroups/$RESOURCE_GROUP_NAME"
Write-Host "Role assignment result: $roleResultUser"

Write-Host "Ensuring Azure AI Project Manager role assignment..."
$roleResultManager = az role assignment create \
  --assignee "$objectId" \
  --role "Azure AI Project Manager" \
  --scope "/subscriptions/$subId/resourceGroups/$RESOURCE_GROUP_NAME"
Write-Host "Role assignment result: $roleResultManager"

Write-Host ""
Write-Host "🎉 Deployment completed successfully!"
Write-Host ""
Write-Host "📋 Resource Information:"
Write-Host "  Resource Group: $RESOURCE_GROUP_NAME"
Write-Host "  AI Project: $AI_PROJECT_NAME"
Write-Host "  Foundry Resource: $AI_FOUNDRY_NAME"
Write-Host "  Application Insights: $APPLICATION_INSIGHTS_NAME"
Write-Host ""
