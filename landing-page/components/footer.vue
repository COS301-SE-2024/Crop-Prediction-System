<template>
	<div
		class="bg-surface-0 dark:bg-surface-900 text-surface-700 dark:text-surface-0 shadow-md border-t-2 border-surface-300 dark:border-surface-600"
	>
		<footer>
			<div class="flex flex-col items-center justify-center px-4 py-6">
				<p>&copy; 2024, TerraByte is an EPI-USE Project made by GeekGurusUnion</p>
				<p>Contact us: <span class="underline">terrabyte.app@gmail.com</span></p>
			</div>
		</footer>
	</div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import Divider from 'primevue/divider'

const smoothScroll = (elementId: string) => {
	const element = document.querySelector(elementId)
	element?.scrollIntoView({ behavior: 'smooth' })
}

type Theme = 'light' | 'dark'
const setColorTheme = (newTheme: Theme) => {
	useColorMode().preference = newTheme
}
</script>
