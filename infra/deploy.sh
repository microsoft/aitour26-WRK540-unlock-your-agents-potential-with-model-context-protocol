#!/bin/bash

echo "Deploying the Azure resources..."

# Define resource group parameters
RG_LOCATION="westus"
AI_PROJECT_FRIENDLY_NAME="Zava Agent Service Workshop"
RESOURCE_PREFIX="zava-agent-wks"
UNIQUE_SUFFIX=$(head /dev/urandom | tr -dc a-z0-9 | head -c 4)

# Deploy the Azure resources and save output to JSON
echo -e "\033[1;37;41m Creating agent workshop resources in resource group: rg-$RESOURCE_PREFIX-$UNIQUE_SUFFIX \033[0m"
echo "Starting Azure deployment..."
DEPLOYMENT_NAME="azure-ai-agent-service-lab-$(date +%Y%m%d%H%M%S)"
az deployment sub create \
  --name "$DEPLOYMENT_NAME" \
  --location "$RG_LOCATION" \
  --template-file main.bicep \
  --parameters @main.parameters.json \
  --parameters location="$RG_LOCATION" \
  --parameters resourcePrefix="$RESOURCE_PREFIX" \
  --parameters uniqueSuffix="$UNIQUE_SUFFIX" \
  --output json > output.json

# Check if deployment was successful
if [ $? -ne 0 ]; then
  echo "Deployment failed. Check output.json for details."
  exit 1
fi

# Parse the JSON file
if [ ! -f output.json ]; then
  echo "Error: output.json not found."
  exit 1
fi

PROJECTS_ENDPOINT=$(jq -r '.properties.outputs.projectsEndpoint.value' output.json)
RESOURCE_GROUP_NAME=$(jq -r '.properties.outputs.resourceGroupName.value' output.json)
SUBSCRIPTION_ID=$(jq -r '.properties.outputs.subscriptionId.value' output.json)
AI_FOUNDRY_NAME=$(jq -r '.properties.outputs.aiFoundryName.value' output.json)
AI_PROJECT_NAME=$(jq -r '.properties.outputs.aiProjectName.value' output.json)
AZURE_OPENAI_ENDPOINT=$(jq -r '.properties.outputs.projectsEndpoint.value' output.json | sed 's|api/projects/.*||')
APPLICATIONINSIGHTS_CONNECTION_STRING=$(jq -r '.properties.outputs.applicationInsightsConnectionString.value' output.json)
APPLICATION_INSIGHTS_NAME=$(jq -r '.properties.outputs.applicationInsightsName.value' output.json)

if [ -z "$PROJECTS_ENDPOINT" ] || [ "$PROJECTS_ENDPOINT" = "null" ]; then
  echo "Error: projectsEndpoint not found. Possible deployment failure."
  exit 1
fi

ENV_FILE_PATH="../src/python/workshop/.env"

# Delete the file if it exists
[ -f "$ENV_FILE_PATH" ] && rm "$ENV_FILE_PATH"

# Create workshop directory if it doesn't exist
mkdir -p "$(dirname "$ENV_FILE_PATH")"

# Write to the workshop .env file
{
  echo "PROJECT_ENDPOINT=$PROJECTS_ENDPOINT"
  echo "AZURE_OPENAI_ENDPOINT=$AZURE_OPENAI_ENDPOINT"
  echo "GPT_MODEL_DEPLOYMENT_NAME=\"gpt-4o-mini\""
  echo "EMBEDDING_MODEL_DEPLOYMENT_NAME=\"text-embedding-3-small\""
  echo "APPLICATIONINSIGHTS_CONNECTION_STRING=\"$APPLICATIONINSIGHTS_CONNECTION_STRING\""
  echo "DEV_TUNNEL_URL=\"\""
  echo "AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED=\"true\""
} > "$ENV_FILE_PATH"

RESOURCES_FILE_PATH="../src/python/workshop/resources.txt"

