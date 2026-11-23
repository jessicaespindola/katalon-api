import static com.kms.katalon.core.testobject.ObjectRepository.findTestObject
import com.kms.katalon.core.webservice.keyword.WSBuiltInKeywords as WS
import estudo.Padrao
import groovy.json.JsonSlurper

'1. Cria a tarefa que este fluxo vai usar'
def criada = WS.sendRequest(findTestObject('Object Repository/Tarefas/POST tarefa', [
	'titulo': 'Estudar o fluxo do Katalon',
	'feita': false
]))
Padrao.conferir(criada, 201, 'Tarefa.json')

def id = new JsonSlurper().parseText(criada.getResponseText()).id

'2. Busca pelo id devolvido no passo anterior'
def buscada = WS.sendRequest(findTestObject('Object Repository/Tarefas/GET tarefa por id', [
	'id': id
]))
Padrao.conferir(buscada, 200, 'Tarefa.json')
WS.verifyElementPropertyValue(buscada, 'titulo', 'Estudar o fluxo do Katalon')
WS.verifyElementPropertyValue(buscada, 'feita', false)

'3. Marca a tarefa como feita'
def atualizada = WS.sendRequest(findTestObject('Object Repository/Tarefas/PUT tarefa', [
	'id': id,
	'titulo': 'Estudar o fluxo do Katalon',
	'feita': true
]))
Padrao.conferir(atualizada, 200, 'Tarefa.json')
WS.verifyElementPropertyValue(atualizada, 'feita', true)

'4. Remove a tarefa. 204 não traz corpo nem Content-Type.'
def apagada = WS.sendRequest(findTestObject('Object Repository/Tarefas/DELETE tarefa', [
	'id': id
]))
Padrao.conferir(apagada, 204, null)

'5. A mesma URL agora responde 404'
def sumiu = WS.sendRequest(findTestObject('Object Repository/Tarefas/GET tarefa por id', [
	'id': id
]))
Padrao.conferir(sumiu, 404, 'Erro.json')
WS.verifyElementPropertyValue(sumiu, 'erro', 'Tarefa nao encontrada')
