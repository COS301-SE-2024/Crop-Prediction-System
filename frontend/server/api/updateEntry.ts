export default defineEventHandler(async (event) => {
	const config = useRuntimeConfig()
	const body = await readBody(event)

	try {
		// Post request to {URL}/updateEntry
		const response = await $fetch(`${config.public.apiBaseUrl}/updateEntry`, {
			method: 'PUT',
			body: JSON.stringify(body),
		})
		return response
	} catch (e) {
		console.log(e)
		return {
			statusCode: 500,
			body: { e: 'Failed to create entry' },
		}
	}
})
