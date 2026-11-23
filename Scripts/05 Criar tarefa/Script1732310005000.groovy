import static com.kms.katalon.core.testobject.ObjectRepository.findTestObject
import com.kms.katalon.core.util.KeywordUtil
import com.kms.katalon.core.webservice.keyword.WSBuiltInKeywords as WS
import estudo.Padrao
import groovy.json.JsonSlurper

'Cria uma tarefa. Os valores do mapa substituem as variáveis do pedido.'
def response = WS.sendRequest(findTestObject('Object Repository/Tarefas/POST tarefa', [
	'titulo': 'Criada pelo teste 05',
	'feita': false
]))

'201, Content-Type, schema da tarefa e tempo de resposta'
Padrao.conferir(response, 201, 'Tarefa.json')
WS.verifyElementPropertyValue(response, 'titulo', 'Criada pelo teste 05')
WS.verifyElementPropertyValue(response, 'feita', false)

'Guarda cada campo da resposta e exige valor'
def jsonResponse = new JsonSlurper().parseText(response.getResponseText())
def dynamicVars = [:]
jsonResponse.each { key, value ->
	dynamicVars[key] = value
}
dynamicVars.each { key, value ->
	if (value == null) {
		KeywordUtil.markFailed("Field '${key}' is null")
	}
}
if (!(dynamicVars['id'] > 0)) {
	KeywordUtil.markFailed('FAILED: ID is invalid (Value: ' + dynamicVars['id'] + ')')
}
