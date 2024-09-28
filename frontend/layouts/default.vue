<template>
	<div class="bg-surface-300/60 dark:bg-surface-900 select-none">
		<div class="w-full min-h-screen">
			<!-- <div class="h-auto"> -->
			<header class="sticky">
				<Navbar />
			</header>
			<!-- </div> -->
			<div class="p-4">
				<slot />
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import Navbar from '~/components/Navbar.vue'

useHead({
	title: 'TerraByte',
	meta: [
		{
			name: 'description',
			content:
				'AI-driven Crop Prediction System that applies Machine Learning and AI to analyze weather, soil, and crop data to predict crop health and yield. This system provides farmers with precise predictions, empowering them to make data-driven decisions and enhance their farming practices. ',
		},
	],
})
</script>

<style scoped>
div {
	font-family: 'Open Sans', sans-serif;
}
</style>
