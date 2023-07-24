
@allowed([
  'Device'
  'ForeignGroup'
  'Group'
  'ServicePrincipal'
  'User'
])

param principalType string = 'User'
param roleDefinitionId string
/* 7f189770-2ab1-4898-88f4-315bef704ab8 Hauk 
  28ffb7b0-7bee-4e01-8f46-fd5f9568d9c7 Alex
  3a682528-6f8c-48fd-aecf-994f9f3e95c0 Herman 
  68d01abb-fe3e-44cc-8709-3275d4c58a03 Njål

*/  

var principalIdArray = ['7f189770-2ab1-4898-88f4-315bef704ab8','28ffb7b0-7bee-4e01-8f46-fd5f9568d9c7','3a682528-6f8c-48fd-aecf-994f9f3e95c0','68d01abb-fe3e-44cc-8709-3275d4c58a03']

resource role 'Microsoft.Authorization/roleAssignments@2022-04-01' = [for i in range(0,length(principalIdArray)):{
  name: guid(subscription().id, resourceGroup().id, principalIdArray[i], roleDefinitionId)
  properties: {
    principalId: principalIdArray[i]
    principalType: principalType
    roleDefinitionId: resourceId('Microsoft.Authorization/roleDefinitions', roleDefinitionId)
  }
}]
