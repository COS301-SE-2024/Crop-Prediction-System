export default defineEventHandler(async (event) => {
	const config = useRuntimeConfig()
	const { fieldid } = getQuery(event)

	try {
		const response = await $fetch(`${config.public.apiBaseUrl}/getFieldInfo`, {
			params: { fieldid },
		})
		return response
	} catch (error) {
		console.error('Error fetching field info:', error)
	}
})
