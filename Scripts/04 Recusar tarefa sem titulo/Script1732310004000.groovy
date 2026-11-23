import static com.kms.katalon.core.testobject.ObjectRepository.findTestObject
import com.kms.katalon.core.webservice.keyword.WSBuiltInKeywords as WS
import estudo.Padrao

'O mesmo pedido de criação, agora com título vazio'
def response = WS.sendRequest(findTestObject('Object Repository/Tarefas/POST tarefa', [
	'titulo': '',
	'feita': false
]))

'400 esperado, com o contrato de erro'
Padrao.conferir(response, 400, 'Erro.json')
WS.verifyElementPropertyValue(response, 'erro', 'Informe o titulo')
