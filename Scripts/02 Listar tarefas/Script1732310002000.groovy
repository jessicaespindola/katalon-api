import static com.kms.katalon.core.testobject.ObjectRepository.findTestObject
import com.kms.katalon.core.webservice.keyword.WSBuiltInKeywords as WS

'Envia GET /tarefas'
def response = WS.sendRequest(findTestObject('Object Repository/Tarefas/GET tarefas'))

'A lista responde 200'
WS.verifyResponseStatusCode(response, 200)

'A primeira tarefa é a de exemplo, carregada quando o servidor sobe'
WS.verifyElementPropertyValue(response, '[0].id', 1)
WS.verifyElementPropertyValue(response, '[0].titulo', 'Ler o README')
WS.verifyElementPropertyValue(response, '[0].feita', false)
