export default defineEventHandler(async (event) => {
	const body = await readBody(event)
	console.log('Body is', body)

	const { id, full_name } = body

	// Ensure both user_id and role are provided
	if (!id || !full_name) {
		return {
			statusCode: 400,
			message: 'Both user_id and full name are required',
		}
	}

	const apiBaseUrl = useRuntimeConfig().public.apiBaseUrl

	try {
		// Make a POST request to the external API
		const response = await $fetch(`${apiBaseUrl}/updateUser`, {
			method: 'PUT',
			body: { id, full_name },
		})

		console.log(response)
		// Return the response from the API call
		return {
			statusCode: 200,
			message: 'Successfully updated user profile',
			data: response,
		}
	} catch (error: any) {
		return {
			statusCode: error.response?.status || 500,
			message: error.message,
		}
	}
})
