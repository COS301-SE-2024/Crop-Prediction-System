export default defineNuxtRouteMiddleware((to, _from) => {
	const user = useSupabaseUser()

	if (!user.value) {
		// Capture the current route path (to.fullPath)
		const redirectPath = to.fullPath

		// Redirect to login with redirectPath as a query parameter
		return navigateTo(`/login?redirectTo=${redirectPath}`)
	}
})
