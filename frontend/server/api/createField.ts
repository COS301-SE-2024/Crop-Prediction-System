export default defineEventHandler(async (event) => {
	const config = useRuntimeConfig()
	const body = await readBody(event)

	try {
		// Post request to {URL}/createField
		const response = await $fetch(`${config.public.apiBaseUrl}/createField`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(body),
		})
		return response
	} catch (e) {
		console.log(e)
		return {
			statusCode: 500,
			body: { e: 'Failed to create field' },
		}
	}
})
