// application-insights.bicep
// This file creates Application Insights resources for monitoring

// Parameters
@description('Name for the Application Insights resource')
param applicationInsightsName string

@description('Location for the Application Insights resource')
param location string

@description('Set of tags to apply to all resources.')
param tags object = {}

@description('Name of the Log Analytics workspace (optional)')
param logAnalyticsWorkspaceName string = ''

// Create Log Analytics workspace if not provided
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
  tags: tags
}

// Reference existing Log Analytics workspace if provided
resource existingLogAnalyticsWorkspace 'Microsoft.OperationalInsights/workspaces@2023-09-01' existing = if (!empty(logAnalyticsWorkspaceName)) {
  name: logAnalyticsWorkspaceName
}

// Create Application Insights
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
  tags: tags
}

// Outputs
output applicationInsightsId string = applicationInsights.id
output applicationInsightsName string = applicationInsights.name
output instrumentationKey string = applicationInsights.properties.InstrumentationKey
output connectionString string = applicationInsights.properties.ConnectionString
output logAnalyticsWorkspaceId string = empty(logAnalyticsWorkspaceName) ? logAnalyticsWorkspace.id : existingLogAnalyticsWorkspace.id
