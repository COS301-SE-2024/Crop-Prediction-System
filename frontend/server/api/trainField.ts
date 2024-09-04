export default defineEventHandler(async (event) => {
	const proxyUrl = useRuntimeConfig().public.apiBaseUrl
	const field_id = getQuery(event).field_id

	const callUrl = `${proxyUrl}/train?field_id=${field_id}`

	try {
		const response = await fetch(callUrl)
		if (!response.ok) {
			throw new Error(`Error: ${response.statusText}`)
		}
		const data = await response.json()
		return data
	} catch (error: any) {
		return {
			statusCode: error.response?.status || 500,
			message: error.message,
		}
	}
})
