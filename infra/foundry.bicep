// ai-services.bicep
// This file contains the AI services resources for the agent workshop

// Parameters
@description('Name for the project')
param aiProjectName string

@description('Set of tags to apply to all resources.')
param tags object = {}

@description('Location for the Azure AI Foundry resource')
param location string

@description('Name of the Azure AI Foundry account')
@minLength(3)
@maxLength(24)
param foundryResourceName string

resource account 'Microsoft.CognitiveServices/accounts@2025-04-01-preview' = {
  name: foundryResourceName
  location: location
  sku: {
    name: 'S0'
  }
  kind: 'AIServices'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    apiProperties: {}
    allowProjectManagement: true
    customSubDomainName: foundryResourceName
    networkAcls: {
      defaultAction: 'Allow'
      virtualNetworkRules: []
      ipRules: []
    }
    publicNetworkAccess: 'Enabled'
    disableLocalAuth: true
    defaultProject: aiProjectName
    associatedProjects: [aiProjectName]
  }
  tags: tags
}

output accountName string = account.name
output endpoint string = account.properties.endpoints['AI Foundry API']
