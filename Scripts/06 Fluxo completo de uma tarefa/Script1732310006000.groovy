import static com.kms.katalon.core.testobject.ObjectRepository.findTestObject
import com.kms.katalon.core.webservice.keyword.WSBuiltInKeywords as WS
import groovy.json.JsonSlurper

'1. Cria a tarefa que este fluxo vai usar'
def criada = WS.sendRequest(findTestObject('Object Repository/Tarefas/POST tarefa', [
    'titulo': 'Estudar o fluxo do Katalon',
    'feita': false
]))
WS.verifyResponseStatusCode(criada, 201)

def id = new JsonSlurper().parseText(criada.getResponseText()).id

'2. Busca pelo id devolvido no passo anterior'
def buscada = WS.sendRequest(findTestObject('Object Repository/Tarefas/GET tarefa por id', [
    'id': id
]))
WS.verifyResponseStatusCode(buscada, 200)
WS.verifyElementPropertyValue(buscada, 'titulo', 'Estudar o fluxo do Katalon')
WS.verifyElementPropertyValue(buscada, 'feita', false)

'3. Marca a tarefa como feita'
def atualizada = WS.sendRequest(findTestObject('Object Repository/Tarefas/PUT tarefa', [
    'id': id,
    'titulo': 'Estudar o fluxo do Katalon',
    'feita': true
]))
WS.verifyResponseStatusCode(atualizada, 200)
WS.verifyElementPropertyValue(atualizada, 'feita', true)

'4. Remove a tarefa. 204 não traz corpo.'
def apagada = WS.sendRequest(findTestObject('Object Repository/Tarefas/DELETE tarefa', [
    'id': id
]))
WS.verifyResponseStatusCode(apagada, 204)

'5. A mesma URL agora responde 404'
def sumiu = WS.sendRequest(findTestObject('Object Repository/Tarefas/GET tarefa por id', [
    'id': id
]))
WS.verifyResponseStatusCode(sumiu, 404)
WS.verifyElementPropertyValue(sumiu, 'erro', 'Tarefa nao encontrada')
