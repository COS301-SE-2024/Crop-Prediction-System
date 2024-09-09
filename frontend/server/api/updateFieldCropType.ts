export default defineEventHandler(async (event) => {
	const body = await readBody(event)
	const { field_id, crop_type } = body

	// Validate that the required parameters are present
	if (!field_id || !crop_type) {
		return {
			statusCode: 400,
			message: 'Both field_id and crop_type are required',
		}
	}

	const apiBaseUrl = useRuntimeConfig().public.apiBaseUrl

	try {
		// Call the external API to update the crop type
		await $fetch(`${apiBaseUrl}/updateField`, {
			method: 'PUT',
			body: { field_id, crop_type },
		})

		// Return success response
		return {
			statusCode: 200,
			message: 'Crop type updated successfully',
		}
	} catch (error) {
		// Return error response in case of failure
		return {
			statusCode: 500,
			message: 'Failed to update the crop type',
		}
	}
})
