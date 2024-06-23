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
	<div>Waiting for login...</div>
</template>
