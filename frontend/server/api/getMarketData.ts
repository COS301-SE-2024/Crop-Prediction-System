export default defineEventHandler(async (event) => {
	const { crop } = getQuery(event)

	// Ensure both team_id and user_id are provided
	if (!crop) {
		return {
			statusCode: 400,
			message: 'Crop is required',
		}
	}
	const apiBaseUrl = useRuntimeConfig().public.apiBaseUrl
	const callUrl = `${apiBaseUrl}/market?crop=${crop}`
	console.log('Call url is ', callUrl)

	try {
		const response = await fetch(callUrl)
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
