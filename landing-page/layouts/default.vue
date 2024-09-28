<script setup lang="ts">
import Navbar from '~/components/navbar.vue'
import Footer from '~/components/footer.vue'
</script>

<template>
	<div class="h-screen select-none">
		<Navbar />
		<slot />
		<Footer />
	</div>
</template>
