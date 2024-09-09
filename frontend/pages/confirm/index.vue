<script setup lang="ts">
const user = useSupabaseUser()

watch(
	user,
	() => {
		if (user.value) {
			// Get the redirect path from query parameters
			const route = useRoute()
			const redirectTo = route.query.redirectTo as string | undefined

			// If a redirect path exists, navigate to it
			if (redirectTo) {
				return navigateTo(redirectTo)
			}

			// Fallback: Navigate to default route if no redirect path is provided
			return navigateTo('/')
		}
	},
	{ immediate: true },
)

definePageMeta({
	layout: 'auth',
})
</script>

<template>
	<div class="w-full h-screen gap-5 flex flex-col items-center justify-center">
		<ProgressSpinner />
		<h2 class="dark:text-white font-bold">Waiting for login...</h2>
	</div>
</template>
