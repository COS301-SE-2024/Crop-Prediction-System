<template>
	<div>
		<h1>Help</h1>
		<p>{{ data }}</p>
	</div>
</template>

<script setup>
const { data } = await $fetch('/api/fieldInfo', {
	params: { fieldId: 9 },
})

console.log('data', data)
</script>
