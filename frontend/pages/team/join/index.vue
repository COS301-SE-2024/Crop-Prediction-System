<template>
	<div class="flex flex-col justify-center items-center">
		<p>This this is the Join Team Page</p>
	</div>
</template>

<script setup lang="ts">
definePageMeta({
	middleware: 'auth',
})
</script>
