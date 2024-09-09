export default defineEventHandler(async (event) => {
	const body = await readBody(event)
	const { field_id, field_area } = body

	// Validate that the required parameters are present
	if (!field_id || !field_area) {
		return {
			statusCode: 400,
			message: 'Both field_id and field_area are required',
		}
	}

	const apiBaseUrl = useRuntimeConfig().public.apiBaseUrl

	try {
		// Call the external API to update the field area
		await $fetch(`${apiBaseUrl}/updateField`, {
			method: 'PUT',
			body: { field_id, field_area },
		})

		// Return success response
		return {
			statusCode: 200,
			message: 'Field area updated successfully',
		}
	} catch (error) {
		// Return error response in case of failure
		return {
			statusCode: 500,
			message: 'Failed to update the field area',
		}
	}
})
