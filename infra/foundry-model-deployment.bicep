@description('Name of the Azure AI Foundry account')
@minLength(3)
@maxLength(24)
param foundryResourceName string

@description('Model name for deployment')
param modelName string

@description('Model format for deployment')
param modelFormat string

@description('Model version for deployment')
param modelVersion string

@description('Model deployment SKU name')
param modelSkuName string

@description('Model deployment capacity')
param modelCapacity int

@description('Set of tags to apply to all resources.')
param tags object = {}

resource account 'Microsoft.CognitiveServices/accounts@2025-04-01-preview' existing = {
  name: foundryResourceName
}

resource modelDeployment 'Microsoft.CognitiveServices/accounts/deployments@2024-10-01' = {
  parent: account
  name: modelName
  sku: {
    capacity: modelCapacity
    name: modelSkuName
  }
  properties: {
    model: {
      name: modelName
      format: modelFormat
      version: modelVersion
    }
    versionUpgradeOption: 'OnceNewDefaultVersionAvailable'
    currentCapacity: modelCapacity
  }
  tags: tags
}

output modelDeploymentId string = modelDeployment.id
output modelDeploymentName string = modelDeployment.name
