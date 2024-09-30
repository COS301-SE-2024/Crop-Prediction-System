<template>
	<div class="bg-surface-300/60 dark:bg-surface-900 select-none">
		<div class="w-full h-screen flex flex-col justify-between">
			<header class="sticky top-0">
				<Navbar />
			</header>
			<div ref="scrollableContainer" class="px-4 py-4 md:px-32 overflow-y-scroll">
				<slot />
			</div>
			<div class="h-[20%] p-4 md:px-32">
				<div class="w-full h-full">
					<MessageToolbar />
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import MessageToolbar from '~/components/MessageToolbar.vue'
import Navbar from '~/components/Navbar.vue'
import { ref } from 'vue'

const scrollableContainer = ref(null)

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
