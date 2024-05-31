<template>
	<div>
		<div>
			<header class="sticky">
				<Navbar />
			</header>
		</div>

		<div class="mt-5 min-h-screen w-[95%] m-auto">
			<slot />
		</div>
	</div>
</template>

<script setup lang="ts">
import Navbar from '~/components/Navbar.vue'
</script>
