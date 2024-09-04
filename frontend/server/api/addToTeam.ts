const config = useRuntimeConfig()

export default defineEventHandler(async (event) => {
	const body = await readBody(event)

	const { team_id, user_id } = body

	// Ensure both team_id and user_id are provided
	if (!team_id || !user_id) {
		return {
			statusCode: 400,
			message: 'Both team_id and user_id are required',
		}
	}
	const apiBaseUrl = config.public.apiBaseUrl

	try {
		// Make a POST request to the external API
		const response = await $fetch(`${apiBaseUrl}/addToTeam`, {
			method: 'POST',
			body: { team_id, user_id },
		})

		// Return the response from the API call
		return {
			statusCode: 200,
			message: 'Successfully added user to the team',
			data: response,
		}
	} catch (error) {
		// Handle any errors that occur during the API call
		return {
			statusCode: 500,
			message: 'Failed to add user to the team',
			error: error.message,
		}
	}
})
