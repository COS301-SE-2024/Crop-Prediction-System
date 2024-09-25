export default defineEventHandler(async (event) => {
	const body = await readBody(event)

	const { user_id, role } = body

	// Ensure both user_id and role are provided
	if (!user_id || !role) {
		return {
			statusCode: 400,
			message: 'Both user_id and role are required',
		}
	}

	const apiBaseUrl = useRuntimeConfig().public.apiBaseUrl

	try {
		// Make a POST request to the external API
		const response = await $fetch(`${apiBaseUrl}/updateRoles`, {
			method: 'POST',
			body: { user_id, role },
		})

		// Return the response from the API call
		return {
			statusCode: 200,
			message: 'Successfully updated user role',
			data: response,
		}
	} catch (error: any) {
		return {
			statusCode: error.response?.status || 500,
			message: error.message,
		}
	}
})
