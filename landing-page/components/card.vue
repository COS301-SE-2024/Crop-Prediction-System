<template>
	<div class="w-full border border-surface-border dark:border-surface-600 p-6 rounded-lg">
		<div class="w-full flex flex-col gap-2 justify-between items-center">
			<h2 class="font-semibold text-lg self-start">{{ title }}</h2>
			<h2 class="font-semibold text-lg self-start">{{ data }}</h2>
		</div>
	</div>
</template>

<script setup>
import Chart from 'primevue/chart'
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
