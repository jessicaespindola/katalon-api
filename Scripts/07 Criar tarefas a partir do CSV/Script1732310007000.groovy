import static com.kms.katalon.core.testobject.ObjectRepository.findTestObject
import com.kms.katalon.core.util.KeywordUtil
import com.kms.katalon.core.webservice.keyword.WSBuiltInKeywords as WS
import estudo.Padrao
import groovy.json.JsonSlurper

String tituloInformado = titulo == null ? '' : titulo.toString()
boolean feitaInformada = feita.toString().equalsIgnoreCase('true')
int statusInformado = statusEsperado.toString().toInteger()

'Uma linha do CSV, o mesmo pedido POST'
def response = WS.sendRequest(findTestObject('Object Repository/Tarefas/POST tarefa', [
	'titulo': tituloInformado,
	'feita': feitaInformada
]))

String schema = statusInformado == 201 ? 'Tarefa.json' : 'Erro.json'
Padrao.conferir(response, statusInformado, schema)

if (statusInformado == 201) {
	WS.verifyElementPropertyValue(response, 'titulo', tituloInformado)
	WS.verifyElementPropertyValue(response, 'feita', feitaInformada)
	def corpo = new JsonSlurper().parseText(response.getResponseText())
	if (!(corpo.id > 0)) {
		KeywordUtil.markFailed('FAILED: ID is invalid (Value: ' + corpo.id + ')')
	}
} else {
	WS.verifyElementPropertyValue(response, 'erro', 'Informe o titulo')
}
