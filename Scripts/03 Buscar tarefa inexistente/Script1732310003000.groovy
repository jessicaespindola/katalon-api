import static com.kms.katalon.core.testobject.ObjectRepository.findTestObject
import com.kms.katalon.core.webservice.keyword.WSBuiltInKeywords as WS

'Pede um id que a API não conhece'
def response = WS.sendRequest(findTestObject('Object Repository/Tarefas/GET tarefa por id', [
    'id': 99999
]))

'Recurso ausente é 404, com uma mensagem no corpo'
WS.verifyResponseStatusCode(response, 404)
WS.verifyElementPropertyValue(response, 'erro', 'Tarefa nao encontrada')
