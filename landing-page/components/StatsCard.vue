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

const hardcodedData = {
	SoilMoisture: [20, 25, 30, 28, 35, 33, 40],
	SoilTemperature: [10, 12, 14, 13, 15, 17, 18],
	Temperature: {
		Max: [32, 33, 30, 26, 23, 23, 18],
		Mean: [25, 27, 28, 26, 30, 29, 31],
		Min: [15, 17, 19, 18, 20, 21, 22],
	},
	DewPoint: [5, 6, 7, 8, 9, 10, 11],
	Humidity: [65, 60, 70, 68, 75, 73, 80],
	Pressure: [1012, 1010, 1013, 1015, 1017, 1014, 1016],
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

// Function to generate chart data
function generateChartData() {
	switch (props.title) {
		case 'Soil Moisture':
			return {
				labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
				datasets: [
					{
						label: 'Soil Moisture',
						data: hardcodedData.SoilMoisture,
						fill: false,
						borderColor: 'rgba(6, 182, 212, 1)',
						tension: 0.4,
						borderWidth: 3,
					},
				],
			}
		case 'Soil Temperature':
			return {
				labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
				datasets: [
					{
						label: 'Soil Temperature',
						data: hardcodedData.SoilTemperature,
						fill: false,
						borderColor: 'rgba(248, 114, 22, 1)',
						tension: 0.4,
						borderWidth: 3,
					},
				],
			}
		case 'Temperature':
			return {
				labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
				datasets: [
					{
						label: 'Max',
						data: hardcodedData.Temperature.Max,
						borderColor: 'rgba(76, 175, 80, 1)',
						fill: false,
						tension: 0.4,
						borderWidth: 3,
					},
					{
						label: 'Mean',
						data: hardcodedData.Temperature.Mean,
						borderColor: 'rgba(255, 205, 86, 1)',
						fill: false,
						tension: 0.4,
						borderWidth: 3,
					},
					{
						label: 'Min',
						data: hardcodedData.Temperature.Min,
						borderColor: 'rgba(255, 99, 132, 1)',
						fill: false,
						tension: 0.4,
						borderWidth: 3,
					},
				],
			}
		case 'Dew Point':
			return {
				labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
				datasets: [
					{
						label: 'Dew Point',
						data: hardcodedData.DewPoint,
						fill: false,
						borderColor: 'rgba(226, 226, 226, 1)',
						tension: 0.4,
						borderWidth: 3,
					},
				],
			}
		case 'Humidity':
			return {
				labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
				datasets: [
					{
						label: 'Humidity',
						data: hardcodedData.Humidity,
						fill: false,
						borderColor: 'rgba(168, 84, 246, 1)',
						tension: 0.4,
						borderWidth: 3,
					},
				],
			}
		case 'Pressure':
			return {
				labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
				datasets: [
					{
						label: 'Pressure',
						data: hardcodedData.Pressure,
						fill: false,
						borderColor: 'rgba(255, 99, 132, 1)',
						tension: 0.4,
						borderWidth: 3,
					},
				],
			}
		default:
			return {}
	}
}

// Chart options initialization
const chartOptions = ref()

onMounted(() => {
	chartOptions.value = setChartOptions()
})

// Function to set chart options
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
