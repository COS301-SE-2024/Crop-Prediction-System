export default defineEventHandler(async (event) => {
	const proxyUrl = useRuntimeConfig().public.apiBaseUrl
	const body = await readBody(event)

	const callUrl = `${proxyUrl}/train`

	try {
		const response = await $fetch(callUrl, {
			method: 'POST',
			body: JSON.stringify(body),
		})
		if (!response.ok) {
			throw new Error(`Error: ${response.statusText}`)
		}
		const data = await response.json()
		return data.status
	} catch (error: any) {
		return {
			statusCode: error.response?.status || 500,
			message: error.message,
		}
	}
})
