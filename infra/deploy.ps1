Write-Host "Deploying the Azure resources..."

# Define resource group parameters
$RG_LOCATION = "westus"
$AI_PROJECT_FRIENDLY_NAME = "Zava DIY Agent Service Workshop"
$RESOURCE_PREFIX = "zava-agent-wks"
$UNIQUE_SUFFIX = -join ((65..90) + (97..122) | Get-Random -Count 4 | ForEach-Object { [char]$_ })

# Deploy the Azure resources and save output to JSON
Write-Host " Creating agent workshop resources in resource group: rg-$RESOURCE_PREFIX-$UNIQUE_SUFFIX " -BackgroundColor Red -ForegroundColor White
$deploymentName = "azure-ai-agent-service-lab-$(Get-Date -Format 'yyyyMMddHHmmss')"
az deployment sub create `
  --name "$deploymentName" `
  --location "$RG_LOCATION" `
  --template-file main.bicep `
  --parameters "@main.parameters.json" `
  --parameters location="$RG_LOCATION" `
  --parameters resourcePrefix="$RESOURCE_PREFIX" `
  --parameters uniqueSuffix="$UNIQUE_SUFFIX" | Out-File -FilePath output.json -Encoding utf8

# Parse the JSON file using native PowerShell cmdlets
if (-not (Test-Path -Path output.json)) {
    Write-Host "Error: output.json not found."
    exit -1
}

$jsonData = Get-Content output.json -Raw | ConvertFrom-Json
$outputs = $jsonData.properties.outputs

# Extract values from the JSON object
$projectsEndpoint = $outputs.projectsEndpoint.value
$resourceGroupName = $outputs.resourceGroupName.value
$subscriptionId = $outputs.subscriptionId.value
$aiFoundryName = $outputs.aiFoundryName.value
$aiProjectName = $outputs.aiProjectName.value
$azureOpenAIEndpoint = $projectsEndpoint -replace 'api/projects/.*$', ''
$applicationInsightsConnectionString = $outputs.applicationInsightsConnectionString.value
$applicationInsightsName = $outputs.applicationInsightsName.value

if ([string]::IsNullOrEmpty($projectsEndpoint)) {
    Write-Host "Error: projectsEndpoint not found. Possible deployment failure."
    exit -1
}

# Set the path for the .env file
$ENV_FILE_PATH = "../src/python/workshop/.env"

# Create workshop directory if it doesn't exist
$workshopDir = Split-Path -Parent $ENV_FILE_PATH
if (-not (Test-Path $workshopDir)) {
    New-Item -ItemType Directory -Path $workshopDir -Force
}

# Delete the file if it exists
if (Test-Path $ENV_FILE_PATH) {
    Remove-Item -Path $ENV_FILE_PATH -Force
}

# Create a new workshop .env file and write to it
@"
PROJECT_ENDPOINT=$projectsEndpoint
GPT_MODEL_DEPLOYMENT_NAME="gpt-4o-mini"
EMBEDDING_MODEL_DEPLOYMENT_NAME="text-embedding-3-small"
APPLICATIONINSIGHTS_CONNECTION_STRING="$applicationInsightsConnectionString"
"@ | Set-Content -Path $ENV_FILE_PATH


# Set the path for the .resources.txt file
$RESOURCES_FILE_PATH = "../src/python/workshop/resources.txt"

# Create workshop directory if it doesn't exist
$workshopDir = Split-Path -Parent $RESOURCES_FILE_PATH
if (-not (Test-Path $workshopDir)) {
    New-Item -ItemType Directory -Path $workshopDir -Force
}

# Delete the file if it exists
if (Test-Path $RESOURCES_FILE_PATH) {
    Remove-Item -Path $RESOURCES_FILE_PATH -Force
}

# Create a new workshop .env file and write to it
@"
Resource Information:
- Resource Group Name: $resourceGroupName
- AI Project Name: $aiProjectName
- Foundry Resource Name: $aiFoundryName"
- Application Insights Name: $applicationInsightsName
"@ | Set-Content -Path $RESOURCES_FILE_PATH

# # Create fresh root .env file (always overwrite)
# $ROOT_ENV_FILE_PATH = "../.env"
# @"
# AZURE_OPENAI_ENDPOINT="$azureOpenAIEndpoint"
# PROJECT_ENDPOINT="$projectsEndpoint"
# GPT_MODEL_DEPLOYMENT_NAME="gpt-4o-mini"
# EMBEDDING_MODEL_DEPLOYMENT_NAME="text-embedding-3-small"
# APPLICATIONINSIGHTS_CONNECTION_STRING="$applicationInsightsConnectionString"
# DEV_TUNNEL_URL=""
# AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED="true"
# "@ | Set-Content -Path $ROOT_ENV_FILE_PATH

# Set the C# project path
$CSHARP_PROJECT_PATH = "../src/csharp/workshop/AgentWorkshop.Client/AgentWorkshop.Client.csproj"

# Set the user secrets for the C# project (if the project exists)
if (Test-Path $CSHARP_PROJECT_PATH) {
    dotnet user-secrets set "ConnectionStrings:AiAgentService" "$projectsEndpoint" --project "$CSHARP_PROJECT_PATH"
    dotnet user-secrets set "Azure:ModelName" "gpt-4o-mini" --project "$CSHARP_PROJECT_PATH"
}

# Delete the output.json file
Remove-Item -Path output.json -Force

Write-Host "Adding Azure AI Developer user role"

# Set Variables
$subId = az account show --query id --output tsv
$objectId = az ad signed-in-user show --query id -o tsv

Write-Host "Ensuring Azure AI Developer role assignment..."

# Try to create the role assignment and capture the result
try {
    $roleResult = az role assignment create `
                            --role "Azure AI Developer" `
                            --assignee "$objectId" `
                            --scope "/subscriptions/$subId/resourceGroups/$resourceGroupName/providers/Microsoft.CognitiveServices/accounts/$aiFoundryName" 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Azure AI Developer role assignment created successfully." -ForegroundColor Green
    }
    else {
        # Check if the error is about existing role assignment
        $errorOutput = $roleResult -join " "
        if ($errorOutput -match "RoleAssignmentExists|already exists") {
            Write-Host "✅ Azure AI Developer role assignment already exists." -ForegroundColor Green
        }
        else {
            Write-Host "❌ User role assignment failed with unexpected error:" -ForegroundColor Red
            Write-Host $errorOutput -ForegroundColor Red
            exit 1
        }
    }
}
catch {
    # Handle any PowerShell exceptions
    $errorMessage = $_.Exception.Message
    if ($errorMessage -match "RoleAssignmentExists|already exists") {
        Write-Host "✅ Azure AI Developer role assignment already exists." -ForegroundColor Green
    }
    else {
        Write-Host "❌ User role assignment failed: $errorMessage" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "🎉 Deployment completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Resource Information:" -ForegroundColor Cyan
Write-Host "  Resource Group: $resourceGroupName"
Write-Host "  AI Project: $aiProjectName"
Write-Host "  Foundry Resource: $aiFoundryName"
Write-Host "  Application Insights: $applicationInsightsName"
Write-Host ""
