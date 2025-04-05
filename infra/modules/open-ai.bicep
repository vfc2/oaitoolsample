@description('The project name to use when naming resources.')
param projectName string

var openAiName = 'oai-${projectName}-001'
var openAiCustomDomain = replace(openAiName, '-', '')

/* Open AI service */
resource openAiService 'Microsoft.CognitiveServices/accounts@2024-10-01' = {
    name: openAiName
    location: resourceGroup().location
    kind: 'OpenAI'
    identity: {
        type: 'SystemAssigned'
    }
    sku: {
        name: 'S0'
    }
    properties: {
        customSubDomainName: openAiCustomDomain
    }
}

/* Model deployments */
resource modelGpt4oMini 'Microsoft.CognitiveServices/accounts/deployments@2024-10-01' = {
    name: 'gpt-4o-mini'
    parent: openAiService
    sku: {
        name: 'GlobalStandard'
        capacity: 500
    }
    properties: {
        model: {
            format: 'OpenAI'
            name: 'gpt-4o-mini'
            version: '2024-07-18'
        }
    }
}

output openAiServiceName string = openAiService.name
output openAiEndpoint string = openAiService.properties.endpoint

