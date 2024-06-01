<template>
	<div class="flex flex-col items-center justify-center min-h-screen">
		<h1 class="text-4xl font-light text-black">This is working, Tailwind CSS is working!</h1>
	</div>
</template>

<script setup lang="ts">
definePageMeta({
	middleware: 'auth',
})
</script>
