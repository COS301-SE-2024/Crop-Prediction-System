export default defineEventHandler(async (event) => {
	const config = useRuntimeConfig()
	const user_id = getQuery(event).user_id

	const apiUrl = `${config.public.apiBaseUrl}/removeFromTeam?user_id=${user_id}`

	// Make a PUT request to the external API
	try {
		const response = await $fetch(apiUrl, {
			method: 'PUT',
		})
		// Return the response from the API call
		return {
			statusCode: 200,
			message: 'Successfully removed user from team',
			data: response,
		}
	} catch (error) {
		return {
			statusCode: 500,
			message: 'Error removing user from team',
		}
	}
})
