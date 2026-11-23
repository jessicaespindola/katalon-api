import static com.kms.katalon.core.testobject.ObjectRepository.findTestObject
import com.kms.katalon.core.webservice.keyword.WSBuiltInKeywords as WS
import groovy.json.JsonSlurper

'Cria uma tarefa. Os valores do mapa substituem as variáveis do pedido.'
def response = WS.sendRequest(findTestObject('Object Repository/Tarefas/POST tarefa', [
    'titulo': 'Criada pelo teste 05',
    'feita': false
]))

'201 Created: o recurso passou a existir'
WS.verifyResponseStatusCode(response, 201)
WS.verifyElementPropertyValue(response, 'titulo', 'Criada pelo teste 05')
WS.verifyElementPropertyValue(response, 'feita', false)

'O id vem da API. O teste não inventa esse número.'
def corpo = new JsonSlurper().parseText(response.getResponseText())
assert corpo.id instanceof Number
assert corpo.id > 0
