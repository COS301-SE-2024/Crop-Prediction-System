export default defineEventHandler(async (event) => {
	const { user_id } = getQuery(event)

	// Ensure both team_id and user_id are provided
	if (!user_id) {
		return {
			statusCode: 400,
			message: 'User ID required',
		}
	}
	const apiBaseUrl = useRuntimeConfig().public.apiBaseUrl
	const callUrl = `${apiBaseUrl}/getUser?user_id=${user_id}`

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