# Delete the file if it exists
[ -f "$RESOURCES_FILE_PATH" ] && rm "$RESOURCES_FILE_PATH"

# Create workshop directory if it doesn't exist
mkdir -p "$(dirname "$RESOURCES_FILE_PATH")"

# Write to the workshop .env file
{
  echo "Azure AI Foundry Resources:"
  echo "- Resource Group Name: $RESOURCE_GROUP_NAME"
  echo "- AI Project Name: $AI_PROJECT_NAME"
  echo "- Foundry Resource Name: $AI_FOUNDRY_NAME"
  echo "- Application Insights Name: $APPLICATION_INSIGHTS_NAME"
} > "$RESOURCES_FILE_PATH"

CSHARP_PROJECT_PATH="../src/csharp/McpAgentWorkshop.AppHost/McpAgentWorkshop.AppHost.csproj"

# Set the user secrets for the C# project (if the project exists)
if [ -f "$CSHARP_PROJECT_PATH" ]; then
  dotnet user-secrets set "Parameters:FoundryEndpoint" "$PROJECTS_ENDPOINT" --project "$CSHARP_PROJECT_PATH"
  dotnet user-secrets set "Parameters:ChatModelDeploymentName" "gpt-4o-mini" --project "$CSHARP_PROJECT_PATH"
  dotnet user-secrets set "Parameters:EmbeddingModelDeploymentName" "text-embedding-3-small" --project "$CSHARP_PROJECT_PATH"
  dotnet user-secrets set "ConnectionStrings:ApplicationInsights" "$APPLICATIONINSIGHTS_CONNECTION_STRING" --project "$CSHARP_PROJECT_PATH"
  dotnet user-secrets set "Parameters:AzureOpenAIEndpoint" "$AZURE_OPENAI_ENDPOINT" --project "$CSHARP_PROJECT_PATH"
fi

# Delete the output.json file
rm -f output.json

echo "Adding Azure AI Developer user role"

# Set Variables
subId=$(az account show --query id --output tsv)
objectId=$(az ad signed-in-user show --query id -o tsv)

echo "Ensuring Azure AI Developer role assignment..."

roleResult=$(az role assignment create \
  --role "Azure AI Developer" \
  --assignee "$objectId" \
  --scope "/subscriptions/$subId/resourceGroups/$RESOURCE_GROUP_NAME/providers/Microsoft.CognitiveServices/accounts/$AI_FOUNDRY_NAME")
echo "Role assignment result: $roleResult"

echo "Ensuring Azure AI User role assignment..."

# Azure AI User role
roleResultUser=$(az role assignment create \
  --assignee "$objectId" \
  --role "Azure AI User" \
  --scope "/subscriptions/$subId/resourceGroups/$RESOURCE_GROUP_NAME")
  echo "Role assignment result: $roleResultUser"

echo "Ensuring Azure AI Project Manager role assignment..."

# Azure AI Project Manager role
roleResultManager=$(az role assignment create \
  --assignee "$objectId" \
  --role "Azure AI Project Manager" \
  --scope "/subscriptions/$subId/resourceGroups/$RESOURCE_GROUP_NAME")
echo "Role assignment result: $roleResultManager"

exitCode=$?

# Check if it succeeded or if the role assignment already exists
if [ $exitCode -eq 0 ]; then
    echo "✅ Azure AI Developer role assignment created successfully."
elif echo "$roleResult" | grep -q "RoleAssignmentExists\|already exists"; then
    echo "✅ Azure AI Developer role assignment already exists."
else
    echo "❌ User role assignment failed with unexpected error:"
    echo "$roleResult"
    exit 1
fi

echo ""
echo "🎉 Deployment completed successfully!"
echo ""
echo "📋 Resource Information:"
echo "  Resource Group: $RESOURCE_GROUP_NAME"
echo "  AI Project: $AI_PROJECT_NAME"
echo "  Foundry Resource: $AI_FOUNDRY_NAME"
echo "  Application Insights: $APPLICATION_INSIGHTS_NAME"
echo ""
