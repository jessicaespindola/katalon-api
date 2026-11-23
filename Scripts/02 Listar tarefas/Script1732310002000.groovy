import static com.kms.katalon.core.testobject.ObjectRepository.findTestObject
import com.kms.katalon.core.util.KeywordUtil
import com.kms.katalon.core.webservice.keyword.WSBuiltInKeywords as WS
import estudo.Padrao
import groovy.json.JsonSlurper

'Envia GET /tarefas'
def response = WS.sendRequest(findTestObject('Object Repository/Tarefas/GET tarefas'))

'Status, Content-Type, schema da lista e tempo de resposta'
Padrao.conferir(response, 200, 'ListaTarefas.json')

'A primeira tarefa é a de exemplo, carregada quando o servidor sobe'
WS.verifyElementPropertyValue(response, '[0].id', 1)
WS.verifyElementPropertyValue(response, '[0].titulo', 'Ler o README')
WS.verifyElementPropertyValue(response, '[0].feita', false)

def tarefas = new JsonSlurper().parseText(response.getResponseText())
if (tarefas.size() == 0) {
	KeywordUtil.markFailed('LOGIC ERROR: a lista de tarefas veio vazia')
}
