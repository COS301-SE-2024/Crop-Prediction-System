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
				<!-- Displaying current time period -->
			</div>
		</div>
	</div>
</template>

<script setup>
import Chart from 'primevue/chart'
import { ref, computed, onMounted } from 'vue'

// Slider parameters
const sliderValue = ref(0) // Default slider position (starts at first data point)
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

// Chart options initialization
const chartOptions = ref()
onMounted(() => {
	chartOptions.value = setChartOptions()
})

// Computed property to update the displayed data for the current slider position
const currentChartData = computed(() => {
	return {
		labels: [chartLabels[sliderValue.value]], // Display the label for the selected slider position
		datasets: props.chartData.datasets.map((dataset) => ({
			...dataset,
			data: [dataset.data[sliderValue.value]], // Show only the data for the selected time period
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

// Update the chart data when the slider changes (optional: add custom behavior)
const updateChartData = () => {
	console.log('Slider Value:', sliderValue.value)
}
</script>

<style scoped>
.custom-slider {
	display: flex;
	align-items: center;
	gap: 10px;
}

.slider {
	width: 200px;
	accent-color: #007bff;
}

.slider::-webkit-slider-thumb {
	width: 20px;
	height: 20px;
	background: #007bff;
	border-radius: 50%;
	cursor: pointer;
}

.slider::-moz-range-thumb {
	width: 20px;
	height: 20px;
	background: #007bff;
	border-radius: 50%;
	cursor: pointer;
}
</style>
