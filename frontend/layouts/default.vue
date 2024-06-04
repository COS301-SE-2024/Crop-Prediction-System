<template>
	<div class="bg-primary-inverse dark:bg-surface-800">
		<div>
			<header class="sticky">
				<Navbar />
			</header>
		</div>

		<div class="sm:p-5 h-full w-screen">
			<slot />
		</div>
	</div>
</template>

<script setup lang="ts">
import Navbar from '~/components/Navbar.vue'
</script>
