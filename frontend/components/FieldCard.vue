<template>
	<Card style="overflow: hidden; padding: 10px; box-shadow: none">
		<template #header>
			<div class="flex flex-row items-center justify-center">
				<Dropdown
					v-model="internalSelectedField"
					:options="fields"
					optionLabel="field_name"
					placeholder="Select a Field"
					checkmark
					:highlightOnSelect="false"
					class="w-full"
				/>
			</div>
		</template>
		<template #title>{{ capitalizeFirstCharacter(internalSelectedField?.crop_type as string) }}</template>
		<template #subtitle>
			<div class="flex flex-row justify-between items-center">
				<h4 class="text-lg">Expected Yield: {{ calculateYield() }}t</h4>
				<Tag :value="healthStatus.value" :severity="healthStatus.severity" rounded></Tag>
			</div>
			<div class="mt-4 rounded-md bg-gradient-to-r from-[#7951B4] to-[#1C8EDB] p-[0.07rem]">
				<div class="bg-surface-800 rounded-md p-4 space-y-2">
					<div class="flex gap-2 items-center">
						<img src="../assets/google-gemini-icon.webp" alt="Field Image" class="rounded-lg h-6 w-6 spinner" />
						<span class="text-sm text-gray-400">AI Weather Summary</span>
					</div>
					<p>
						{{ getCurrentSummary() }}
					</p>
				</div>
			</div>
		</template>
		<template #content>
			<div class="flex flex-col justify-between items-center gap-8 w-full">
				<div class="flex flex-col gap-2 justify-between items-center w-full">
					<div class="flex flex-row justify-center items-center gap-4">
						<h3 class="font-semibold text-lg">Field Health</h3>
						<Button
							icon="pi pi-question-circle"
							rounded
							severity="secondary"
							size="small"
							text
							v-tooltip
							@click="healthVisible = true"
						/>
						<Dialog v-model:visible="healthVisible" modal header="Field Health" :style="{ width: '350px' }">
							<p>
								The Field Health chart shows the health status of the field over time. It helps monitor trends in
								field health for better management.
							</p>
						</Dialog>
					</div>
					<Chart type="line" :data="lineChartData" :options="lineChartOptions" class="h-34 w-full" />
				</div>
				<div class="flex flex-col gap-2 justify-between items-center w-full">
					<div class="flex flex-row justify-center items-center gap-4">
						<h3 class="font-semibold text-lg">Precipitation (mm) and Sprayability</h3>
						<Button
							icon="pi pi-question-circle"
							rounded
							severity="secondary"
							size="small"
							text
							v-tooltip
							@click="precVisible = true"
						/>
						<Dialog
							v-model:visible="precVisible"
							modal
							header="Precipitation and Sprayability"
							:style="{ width: '350px' }"
						>
							<p>
								The Precipitation and Sprayability chart provides insights into how rainfall affects the
								suitability for spraying crops. Higher precipitation generally reduces sprayability, while lower
								precipitation generally increases sprayability.
							</p>
							<div class="flex flex-col w-full gap-1 justify-between items-start mt-5">
								<strong class="text-lg">Sprayability Categories:</strong>
								<span
									><strong style="color: rgba(76, 175, 80, 1)">Suitable:</strong> Ideal conditions for
									spraying.</span
								>
								<span
									><strong style="color: rgba(255, 205, 86, 1)">Partially Suitable:</strong> Conditions may not
									be optimal for spraying.</span
								>
								<span
									><strong style="color: rgba(255, 99, 132, 1)">Not Suitable:</strong> Conditions are
									unfavorable for spraying.</span
								>
							</div>
						</Dialog>
					</div>
					<Chart type="bar" :data="barChartData" :options="barChartOptions" class="h-34 w-full" />
					<CustomLegend />
				</div>
			</div>
		</template>
	</Card>
</template>

<script setup lang="ts">
import { ref, watch, computed, onMounted } from 'vue'
import Card from 'primevue/card'
import Dropdown from 'primevue/dropdown'
import Chart from 'primevue/chart'
import Tag from 'primevue/tag'
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import CustomLegend from './CustomLegend.vue'

const healthVisible = ref(false)
const precVisible = ref(false)

interface Field {
	id: number
	created_at: string
	field_area: [number, number][]
	field_name: string
	field_tph: number
	field_health: number
	crop_type: string
	team_id: string
	updated_at: string
	hectare: number
	data?: any // assuming this holds the transformed data
}

const props = defineProps({
	modelValue: {
		type: Object as () => Field | null,
		default: null,
	},
	fields: {
		type: Array as () => Field[],
		default: () => [],
	},
})

const emit = defineEmits(['update:modelValue'])

const internalSelectedField = ref<Field | null>(props.modelValue)

watch(
	() => props.modelValue,
	(newField) => {
		internalSelectedField.value = newField
	},
)

watch(internalSelectedField, (newField) => {
	emit('update:modelValue', newField)
	updateLineChartData()
	updateBarChartData() // Update bar chart data when selected field changes
})

