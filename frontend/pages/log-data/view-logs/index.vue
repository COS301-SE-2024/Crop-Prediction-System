<template>
	<div>
		<div class="rounded-lg">
			<LogsView />
		</div>
	</div>
</template>

<script setup lang="ts">
import LogsToolbar from '~/components/LogsToolbar.vue'
import LogsView from '~/components/LogsView.vue'

definePageMeta({
	layout: 'default',
	middleware: 'auth',
})
</script>
