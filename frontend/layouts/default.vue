<template>
	<div class="bg-primary-inverse dark:bg-surface-800">
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
