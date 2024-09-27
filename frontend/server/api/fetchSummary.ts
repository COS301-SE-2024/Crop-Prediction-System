export default defineEventHandler(async () => {
	const proxyUrl = useRuntimeConfig().public.apiBaseUrl

	const apiUrl = `${proxyUrl}/fetchSummary`

	try {
		const response = await fetch(apiUrl)
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
