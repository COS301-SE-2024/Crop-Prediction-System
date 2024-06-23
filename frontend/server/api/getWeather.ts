export default defineEventHandler(async (event) => {
	const proxyUrl = useRuntimeConfig().public.openweatherApiUrl
	const apiKey = useRuntimeConfig().public.openweatherApiKey
	const lat = getQuery(event).lat
	const lon = getQuery(event).lon

	const apiUrl = `${proxyUrl}/forecast?lat=${lat}&lon=${lon}&appid=${apiKey}`

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
