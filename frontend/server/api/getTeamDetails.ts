export default defineEventHandler(async (event) => {
	const proxyUrl = useRuntimeConfig().public.apiBaseUrl
	const team_id = getQuery(event).team_id

	const apiUrl = `${proxyUrl}/getTeamDetails?team_id=${team_id}`

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
