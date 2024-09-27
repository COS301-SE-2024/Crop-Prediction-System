export default defineEventHandler(async (event) => {
	const { team_id } = getQuery(event)

	// Ensure both team_id and user_id are provided
	if (!team_id) {
		return {
			statusCode: 400,
			message: 'Team ID required',
		}
	}
	const apiBaseUrl = useRuntimeConfig().public.apiBaseUrl
	const callUrl = `${apiBaseUrl}/getTeamYield?team_id=${team_id}`

	try {
		const response = await fetch(callUrl)
		if (!response.ok) throw new Error()
		return response
	} catch (error) {
		// Handle any errors that occur during the API call
		return {
			statusCode: 500,
			message: 'Failed to fetch team messages',
			error: error.message,
		}
	}
})
