<template>
	<div class="bg-surface-300/60 dark:bg-surface-900">
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
</script>

<style scoped>
div {
	font-family: 'Inter', sans-serif;
}
</style>
