<template>
	<div class="w-full p-6 rounded-lg shadow-md bg-surface-100 dark:bg-surface-800">
		<div class="w-full flex flex-col gap-2 justify-between items-center">
			<div class="flex justify-between w-full md:items-center">
				<div>
					<h2 class="font-semibold text-lg self-start">{{ title }}</h2>
				</div>
				<div class="text-end">
					<p class="text-surface-500 dark:text-surface-400 text-xs md:text-sm">Today</p>
					<h2 class="font-semibold text-sm md:text-lg self-start">{{ chartToday }}{{ unit }}</h2>
				</div>
			</div>
			<Chart :type="chartType" :data="chartData" :options="chartOptions" class="h-[200px] w-full" />
			<p class="text-xs md:text-sm text-surface-500 dark:text-surface-400">{{ subtitle }}</p>
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
	subtitle: {
		type: String,
		required: true,
		default: 'No subtitle provided',
	},
	chartData: {
		type: Object,
		required: true,
	},
	chartType: {
		type: String,
		default: 'line',
	},
	unit: {
		type: String,
		default: '',
	},
})

// get todays date
const today = new Date()

// get in format 10-11
let todayFormatted = today.toLocaleDateString('en-US', {
	month: '2-digit',
	day: '2-digit',
})

// change / with -
todayFormatted = todayFormatted.replace(/\//g, '-')

const chartToday = ref(getChartToday())
function getChartToday() {
	if (!props.chartData || !props.chartData.labels) return 0

	const index = props.chartData.labels.indexOf(todayFormatted)

	if (index === -1) return 0

	const chartToday = props.chartData.datasets[0].data[index] || 0

	return Math.round(chartToday * 100) / 100
}

console.log(chartToday.value)

console.log(todayFormatted)

console.log(props.chartData)

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
					color: 'rgba(192, 192, 192, 0.5)',
					display: true,
				},
			},
			y: {
				beginAtZero: false,
				ticks: {
					stepSize: 2,
					callback: function (value, index, ticks) {
						return value + props.unit
					},
				},
				grid: {
					color: 'rgba(192, 192, 192, 0.5)',
					display: true,
				},
			},
		},
	}
}
</script>
