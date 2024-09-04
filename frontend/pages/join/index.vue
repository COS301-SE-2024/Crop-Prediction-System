<template>
	<h1>Code: {{ teamid.team_id }}</h1>
</template>

<script setup lang="ts">
const teamid = useRoute().query

definePageMeta({
	layout: 'auth',
})
</script>
