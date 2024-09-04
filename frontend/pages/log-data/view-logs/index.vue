<template>
	<div class="px-4 sm:px-6 md:px-8 lg:px-0 py-4 sm:py-6 md:py-8 lg:py-0">
		<div class="fixed flex w-full justify-center bottom-0 left-0 mb-2 z-10"></div>
		<div class="rounded-lg">
			<LogsView />
		</div>
	</div>
</template>

<script setup lang="ts">
import LogsView from '~/components/LogsView.vue'

definePageMeta({
	layout: 'default',
	middleware: 'auth',
})
</script>
