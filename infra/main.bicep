targetScope='subscription'

@description('The project name to use when naming resources.')
param projectName string

@description('The Principal ID of the AI Developers Entra group')
param aiDevelopersGroupPrincipalId string

resource resourceGroup 'Microsoft.Resources/resourceGroups@2024-11-01' = {
    name: 'rg-${projectName}-001'
    location: deployment().location
}

module openAi './modules/open-ai.bicep' = {
    name: 'openAiDeployment'
    scope: resourceGroup
    params: {
        projectName: projectName
    }
}

module database './modules/database.bicep' = {
    name: 'databaseDeployment'
    scope: resourceGroup
    params: {
        projectName: projectName
        aiDevelopersGroupPrincipalId: aiDevelopersGroupPrincipalId
    }
}

module roleAssignments './modules/role-assignments.bicep' = {
    name: 'roleAssignmentsDeployment'
    scope: resourceGroup
    params: {
        aiDevelopersGroupPrincipalId: aiDevelopersGroupPrincipalId
        openAiServiceName: openAi.outputs.openAiServiceName
    }
}

output openAiEndpoint string = openAi.outputs.openAiEndpoint
output dbConnectionString string = 'SERVER=${database.outputs.sqlServerName}${environment().suffixes.sqlServerHostname};DATABASE=${database.outputs.sqlDatabaseName}'
