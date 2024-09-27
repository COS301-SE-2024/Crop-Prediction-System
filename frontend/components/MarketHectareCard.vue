<template>
	<div class="bg-surface-100 dark:bg-surface-800 p-5 rounded-md shadow-md">
		<div class="flex justify-between mb-4">
			<div>
				<span class="block text-surface-600 dark:text-surface-0/60 font-medium mb-4">{{ title }}</span>
				<div v-if="hectare !== 0" class="text-surface-900 dark:text-surface-0 font-medium text-xl">
					{{ hectare }} <span class="text-lg">ha</span>
				</div>
				<div v-else class="text-surface-900 dark:text-surface-0 font-medium text-sm">N/A</div>
			</div>
			<div
				class="flex items-center justify-center bg-blue-100 dark:bg-blue-400/10 rounded-md"
				style="width: 2.5rem; height: 2.5rem"
			>
				<i class="pi pi-map text-blue-500 !text-xl"></i>
			</div>
		</div>
		<span class="text-surface-600 dark:text-surface-0/60">{{ footer }}</span>
	</div>
</template>

<script setup>
const props = defineProps({
	title: {
		type: String,
		required: true,
	},
	hectare: {
		type: Number,
		required: false,
		default: 0,
	},
	footer: {
		type: String,
		required: true,
	},
})
</script>
