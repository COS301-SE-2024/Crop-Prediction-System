<script lang="ts" setup>
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

<template>
	<div class="bg-surface-300/60 dark:bg-surface-900">
		<slot />
	</div>
</template>

<style scoped>
div {
	font-family: 'Open Sans', sans-serif;
}
</style>
