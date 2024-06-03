<template>
	<div>
		<div class="fixed flex w-full justify-center bottom-0 left-0 mb-2 z-10">
			<LogsToolbar />
		</div>
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
