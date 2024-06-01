<template>
	<div class="dark:bg-surface-800">
		<div>
			<header class="sticky">
				<Navbar />
			</header>
		</div>

		<div class="p-5 h-full">
			<slot />
		</div>
	</div>
</template>

<script setup lang="ts">
import Navbar from '~/components/Navbar.vue'
</script>
