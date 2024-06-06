<template>
	<div>
		<div>
			<Chart type="polarArea" :data="chartData" :options="chartOptions" class="h-96" />
		</div>
	</div>
</template>

<script setup lang="ts">
import { maxLength } from '@vuelidate/validators'
import Chart from 'primevue/chart'
import { ref, onMounted, defineProps } from 'vue'

const props = defineProps({
	chartInput: {
		type: Object,
		required: true,
	},
})

onMounted(() => {
	chartData.value = setChartData()
	chartOptions.value = setChartOptions()
})

const chartData = ref()
const chartOptions = ref()

const setChartData = () => {
	return {
		labels: ['Moisture', 'Temperature', 'Humidity', 'Soil', 'Rainfall'],
		datasets: [
			{
				label: false,
				data: props.chartInput,
				fill: true,
				backgroundColor: [
					// moisture
					'rgba(255, 99, 132, 0.2)',
					// temperature
					'rgba(54, 162, 235, 0.2)',
					// humidity
					'rgba(255, 206, 86, 0.2)',
					// soil
					'rgba(75, 192, 192, 0.2)',
					// rainfall
					'rgba(153, 102, 255, 0.2)',
				],
				borderColor: [
					// moisture
					'rgba(255, 99, 132, 1)',
					// temperature
					'rgba(54, 162, 235, 1)',
					// humidity
					'rgba(255, 206, 86, 1)',
					// soil
					'rgba(75, 192, 192, 1)',
					// rainfall
					'rgba(153, 102, 255, 1)',
				],
				tension: 0.4,
			},
		],
	}
}
const setChartOptions = () => {
	return {
		maintainAspectRatio: false,
		responsive: true,
		width: 100,
		plugins: {
			labels: {
				display: false,
			},
		},
		scales: {
			// x: {
			// 	ticks: {
			// 		display: false,
			// 	},
			// 	grid: {
			// 		display: false,
			// 	},
			// },
			// y: {
			// 	ticks: {
			// 		display: false,
			// 	},
			// 	grid: {
			// 		display: false,
			// 	},
			// },
			r: {
				ticks: {
					display: false,
				},
				grid: {
					color: 'rgba(192, 192, 192, 0.2)',
				},
				max: 1,
			},
		},
	}
}
</script>
