import static com.kms.katalon.core.testobject.ObjectRepository.findTestObject
import com.kms.katalon.core.webservice.keyword.WSBuiltInKeywords as WS

'Envia GET /health'
def response = WS.sendRequest(findTestObject('Object Repository/Tarefas/GET health'))

'A API deve responder 200'
WS.verifyResponseStatusCode(response, 200)

'O corpo diz que o serviço está no ar'
WS.verifyElementPropertyValue(response, 'status', 'ok')
WS.verifyElementPropertyValue(response, 'servico', 'tarefas')
