export default defineEventHandler(async (event) => {
	const body = await readBody(event)

	const { field_id, field_name } = body

	if (!field_name || !field_id) {
		return {
			statusCode: 400,
			message: 'Both field_name and field_id are required',
		}
	}
	const apiBaseUrl = useRuntimeConfig().public.apiBaseUrl

	try {
		await $fetch(`${apiBaseUrl}/updateField`, {
			method: 'PUT',
			body: { field_id, field_name },
		})

		return {
			statusCode: 200,
			message: 'Field name updated',
		}
	} catch (error) {
		return {
			statusCode: 500,
			message: 'Failed to update field name',
		}
	}
})
