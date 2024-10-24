export default defineEventHandler(async (event) => {
	try {
		// Read the request body
		const body = await readBody(event)

		// Check if necessary data is present in the request body
		const { field_name, crop_type, team_id, field_area } = body

		if (!field_name || !crop_type || !team_id || !field_area) {
			return {
				statusCode: 400,
				message: 'Missing required fields: field_name, crop_type, team_id, or field_area',
			}
		}

		// Prepare the API call to the external server
		const apiBaseUrl = useRuntimeConfig().public.apiBaseUrl
		const saveFieldUrl = `${apiBaseUrl}/createField`

		const sendBody = {
			field_name,
			crop_type,
			field_area, // Pass the polygon coordinates
			team_id,
		}

		// console.log('SendBody', sendBody)
		// console.log('Field Stringify', JSON.stringify(field_area))
		// Forward the data to the external API
		const response = await $fetch(saveFieldUrl, {
			method: 'POST',
			body: {
				field_name,
				crop_type,
				field_area, // Pass the polygon coordinates
				team_id,
			},
		})

		// Check if the external API responded with success
		if (response.statusCode === 200 || response.status === 'success') {
			return {
				statusCode: 200,
				message: 'Field saved successfully',
			}
		} else {
			return {
				statusCode: response.statusCode || 500,
				message: response.message || 'Failed to save field',
			}
		}
	} catch (error) {
		// Handle any errors
		console.error('Error saving field:', error)
		return {
			statusCode: 500,
			message: 'An error occurred while saving the field',
		}
	}
})
