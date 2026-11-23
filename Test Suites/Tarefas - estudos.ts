<?xml version="1.0" encoding="UTF-8"?>
<TestSuiteEntity>
   <description>Caminho principal primeiro. O CSV repete o POST. Os casos negativos fecham a suíte.</description>
   <name>Tarefas - estudos</name>
   <tag></tag>
   <isRerun>false</isRerun>
   <mailRecipient></mailRecipient>
   <numberOfRerun>0</numberOfRerun>
   <pageLoadTimeout>30</pageLoadTimeout>
   <pageLoadTimeoutDefault>true</pageLoadTimeoutDefault>
   <rerunFailedTestCasesOnly>false</rerunFailedTestCasesOnly>
   <rerunImmediately>false</rerunImmediately>
   <testSuiteGuid>4a0e5c30-0b1a-4a1e-8c01-000000000030</testSuiteGuid>
   <testCaseLink>
      <guid>4a0e5c30-0b1a-4a1e-8c01-000000000031</guid>
      <isReuseDriver>false</isReuseDriver>
      <isRun>true</isRun>
      <testCaseId>Test Cases/01 Verificar saude da API</testCaseId>
   </testCaseLink>
   <testCaseLink>
      <guid>4a0e5c30-0b1a-4a1e-8c01-000000000032</guid>
      <isReuseDriver>false</isReuseDriver>
      <isRun>true</isRun>
      <testCaseId>Test Cases/02 Listar tarefas</testCaseId>
   </testCaseLink>
   <testCaseLink>
      <guid>4a0e5c30-0b1a-4a1e-8c01-000000000035</guid>
      <isReuseDriver>false</isReuseDriver>
      <isRun>true</isRun>
      <testCaseId>Test Cases/05 Criar tarefa</testCaseId>
   </testCaseLink>
   <testCaseLink>
      <guid>4a0e5c30-0b1a-4a1e-8c01-000000000036</guid>
      <isReuseDriver>false</isReuseDriver>
      <isRun>true</isRun>
      <testCaseId>Test Cases/06 Fluxo completo de uma tarefa</testCaseId>
   </testCaseLink>
   <testCaseLink>
      <guid>4a0e5c30-0b1a-4a1e-8c01-000000000037</guid>
      <isReuseDriver>false</isReuseDriver>
      <isRun>true</isRun>
      <testCaseId>Test Cases/07 Criar tarefas a partir do CSV</testCaseId>
      <testDataLink>
         <combinationType>ONE</combinationType>
         <id>7a0e5c30-0b1a-4a1e-8c01-000000000081</id>
         <iterationEntity>
            <iterationType>ALL</iterationType>
            <value></value>
         </iterationEntity>
         <testDataId>Data Files/criar-tarefa</testDataId>
      </testDataLink>
      <variableLink>
         <testDataLinkId>7a0e5c30-0b1a-4a1e-8c01-000000000081</testDataLinkId>
         <type>DATA_COLUMN</type>
         <value>titulo</value>
         <variableId>6a0e5c30-0b1a-4a1e-8c01-000000000071</variableId>
      </variableLink>
      <variableLink>
         <testDataLinkId>7a0e5c30-0b1a-4a1e-8c01-000000000081</testDataLinkId>
         <type>DATA_COLUMN</type>
         <value>feita</value>
         <variableId>6a0e5c30-0b1a-4a1e-8c01-000000000072</variableId>
      </variableLink>
      <variableLink>
         <testDataLinkId>7a0e5c30-0b1a-4a1e-8c01-000000000081</testDataLinkId>
         <type>DATA_COLUMN</type>
         <value>statusEsperado</value>
         <variableId>6a0e5c30-0b1a-4a1e-8c01-000000000073</variableId>
      </variableLink>
   </testCaseLink>
   <testCaseLink>
      <guid>4a0e5c30-0b1a-4a1e-8c01-000000000033</guid>
      <isReuseDriver>false</isReuseDriver>
      <isRun>true</isRun>
      <testCaseId>Test Cases/03 Buscar tarefa inexistente</testCaseId>
   </testCaseLink>
   <testCaseLink>
      <guid>4a0e5c30-0b1a-4a1e-8c01-000000000034</guid>
      <isReuseDriver>false</isReuseDriver>
      <isRun>true</isRun>
      <testCaseId>Test Cases/04 Recusar tarefa sem titulo</testCaseId>
   </testCaseLink>
</TestSuiteEntity>
