<template>
	<div class="w-full border border-surface-border dark:border-surface-600 p-6 rounded-lg">
		<div class="w-full flex flex-col gap-4 justify-between items-center">
			<h2 class="font-semibold text-lg self-start">{{ title }}</h2>
			<Chart :type="chartType" :data="currentChartData" :options="chartOptions" class="h-[200px] w-full" />
			<div class="custom-slider">
				<input
					type="range"
					:min="min"
					:max="max"
					:step="step"
					v-model="sliderValue"
					@input="updateChartData"
					class="slider"
				/>
				<span>{{ chartLabels[sliderValue] }}</span>
				<!-- Displaying current month -->
			</div>
		</div>
	</div>
</template>

<script setup>
import Chart from 'primevue/chart'
import { ref, computed, onMounted } from 'vue'

// Slider parameters
const sliderValue = ref(0) // Default slider position (starts at the first data point)
const min = 0
const max = 6 // Assuming 7 data points (Jan to Jul)
const step = 1

// Props for chart configuration
const props = defineProps({
	title: {
		type: String,
		required: true,
	},
	chartType: {
		type: String,
		default: 'line',
	},
	chartData: {
		type: Object,
		required: true,
	},
})

// Labels for each data point (e.g., months)
const chartLabels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul']

// Array to store the locked data points
const lockedData = ref(props.chartData.datasets.map((dataset) => dataset.data.map(() => null)))

// Chart options initialization
const chartOptions = ref()
onMounted(() => {
	chartOptions.value = setChartOptions()
})

// Generate random data for future months
const getRandomData = () => Math.floor(Math.random() * 100)

// Function to lock data for current and previous months
const lockData = () => {
	props.chartData.datasets.forEach((dataset, datasetIndex) => {
		// Lock data up to the current slider value
		for (let i = 0; i <= sliderValue.value; i++) {
			lockedData.value[datasetIndex][i] = dataset.data[i]
		}
	})
}

// Computed property to display locked data up to the current slider value, and predicted data after that
const currentChartData = computed(() => {
	return {
		labels: chartLabels, // Always show all the months
		datasets: props.chartData.datasets.map((dataset, datasetIndex) => ({
			...dataset,
			data: dataset.data.map((value, index) => {
				// Use locked data up to the slider value, randomize data for future months
				if (index <= sliderValue.value) {
					// Return locked data (real data from the past)
					return lockedData.value[datasetIndex][index]
				} else {
					// Return predicted data (randomized data for the future)
					return getRandomData()
				}
			}),
		})),
	}
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

// Update the chart data when the slider changes
const updateChartData = () => {
	// Lock data for months up to the current slider value
	lockData()
	console.log('Slider Value:', sliderValue.value)
}
</script>
