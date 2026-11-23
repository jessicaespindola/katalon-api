package estudo

import com.kms.katalon.core.configuration.RunConfiguration
import com.kms.katalon.core.util.KeywordUtil
import com.kms.katalon.core.webservice.keyword.WSBuiltInKeywords as WS

import internal.GlobalVariable as GlobalVariable

/**
 * Passos que a documentação de scripting do Katalon pede em todo pedido:
 * status, Content-Type, schema JSON e tempo de resposta.
 *
 * https://docs.katalon.com/katalon-studio/create-test-cases/api-testing-best-practices-scripting-standards
 */
class Padrao {

	static void conferir(response, int statusEsperado, String schemaArquivo = null) {
		WS.verifyResponseStatusCode(response, statusEsperado)

		if (statusEsperado != 204) {
			String contentType = contentTypeDe(response)
			if (!contentType.contains('application/json')) {
				KeywordUtil.markFailed('Invalid Content-Type. Expected JSON but found: ' + contentType)
			}
		}

		if (schemaArquivo) {
			String schemaPath = RunConfiguration.getProjectDir() + '/Schemas/' + schemaArquivo
			String schemaContent = new File(schemaPath).text
			boolean isMatch = WS.validateJsonAgainstSchema(response, schemaContent)
			if (!isMatch) {
				KeywordUtil.markFailed('Response did not match the Schema contract: ' + schemaArquivo)
			}
		}

		long maxResponseTime = GlobalVariable.maxResponseTime as long
		long actualTime = response.getElapsedTime()
		if (actualTime > maxResponseTime) {
			KeywordUtil.markWarning('PERFORMANCE WARNING: API took ' + actualTime + 'ms (Limit: ' + maxResponseTime + 'ms)')
		}
	}

	private static String contentTypeDe(response) {
		def headers = response.getHeaderFields()
		if (headers == null) {
			return ''
		}
		def bruto = headers['Content-Type']
		if (bruto == null) {
			bruto = headers['content-type']
		}
		return bruto == null ? '' : bruto.toString()
	}
}
