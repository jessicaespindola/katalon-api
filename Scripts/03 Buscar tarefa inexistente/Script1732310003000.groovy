import static com.kms.katalon.core.testobject.ObjectRepository.findTestObject
import com.kms.katalon.core.webservice.keyword.WSBuiltInKeywords as WS
import estudo.Padrao

'Pede um id que a API não conhece'
def response = WS.sendRequest(findTestObject('Object Repository/Tarefas/GET tarefa por id', [
	'id': 99999
]))

'404 esperado, com o contrato de erro'
Padrao.conferir(response, 404, 'Erro.json')
WS.verifyElementPropertyValue(response, 'erro', 'Tarefa nao encontrada')
