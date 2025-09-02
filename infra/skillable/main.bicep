targetScope = 'resourceGroup'

// Parameters
@description('Location of the resources')
param location string

@description('Friendly name for your Azure AI resource')
param aiProjectFriendlyName string = 'Agents standard project resource'

@description('Description of your Azure AI resource displayed in Azure AI Foundry')
param aiProjectDescription string = 'Project resources required for the Zava Agent Workshop.'

@description('Set of tags to apply to all resources.')
param tags object = {}

@description('Array of models to deploy')
param models array = [
  {
    name: 'gpt-4o-mini'
    format: 'OpenAI'
    version: '2024-07-18'
    skuName: 'GlobalStandard'
    capacity: 120
  }
  {
    name: 'text-embedding-3-small'
    format: 'OpenAI'
    version: '1'
    skuName: 'GlobalStandard'
    capacity: 50
  }
]

@description('Unique suffix for the resources. Must be 8 characters long.')
@maxLength(8)
@minLength(8)
param uniqueSuffix string

@description('Name of the Log Analytics workspace (optional)')
param logAnalyticsWorkspaceName string = ''

// PostgreSQL Parameters
@description('PostgreSQL server name (will be prefixed with unique suffix if not provided)')
param postgresServerName string = ''

@description('PostgreSQL version')
param postgresVersion string = '17'

@description('PostgreSQL authentication type')
@allowed([
  'Password'
  'EntraOnly'
])
param postgresAuthType string = 'Password'

@description('PostgreSQL administrator login')
param postgresAdminLogin string = 'azureuser'

@description('PostgreSQL administrator password')
@secure()
param postgresAdminPassword string = ''

@description('PostgreSQL SKU configuration')
param postgresSku object = {
  name: 'Standard_B1ms'
  tier: 'Burstable'
}

@description('PostgreSQL storage configuration')
param postgresStorage object = {
  storageSizeGB: 32
  iops: 120
  autoGrow: 'Enabled'
  autoIoScaling: 'Enabled'
}

@description('Database names to create')
param postgresDatabaseNames array = ['defaultdb']

@description('Allow Azure IPs through firewall')
param postgresAllowAzureIPs bool = true

@description('Allow all IPs through firewall (not recommended for production)')
param postgresAllowAllIPs bool = false

@description('Specific IP addresses to allow')
param postgresAllowedIPs array = []

// Variables
var defaultTags = {
  source: 'Azure AI Foundry Agents Service lab'
}

var rootTags = union(defaultTags, tags)

// Calculate resource names
var aiProjectName = toLower('prj-zava-agent-wks-${uniqueSuffix}')
var foundryResourceName = toLower('fdy-zava-agent-wks-${uniqueSuffix}')
var applicationInsightsName = toLower('appi-zava-agent-wks-${uniqueSuffix}')
var postgresServerNameResolved = empty(postgresServerName) ? toLower('pg-zava-agent-wks-${uniqueSuffix}') : postgresServerName

// Log Analytics Workspace (created if not provided)
resource logAnalyticsWorkspace 'Microsoft.OperationalInsights/workspaces@2023-09-01' = if (empty(logAnalyticsWorkspaceName)) {
  name: 'law-${applicationInsightsName}'
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
    features: {
      searchVersion: 1
      legacy: 0
      enableLogAccessUsingOnlyResourcePermissions: true
    }
  }
  tags: rootTags
}

// Reference existing Log Analytics workspace if provided
resource existingLogAnalyticsWorkspace 'Microsoft.OperationalInsights/workspaces@2023-09-01' existing = if (!empty(logAnalyticsWorkspaceName)) {
  name: logAnalyticsWorkspaceName
}

// Application Insights
resource applicationInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: applicationInsightsName
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: empty(logAnalyticsWorkspaceName) ? logAnalyticsWorkspace.id : existingLogAnalyticsWorkspace.id
    IngestionMode: 'LogAnalytics'
    publicNetworkAccessForIngestion: 'Enabled'
    publicNetworkAccessForQuery: 'Enabled'
  }
  tags: rootTags
}

// Azure AI Foundry Account
resource foundryAccount 'Microsoft.CognitiveServices/accounts@2025-04-01-preview' = {
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
  tags: rootTags
}

// Azure AI Foundry Project
resource foundryProject 'Microsoft.CognitiveServices/accounts/projects@2025-04-01-preview' = {
  parent: foundryAccount
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
  tags: rootTags
}

