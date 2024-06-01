<template>
	<div class="h-screen">
		<div>
			<header class="sticky">
				<Navbar />
			</header>
		</div>

		<div class="m-5 h-full">
			<slot />
		</div>
	</div>
</template>

<script setup lang="ts">
import Navbar from '~/components/Navbar.vue'
</script>
