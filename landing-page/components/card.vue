<template>
	<div class="w-full border border-surface-border dark:border-surface-600 py-2 px-6 rounded-lg text-xl">
		<div class="w-full mt-4">
			<slot name="text"></slot>
		</div>
	</div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

onMounted(() => {
	chartOptions.value = setChartOptions()
})

const chartOptions = ref()

const props = defineProps({
	title: {
		type: String,
		required: true,
	},
	chartData: {
		type: Object,
		required: true,
	},
	chartType: {
		type: String,
		default: 'line',
	},
})

const setChartOptions = () => {
	return {
		maintainAspectRatio: false,
		responsive: true,
		plugins: {
			legend: {
				display: true,
			},
		},
		scales: {
			x: {
				ticks: {
					autoSkip: false,
				},
				grid: {
					color: 'rgba(192, 192, 192, 0.3)',
					display: true,
				},
			},
			y: {
				beginAtZero: false,
				ticks: {
					stepSize: 2,
				},
				grid: {
					color: 'rgba(192, 192, 192, 0.3)',
					display: true,
				},
			},
		},
	}
}
</script>
