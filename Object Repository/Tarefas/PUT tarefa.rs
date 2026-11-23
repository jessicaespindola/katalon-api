<?xml version="1.0" encoding="UTF-8"?>
<WebServiceRequestEntity>
   <description>Substitui título e status de uma tarefa existente.</description>
   <name>PUT tarefa</name>
   <tag></tag>
   <elementGuidId>1a0e5c30-0b1a-4a1e-8c01-000000000005</elementGuidId>
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
   <restRequestMethod>PUT</restRequestMethod>
   <restUrl>${GlobalVariable.baseUrl}/tarefas/${id}</restUrl>
   <serviceType>RESTful</serviceType>
   <soapBody></soapBody>
   <soapHeader></soapHeader>
   <soapRequestMethod></soapRequestMethod>
   <soapServiceFunction></soapServiceFunction>
   <variables>
      <defaultValue>1</defaultValue>
      <description></description>
      <id>2a0e5c30-0b1a-4a1e-8c01-000000000014</id>
      <masked>false</masked>
      <name>id</name>
   </variables>
   <variables>
      <defaultValue>'Estudar Katalon'</defaultValue>
      <description></description>
      <id>2a0e5c30-0b1a-4a1e-8c01-000000000015</id>
      <masked>false</masked>
      <name>titulo</name>
   </variables>
   <variables>
      <defaultValue>true</defaultValue>
      <description></description>
      <id>2a0e5c30-0b1a-4a1e-8c01-000000000016</id>
      <masked>false</masked>
      <name>feita</name>
   </variables>
   <verificationScript></verificationScript>
   <wsdlAddress></wsdlAddress>
</WebServiceRequestEntity>
