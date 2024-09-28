<template>
	<div class="w-full border border-surface-border dark:border-surface-600 p-6 rounded-lg">
		<div class="w-full flex flex-col gap-4 justify-between items-center">
			<h2 class="font-semibold text-lg self-start">{{ title }}</h2>
			<Chart :type="chartType" :data="chartData" :options="chartOptions" class="h-[200px] w-full" />
		</div>
	</div>
</template>

<script setup>
import Chart from 'primevue/chart'
import { ref, onMounted } from 'vue'

const dateLabels = ['20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '1', '2', '3']

const fixedData = {
	Temperature: {
		Max: [30.5, 29.2, 31.0, 32.0, 33.5, 30.1, 31.4, 28.7, 27.5, 22.8, 28.4, 29.2, 31.0, 29.5],
		Mean: [27.5, 26.0, 28.0, 28.5, 29.5, 27.0, 28.0, 26.5, 22.0, 18.5, 26.0, 26.5, 28.0, 27.0],
		Min: [24.0, 22.0, 23.0, 24.0, 26.0, 23.5, 24.5, 22.0, 17, 14.2, 21.5, 22.0, 24.0, 23.0],
	},
	Humidity: [60, 57, 50, 53, 58, 60, 62, 66, 64, 61, 59, 68, 65, 60],
	Rainfall: [15.5, 8, 0, 2, 18.9, 5.0, 7.1, 15.4, 20.8, 35.2, 28.5, 30.1, 25.7, 15.9],
	SoilMoisture: [31.5, 30.5, 30.0, 35.5, 38.0, 34.7, 36.5, 38.0, 43.5, 38.5, 34.2, 36.0, 34.0, 36.0],
	SoilTemperature: [20.5, 20.1, 20.8, 21.5, 20.7, 21.5, 22.0, 21.0, 21.2, 18.9, 21.0, 21.5, 21.8, 21.2],
	DewPoint: [17.5, 16.5, 17.0, 18.0, 18.5, 18.0, 17.0, 17.5, 17.2, 16.8, 17.0, 17.5, 18.0, 18.2],
}

const props = defineProps({
	title: {
		type: String,
		required: true,
	},
	chartType: {
		type: String,
		default: 'line',
	},
})

const chartData = ref(generateChartData())

function generateChartData() {
	const baseConfig = {
		labels: dateLabels,
		datasets: [],
	}

	const createDataset = (label, data, color) => {
		const currentDayIndex = 10 // Index of the current day (11th day in our 14-day range)
		return {
			label: label,
			data: data,
			borderColor: color,
			backgroundColor: color,
			fill: false,
			tension: 0.4,
			borderWidth: 2,
			segment: {
				borderDash: (ctx) => (ctx.p0DataIndex >= currentDayIndex ? [5, 5] : undefined),
			},
		}
	}

	switch (props.title) {
		case 'Temperature':
			baseConfig.datasets = [
				createDataset('Max (°C)', fixedData.Temperature.Max, 'rgba(76, 175, 80, 1)'),
				createDataset('Mean (°C)', fixedData.Temperature.Mean, 'rgba(255, 205, 86, 1)'),
				createDataset('Min (°C)', fixedData.Temperature.Min, 'rgba(255, 99, 132, 1)'),
			]
			break
		case 'Rainfall':
			baseConfig.datasets = [createDataset('Rainfall (mm)', fixedData.Rainfall, 'rgba(255, 152, 0, 1)')]
			break
		case 'Humidity':
			baseConfig.datasets = [createDataset('Humidity (%)', fixedData.Humidity, 'rgba(3, 169, 244, 1)')]
			break
		case 'Soil Moisture':
			baseConfig.datasets = [createDataset('Soil Moisture (%)', fixedData.SoilMoisture, 'rgba(6, 182, 212, 1)')]
			break
		case 'Soil Temperature':
			baseConfig.datasets = [createDataset('Soil Temperature (°C)', fixedData.SoilTemperature, 'rgba(248, 114, 22, 1)')]
			break
		case 'Dew Point':
			baseConfig.datasets = [createDataset('Dew Point (°C)', fixedData.DewPoint, 'rgba(156, 39, 176, 1)')]
			break
		default:
			return {}
	}

	return baseConfig
}

const chartOptions = ref()

onMounted(() => {
	chartOptions.value = setChartOptions()
})

const setChartOptions = () => {
	return {
		maintainAspectRatio: false,
		responsive: true,
		plugins: {
			legend: {
				display: true,
			},
			tooltip: {
				mode: 'index',
				intersect: false,
			},
		},
		scales: {
			x: {
				ticks: {
					autoSkip: true,
					maxTicksLimit: 7,
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
