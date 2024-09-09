export default defineEventHandler(async (event) => {
	const body = await readBody(event)
	const { field_id } = body

	if (!field_id) {
		return {
			statusCode: 400,
			message: 'Field ID is required',
		}
	}

	const apiBaseUrl = useRuntimeConfig().public.apiBaseUrl

	try {
		await $fetch(`${apiBaseUrl}/deleteField`, {
			method: 'POST',
			body: { field_id },
		})

		return {
			statusCode: 200,
			message: 'Field deleted successfully',
		}
	} catch (error) {
		return {
			statusCode: 500,
			message: 'Failed to delete the field',
		}
	}
})
