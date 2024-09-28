<script setup lang="ts">
import Navbar from '~/components/navbar.vue'
import Footer from '~/components/footer.vue'
import Divider from 'primevue/divider'
</script>

<template>
	<div class="h-screen select-none">
		<Navbar />
		<slot />
		<Footer />
	</div>
</template>

<style scoped>
div {
	font-family: 'Open Sans', sans-serif;
}
</style>
