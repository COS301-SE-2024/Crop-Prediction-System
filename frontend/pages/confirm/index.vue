<script setup lang="ts">
const user = useSupabaseUser()

watch(
	user,
	() => {
		if (user.value) {
			// Redirect to protected page
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
		<h2 class="dark:text-white font-bold">Waiting for login...</h2>
		<ProgressSpinner />
	</div>
</template>
