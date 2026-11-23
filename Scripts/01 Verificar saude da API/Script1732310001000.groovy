import static com.kms.katalon.core.testobject.ObjectRepository.findTestObject
import com.kms.katalon.core.webservice.keyword.WSBuiltInKeywords as WS
import estudo.Padrao

'Envia GET /health'
def response = WS.sendRequest(findTestObject('Object Repository/Tarefas/GET health'))

'Status, Content-Type, schema e tempo de resposta'
Padrao.conferir(response, 200, 'HealthResponse.json')

'Valores de negócio do corpo'
WS.verifyElementPropertyValue(response, 'status', 'ok')
WS.verifyElementPropertyValue(response, 'servico', 'tarefas')
