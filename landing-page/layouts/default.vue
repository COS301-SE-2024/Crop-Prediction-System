<script setup lang="ts">
import Navbar from '~/components/navbar.vue'
</script>

<template>
	<div class="h-screen">
		<Navbar />
		<slot />
	</div>
</template>
