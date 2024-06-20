export default defineEventHandler(async (event) => {
  const proxyUrl = useRuntimeConfig().public.apiBaseUrl
  const { fieldid } = getQuery(event)

  const apiUrl = `${proxyUrl}/getFieldInfo?fieldid=${fieldid}`

  try {
    const response = await fetch(apiUrl)
    if (!response.ok) {
      throw new Error(`Error: ${response.statusText}`)
    }
    const data = await response.json()
    return data
  } catch (error: any) {
    return {
      statusCode: error.response?.status || 500,
      message: error.message
    }
  }
})
