<template>
	<div class="bg-surface-0 dark:bg-surface-900 text-surface-700 dark:text-surface-0 shadow-md">
		<footer>
			<div class="flex flex-col items-center justify-center px-4 py-4">
				<p>&copy; 2024, Product of GeekGurusUnion</p>
				<a
					@click="smoothScroll('#nav')"
					class="flex flex-wrap items-center justify-center md:justify-start md:mb-0 mb-4 cursor-pointer"
				>
					<h4 class="font-medium text-3xl text-surface-900 dark:text-surface-0">TerraByte</h4>
				</a>
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
