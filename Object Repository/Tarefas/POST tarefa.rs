<?xml version="1.0" encoding="UTF-8"?>
<WebServiceRequestEntity>
   <description>Cria uma tarefa. titulo e feita são variáveis do pedido e entram no corpo JSON.</description>
   <name>POST tarefa</name>
   <tag></tag>
   <elementGuidId>1a0e5c30-0b1a-4a1e-8c01-000000000004</elementGuidId>
   <selectorMethod>BASIC</selectorMethod>
   <useRalativeImagePath>false</useRalativeImagePath>
   <followRedirects>false</followRedirects>
   <httpBody></httpBody>
   <httpBodyContent>{
  &quot;text&quot;: &quot;{\n  \&quot;titulo\&quot;: \&quot;${titulo}\&quot;,\n  \&quot;feita\&quot;: ${feita}\n}&quot;,
  &quot;contentType&quot;: &quot;application/json&quot;,
  &quot;charset&quot;: &quot;UTF-8&quot;
}</httpBodyContent>
   <httpBodyType>text</httpBodyType>
   <httpHeaderProperties>
      <isSelected>true</isSelected>
      <matchCondition>equals</matchCondition>
      <name>Content-Type</name>
      <type>Main</type>
      <value>application/json</value>
   </httpHeaderProperties>
   <restRequestMethod>POST</restRequestMethod>
   <restUrl>${GlobalVariable.baseUrl}/tarefas</restUrl>
   <serviceType>RESTful</serviceType>
   <soapBody></soapBody>
   <soapHeader></soapHeader>
   <soapRequestMethod></soapRequestMethod>
   <soapServiceFunction></soapServiceFunction>
   <variables>
      <defaultValue>'Estudar Katalon'</defaultValue>
      <description>Texto da tarefa. É uma expressão Groovy, por isso o texto fica entre aspas simples.</description>
      <id>2a0e5c30-0b1a-4a1e-8c01-000000000011</id>
      <masked>false</masked>
      <name>titulo</name>
   </variables>
   <variables>
      <defaultValue>false</defaultValue>
      <description>true ou false, sem aspas.</description>
      <id>2a0e5c30-0b1a-4a1e-8c01-000000000012</id>
      <masked>false</masked>
      <name>feita</name>
   </variables>
   <verificationScript></verificationScript>
   <wsdlAddress></wsdlAddress>
</WebServiceRequestEntity>