// Model Deployments - Deploy one at a time to avoid conflicts
@batchSize(1)
resource modelDeployments 'Microsoft.CognitiveServices/accounts/deployments@2024-10-01' = [for (model, index) in models: {
  parent: foundryAccount
  name: model.name
  sku: {
    capacity: model.capacity
    name: model.skuName
  }
  properties: {
    model: {
      name: model.name
      format: model.format
      version: model.version
    }
    versionUpgradeOption: 'OnceNewDefaultVersionAvailable'
    currentCapacity: model.capacity
  }
  tags: rootTags
  dependsOn: [
    foundryProject
  ]
}]

// PostgreSQL Flexible Server
resource postgresServer 'Microsoft.DBforPostgreSQL/flexibleServers@2022-12-01' = {
  name: postgresServerNameResolved
  location: location
  tags: rootTags
  sku: postgresSku
  properties: {
    version: postgresVersion
    storage: postgresStorage
    highAvailability: {
      mode: 'Disabled'
    }
    administratorLogin: postgresAuthType == 'Password' ? postgresAdminLogin : null
    administratorLoginPassword: postgresAuthType == 'Password' ? postgresAdminPassword : null
  }

  resource database 'databases' = [for dbName in postgresDatabaseNames: {
    name: dbName
  }]
}

// PostgreSQL Firewall Rules
resource postgresFirewallAll 'Microsoft.DBforPostgreSQL/flexibleServers/firewallRules@2023-03-01-preview' = if (postgresAllowAllIPs) {
  parent: postgresServer
  name: 'allow-all-IPs'
  properties: {
    startIpAddress: '0.0.0.0'
    endIpAddress: '255.255.255.255'
  }
}

resource postgresFirewallAzure 'Microsoft.DBforPostgreSQL/flexibleServers/firewallRules@2023-03-01-preview' = if (postgresAllowAzureIPs) {
  parent: postgresServer
  name: 'allow-all-azure-internal-IPs'
  properties: {
    startIpAddress: '0.0.0.0'
    endIpAddress: '0.0.0.0'
  }
}

@batchSize(1)
resource postgresFirewallSingle 'Microsoft.DBforPostgreSQL/flexibleServers/firewallRules@2023-03-01-preview' = [for ip in postgresAllowedIPs: {
  parent: postgresServer
  name: 'allow-single-${replace(ip, '.', '')}'
  properties: {
    startIpAddress: ip
    endIpAddress: ip
  }
}]

resource postgresFirewallRange 'Microsoft.DBforPostgreSQL/flexibleServers/firewallRules@2023-03-01-preview' = {
  parent: postgresServer
  name: 'allow-range-103-177-0-0-to-103-177-255-255'
  properties: {
    startIpAddress: '103.177.0.0'
    endIpAddress: '103.177.255.255'
  }
}

// PostgreSQL Administrator (for Entra ID auth)
resource postgresAdministrator 'Microsoft.DBforPostgreSQL/flexibleServers/administrators@2023-03-01-preview' = if (postgresAuthType == 'EntraOnly') {
  parent: postgresServer
  name: deployer().objectId
  properties: {
    tenantId: subscription().tenantId
    principalType: 'User'
    principalName: deployer().userPrincipalName
  }
  dependsOn: [postgresFirewallAll, postgresFirewallAzure]
}

// PostgreSQL Configuration for vector extension
resource postgresConfiguration 'Microsoft.DBforPostgreSQL/flexibleServers/configurations@2023-03-01-preview' = {
  name: 'azure.extensions'
  parent: postgresServer
  properties: {
    value: 'vector'
    source: 'user-override'
  }
  dependsOn: [
    postgresAdministrator
    postgresFirewallAll
    postgresFirewallAzure
    postgresFirewallSingle
    postgresFirewallRange
  ]
}

// Outputs
output resourceGroupName string = resourceGroup().name
output aiFoundryName string = foundryAccount.name
output aiProjectName string = foundryProject.name
output projectsEndpoint string = '${foundryAccount.properties.endpoints['AI Foundry API']}api/projects/${foundryProject.name}'
output deployedModels array = [for (model, index) in models: {
  name: model.name
  deploymentName: modelDeployments[index].name
}]
output applicationInsightsName string = applicationInsights.name
output applicationInsightsConnectionString string = applicationInsights.properties.ConnectionString
output applicationInsightsInstrumentationKey string = applicationInsights.properties.InstrumentationKey
output applicationInsightsId string = applicationInsights.id
output logAnalyticsWorkspaceId string = empty(logAnalyticsWorkspaceName) ? logAnalyticsWorkspace.id : existingLogAnalyticsWorkspace.id

// PostgreSQL Outputs (only available when deployPostgres is true)
@description('PostgreSQL server name')
output postgresServerName string = postgresServerNameResolved

@description('PostgreSQL username')
output postgresUsername string = postgresAuthType == 'Password' ? postgresAdminLogin : deployer().userPrincipalName
