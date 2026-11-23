import static com.kms.katalon.core.testobject.ObjectRepository.findTestObject
import com.kms.katalon.core.webservice.keyword.WSBuiltInKeywords as WS

'O mesmo pedido de criação, agora com título vazio'
def response = WS.sendRequest(findTestObject('Object Repository/Tarefas/POST tarefa', [
    'titulo': '',
    'feita': false
]))

'A API recusa o dado em vez de gravar uma tarefa sem nome'
WS.verifyResponseStatusCode(response, 400)
WS.verifyElementPropertyValue(response, 'erro', 'Informe o titulo')
