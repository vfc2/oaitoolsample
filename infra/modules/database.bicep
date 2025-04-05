@description('The project name to use when naming resources.')
param projectName string

@description('The Principal ID of the AI Developers Entra group')
param aiDevelopersGroupPrincipalId string

resource sqlDatabaseServer 'Microsoft.Sql/servers@2024-05-01-preview' = {
    name: 'sql-${projectName}-001'
    location: resourceGroup().location
    identity: {
        type: 'SystemAssigned'
    }
    properties: {
        administrators: {
            administratorType: 'ActiveDirectory'
            azureADOnlyAuthentication: true
            principalType: 'Group'
            login: 'AI-Developers'
            sid: aiDevelopersGroupPrincipalId
        }
    }
}

resource sqlDatabase 'Microsoft.Sql/servers/databases@2024-05-01-preview' = {
    parent: sqlDatabaseServer
    name: 'sqldb-${projectName}-001'
    location: resourceGroup().location
    sku: {
        name: 'Basic'
        tier: 'Basic'
    }
    properties: {
        requestedBackupStorageRedundancy: 'Local'
    }
}

output sqlServerName string = sqlDatabaseServer.name
output sqlDatabaseName string = sqlDatabase.name
