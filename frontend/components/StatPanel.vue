<template>
	<div class="w-96 grid gap-5 border border-surface-border p-6 rounded-lg shadow-lg">
		<div>
			<p class="text-lg font-[500] text-surface-400">{{ title }}</p>
		</div>
		<div>
			<Chart :type="chartType" :data="chartData" :options="chartOptions" class="h-24" />
		</div>
		<div class="flex justify-between">
			<p>
				<span class="text-sm font-[500]" :class="value > 0 ? 'text-green-500' : 'text-red-500'"
					>{{ value > 0 ? '+' + value : value }}%</span
				>
				<span class="text-sm font-[500] text-surface-500"> from last week</span>
			</p>
			<!-- between 0 and 0.3. Between 0.3 and 0,6. Between 0.6 and 1.0 -->
			<Tag
				:severity="convertedValue < 0 ? 'danger' : convertedValue < 0.6 ? 'warning' : 'success'"
				:value="convertedValue < 0 ? 'Severe' : convertedValue < 0.6 ? 'Moderate' : 'Healthy'"
				rounded
			></Tag>
		</div>
	</div>
</template>

<script setup lang="ts">
import Chart from 'primevue/chart'
import Tag from 'primevue/tag'
import { ref, onMounted, defineProps } from 'vue'

const props = defineProps({
	title: {
		type: String,
		required: true,
	},
	chartInput: {
		type: Object,
		required: true,
	},
	chartType: {
		type: String,
		default: 'line',
	},
	explanation: {
		type: Boolean,
		default: true,
	},
})

// divide last week's value by this week's value
const value = ref(0)
value.value = Math.floor(
	(props.chartInput[props.chartInput.length - 1] / props.chartInput[props.chartInput.length - 2] - 1) * 100,
)

const convertedValue = ref(0)
convertedValue.value = value.value / 100

// use time to get the last 6 weeks
const time = new Date()
time.setDate(time.getDate() - 7 * 6)

// make an array to set the labels
const labels = ref<string[]>([])
for (let i = time.getDate(); i < time.getDate() + 7; i++) {
	time.setDate(time.getDate() + 1)
	labels.value.push('Week ' + i)
}

onMounted(() => {
	chartData.value = setChartData()
	chartOptions.value = setChartOptions()
})

const chartData = ref()
const chartOptions = ref()

const setChartData = () => {
	return {
		labels: labels,
		datasets: [
			{
				label: false,
				data: props.chartInput,
				fill: true,
				backgroundColor: 'rgba(76, 175, 80, 0.2)',
				borderColor: '#4CAF50',
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
			legend: {
				display: false,
			},
		},
		scales: {
			x: {
				ticks: {
					display: false,
				},
				grid: {
					display: false,
				},
			},
			y: {
				ticks: {
					display: false,
				},
				grid: {
					display: false,
				},
			},
		},
	}
}
</script>
