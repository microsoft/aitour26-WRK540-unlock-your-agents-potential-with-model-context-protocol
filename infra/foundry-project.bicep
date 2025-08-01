@description('Name of the Azure AI Foundry account')
@minLength(3)
@maxLength(24)
param foundryResourceName string

@description('Name for the project')
param aiProjectName string

@description('Friendly name for your Azure AI resource')
param aiProjectFriendlyName string

@description('Description of your Azure AI resource dispayed in Azure AI Foundry')
param aiProjectDescription string

@description('Model deployment location. If you want to deploy an Azure AI resource/model in different location than the rest of the resources created.')
param location string

@description('Set of tags to apply to all resources.')
param tags object = {}

resource account 'Microsoft.CognitiveServices/accounts@2025-04-01-preview' existing = {
  name: foundryResourceName
}

resource project 'Microsoft.CognitiveServices/accounts/projects@2025-04-01-preview' = {
  parent: account
  name: aiProjectName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    description: aiProjectDescription
    displayName: aiProjectFriendlyName
    // Note: Direct Application Insights telemetry configuration is not yet supported 
    // in the current API version. Manual configuration required in Azure portal.
  }
  tags: tags
}

output aiProjectId string = project.id
output aiProjectName string = project.name