const lineChartData = ref()
const lineChartOptions = ref()
const barChartData = ref()
const barChartOptions = ref()

onMounted(() => {
	lineChartOptions.value = setChartOptions()
	barChartOptions.value = setBarChartOptions()
	updateLineChartData() // Initialize the line chart with the selected field data
	updateBarChartData() // Initialize the bar chart with the selected field data
})

function updateLineChartData() {
	if (!internalSelectedField.value || !internalSelectedField.value.data) return

	lineChartData.value = {
		labels: internalSelectedField.value.data.date, // Use the field's dates as labels
		datasets: [
			{
				label: 'Field Health',
				data: internalSelectedField.value.data.health, // Use the field's health data
				fill: false,
				backgroundColor: 'rgba(76, 175, 80, 0.2)',
				borderColor: '#4CAF50',
				tension: 0.4,
			},
		],
	}
}

function updateBarChartData() {
	if (!internalSelectedField.value || !internalSelectedField.value.data) return

	const sprayabilityData = internalSelectedField.value.data.sprayability || []
	const backgroundColors = sprayabilityData.map((value: number) => getColor(value, 0.2))
	const borderColors = sprayabilityData.map((value: number) => getColor(value, 1))

	barChartData.value = {
		labels: internalSelectedField.value.data.date, // Use the field's dates as labels
		datasets: [
			{
				type: 'bar',
				label: 'Sprayability',
				data: sprayabilityData,
				backgroundColor: backgroundColors,
				borderColor: borderColors,
				borderWidth: 1,
				barPercentage: 0.8,
				categoryPercentage: 1,
				maxBarThickness: 45,
			},
			{
				type: 'line',
				label: 'Precipitation',
				data: internalSelectedField.value.data.rain,
				fill: false,
				backgroundColor: 'rgba(34, 140, 255, 0.2)',
				borderColor: 'rgba(34, 140, 255, 1)',
				tension: 0.4,
			},
		],
	}
}

const getColor = (value: number, opacity: number) => {
	if (value <= 40) {
		return `rgba(255, 99, 132, ${opacity})` // Red
	} else if (value <= 74) {
		return `rgba(255, 205, 86, ${opacity})` // Orange
	} else {
		return `rgba(76, 175, 80, ${opacity})` // Green
	}
}

const setChartOptions = () => {
	return {
		maintainAspectRatio: false,
		responsive: true,
		plugins: {
			legend: {
				display: false,
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
					stepSize: 10,
				},
				grid: {
					color: 'rgba(192, 192, 192, 0.3)',
					display: true,
				},
			},
		},
	}
}

const setBarChartOptions = () => {
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
					stepSize: 10,
				},
				grid: {
					color: 'rgba(192, 192, 192, 0.3)',
					display: true,
				},
			},
		},
	}
}

function capitalizeFirstCharacter(str: string) {
	if (!str) return '' // Handle empty strings
	return str.charAt(0).toUpperCase() + str.slice(1)
}

function getCurrentDateFormatted() {
	const date = new Date()

	const month = String(date.getMonth() + 1).padStart(2, '0')
	const day = String(date.getDate()).padStart(2, '0')

	return `${month}-${day}`
}

function getCurrentSummary() {
	if (!internalSelectedField.value || !internalSelectedField.value.data) return 'No summary available'

	const currentDate = getCurrentDateFormatted()
	const index = internalSelectedField.value.data.date.indexOf(currentDate)

	if (index === -1) return 'No summary available'

	return internalSelectedField.value.data.summary[index] || 'No summary available'
}

function calculateYield() {
	if (!internalSelectedField.value || !internalSelectedField.value.data) return '0'

	const currentDate = getCurrentDateFormatted()
	const index = internalSelectedField.value.data.date.indexOf(currentDate)

	if (index === -1) return '0'

	const yieldPerHectare = internalSelectedField.value.data.yield[index] || 0

	return (yieldPerHectare * internalSelectedField.value.hectare).toFixed(2)
}

// Computed property to get the current day's health status and determine the tag
const healthStatus = computed(() => {
	if (!internalSelectedField.value || !internalSelectedField.value.data) {
		return { value: 'Unknown', severity: 'secondary' }
	}

	const currentDate = getCurrentDateFormatted()
	const index = internalSelectedField.value.data.date.indexOf(currentDate)

	if (index === -1) return { value: 'Unknown', severity: 'secondary' }

	const currentHealth = internalSelectedField.value.data.health[index] || 0

	if (currentHealth >= 70) {
		return { value: 'Healthy', severity: 'success' }
	} else if (currentHealth >= 40) {
		return { value: 'Moderate', severity: 'warning' }
	} else {
		return { value: 'Severe', severity: 'danger' }
	}
})
</script>

<style scoped>
.spinner {
	animation-name: spin;
	animation-duration: 4s;
	animation-iteration-count: infinite;
}

@keyframes spin {
	0% {
		transform: rotate(0deg);
	}
	100% {
		transform: rotate(360deg);
	}
}
</style>
