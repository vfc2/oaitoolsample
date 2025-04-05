@description('The Entra group for AI Developers')
param aiDevelopersGroupPrincipalId string

@description('The name of the Open AI service instance')
param openAiServiceName string

/* Resources */
resource openAiService 'Microsoft.CognitiveServices/accounts@2024-10-01' existing = {
    name: openAiServiceName
}

/* Role definitions */
@description('This is the built-in Cognitive Services OpenAI Contributor role')
resource roleCognitiveServicesOpenAiContributor 'Microsoft.Authorization/roleDefinitions@2022-04-01' existing = {
  scope: subscription()
  name: 'a001fd3d-188f-4b5d-821b-7da978bf7442'
}

/* Role assignments */
resource roleAssignmentAiDevelopersCognitiveServicesOpenAiContributor 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(subscription().id, aiDevelopersGroupPrincipalId, roleCognitiveServicesOpenAiContributor.id)
  scope: openAiService
  properties: {
      principalId: aiDevelopersGroupPrincipalId
      roleDefinitionId: roleCognitiveServicesOpenAiContributor.id
  }
}
