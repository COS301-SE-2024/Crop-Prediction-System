<template>
	<Card style="overflow: hidden; padding: 20px">
		<template #header>
			<div class="flex flex-row items-center mb-0 justify-center">
				<Dropdown
					v-model="internalSelectedField"
					:options="fields"
					optionLabel="field_name"
					placeholder="Select a Field"
					checkmark
					filter
					:highlightOnSelect="false"
					class="w-full"
				/>
			</div>
		</template>
		<template #title>
			<div class="w-full h-full my-4">
				<h2>
					{{ capitalizeFirstCharacter(internalSelectedField?.crop_type as string) }}
					<span v-show="internalSelectedField" class="text-sm text-surface-600 dark:text-surface-0/60 font-normal"
						>{{ internalSelectedField?.hectare.toFixed(2) }} hectare</span
					>
				</h2>
			</div>
		</template>
		<template #subtitle> </template>
		<template #content>
			<div class="flex flex-col justify-between items-center w-full">
				<div class="w-full flex flex-col gap-4 items-center justify-between">
					<div class="rounded-md bg-gradient-to-r from-[#7951B4] to-[#1C8EDB] p-[0.07rem] w-full">
						<div class="dark:bg-surface-800 bg-surface-100 rounded-md p-4 space-y-2">
							<div class="flex gap-2 items-center">
								<img
									src="../assets/google-gemini-icon.webp"
									alt="Field Image"
									class="rounded-lg h-6 w-6 spinner"
								/>
								<span class="text-sm text-surface-600 dark:text-surface-0/60">AI Weather Summary</span>
							</div>
							<p class="text-surface-600 dark:text-surface-0/60 text-sm">
								{{ getCurrentSummary() }}
							</p>
						</div>
					</div>
					<div
						class="w-full h-[80px] flex items-center justify-between border-2 rounded-md border-surface-300 dark:border-surface-600 p-4 gap-2"
					>
						<!-- First Div Content (40%) -->
						<div class="w-2/5 h-full flex items-center">
							<div class="flex flex-col items-start justify-center">
								<h3 class="text-lg font-semibold text-surface-700 dark:text-surface-0">
									Yield<span class="text-xs md:text-sm text-surface-600 dark:text-surface-0/60"> t/ha</span>
								</h3>
								<p class="text-xs md:text-sm text-surface-600 dark:text-surface-0/60">
									<span v-show="internalSelectedField"
										>5YR Avg: {{ internalSelectedField?.pastYieldAvg.toFixed(2) }}</span
									>
								</p>
							</div>
						</div>
						<!-- Second Div (60%) with chart and value -->
						<div class="w-3/5 h-full flex items-center justify-between gap-2">
							<!-- Chart Section -->
							<div class="w-2/4 h-full flex justify-center items-center">
								<Chart type="line" :data="yieldData" :options="yieldOptions" class="w-full h-full" />
							</div>
							<!-- Value Section -->
							<div class="w-2/4 flex flex-col items-end justify-center">
								<div class="flex flex-col justify-center items-center">
									<h3 class="text-lg font-semibold text-surface-700 dark:text-surface-0">
										{{ yieldStatus.yieldScore }}
									</h3>
									<Tag :value="yieldStatus.percentageDifference" :severity="yieldStatus.severity" />
								</div>
							</div>
						</div>
					</div>
					<div
						class="w-full h-[80px] flex items-center justify-between border-2 rounded-md border-surface-300 dark:border-surface-600 p-4 gap-2"
					>
						<!-- First Div Content (40%) -->
						<div class="w-2/5 h-full flex items-center">
							<div class="flex flex-col items-start justify-center">
								<h3 class="text-lg font-semibold text-surface-700 dark:text-surface-0">Health</h3>
								<p class="text-sm text-surface-600 dark:text-surface-0/60">
									<span v-show="internalSelectedField">Rolling Avg</span>
								</p>
							</div>
						</div>
						<!-- Second Div (60%) with chart and value -->
						<div class="w-3/5 h-full flex items-center justify-between gap-2">
							<!-- Chart Section -->
							<div class="w-2/4 h-full flex items-center">
								<Chart type="line" :data="healthData" :options="yieldOptions" class="w-full h-full" />
							</div>
							<!-- Value Section -->
							<div class="w-2/4 flex flex-col items-end justify-center">
								<div class="flex flex-col justify-center items-center">
									<h3 class="text-lg font-semibold text-surface-700 dark:text-surface-0">
										{{ healthStatus.healthScore }}
									</h3>
									<Tag :value="healthStatus.value" :severity="healthStatus.severity" />
								</div>
							</div>
						</div>
					</div>

					<div class="flex flex-row gap-4 w-full flex-wrap mol:flex-nowrap justify-between items-center">
						<div
							class="flex flex-col gap-1 w-full justify-between items-center border-2 rounded-md border-surface-300 dark:border-surface-600 p-4"
						>
							<Knob
								v-model="sprayabilityFactor"
								valueTemplate="{value}%"
								:strokeWidth="5"
								readonly
								class="select-none pointer-events-none cursor-default"
							/>
							<h4 class="text-sm">Sprayability</h4>
						</div>
						<div
							class="flex flex-col w-full gap-1 justify-between items-center border-2 rounded-md border-surface-300 dark:border-surface-600 p-4"
						>
							<Knob
								v-model="precipitation"
								class="select-none pointer-events-none cursor-default"
								valueTemplate="{value}mm"
								:strokeWidth="5"
								:max="precipitation"
								readonly
							/>
							<h4 class="text-sm">Precipitation</h4>
						</div>
					</div>
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

const yieldData = ref({})
const healthData = ref({})

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
	data?: any
	pastYieldAvg: number
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

function calculatePercentageDifference(currentYield: number, pastYield: number) {
	if (pastYield === 0) {
		return currentYield > 0 ? 100 : currentYield < 0 ? -100 : 0 // Avoid division by zero
	}
	const difference = currentYield - pastYield
	const percentageDifference = (difference / pastYield) * 100
	return Number(percentageDifference.toFixed(2))
}

watch(internalSelectedField, (newField) => {
	emit('update:modelValue', newField)
	updateLineChartData()
	sprayabilityFactor.value = getSprayabilityFactor()
	precipitation.value = getPrecipitation()
})

onMounted(() => {
	updateLineChartData() // Initialize the line chart with the selected field data
})

function updateLineChartData() {
	if (!internalSelectedField.value || !internalSelectedField.value.data) return

	const healthBackgroundColor = getHealthColor(healthStatus.value.healthScore, 0.2)
	const healthBorderColor = getHealthColor(healthStatus.value.healthScore, 1)
	const yieldBackgroundColor = getYieldColor(
		calculatePercentageDifference(yieldStatus.value.yieldScore, internalSelectedField?.value.pastYieldAvg),
		0.2,
	)
	const yieldBorderColor = getYieldColor(
		calculatePercentageDifference(yieldStatus.value.yieldScore, internalSelectedField?.value.pastYieldAvg),
		1,
	)

	healthData.value = {
		labels: internalSelectedField.value.data.date, // Use the field's dates as labels
		datasets: [
			{
				label: 'Health',
				data: internalSelectedField.value.data.pred_health, // Use the field's health data
				fill: true, // Fill the chart area
				backgroundColor: healthBackgroundColor, // Orange fill
				borderColor: healthBorderColor, // Orange border
				borderWidth: 2,
				tension: 0.4, // Smooth line curve
				pointRadius: 0, // No points on the line
			},
		],
	}

	yieldData.value = {
		labels: internalSelectedField.value.data.date, // Use the field's dates as labels
		datasets: [
			{
				label: 'Yield',
				data: internalSelectedField.value.data.pred_yield, // Use the field's yield data
				fill: true, // Fill the chart area
				backgroundColor: yieldBackgroundColor, // Orange fill
				borderColor: yieldBorderColor, // Orange border
				borderWidth: 2,
				tension: 0.4, // Smooth line curve
				pointRadius: 0, // No points on the line
			},
		],
	}
}

const getHealthColor = (value: number, opacity: number) => {
	if (value <= 40) {
		return `rgba(255, 99, 132, ${opacity})` // Red
	} else if (value < 70) {
		return `rgba(248, 114, 22, ${opacity})` // Orange
	} else {
		return `rgba(17, 185, 29, ${opacity})` // Green
	}
}

const getYieldColor = (value: number, opacity: number) => {
	if (value >= 0) {
		return `rgba(17, 185, 29, ${opacity})` // Green
	} else if (value >= -9.99) {
		return `rgba(248, 114, 22, ${opacity})` // Orange
	} else {
		return `rgba(255, 99, 132, ${opacity})` // Red
	}
}

function capitalizeFirstCharacter(str: string) {
	if (!str) return 'Select a Field' // Handle empty strings
	return str.charAt(0).toUpperCase() + str.slice(1)
}

function getCurrentDateFormatted() {
	const date = new Date()

	const month = String(date.getMonth() + 1).padStart(2, '0')
	const day = String(date.getDate()).padStart(2, '0')

	return `${month}-${day}`
}

function getCurrentSummary() {
	if (!internalSelectedField.value || !internalSelectedField.value.data) return 'Please select a field to view the AI summary.'

	const currentDate = getCurrentDateFormatted()
	const index = internalSelectedField.value.data.date.indexOf(currentDate)

	if (index === -1) return 'Please select a field to view the AI summary.'

	return internalSelectedField.value.data.summary[index] || 'Please select a field to view the AI summary.'
}

const sprayabilityFactor = ref(getSprayabilityFactor())
function getSprayabilityFactor() {
	if (!internalSelectedField.value || !internalSelectedField.value.data) return 0

	const currentDate = getCurrentDateFormatted()
	const index = internalSelectedField.value.data.date.indexOf(currentDate)

	if (index === -1) return 0

	const sprayabilityFactor = internalSelectedField.value.data.pred_sprayability[index] || 0

	return Math.round(sprayabilityFactor * 100) / 100
}

const precipitation = ref(getPrecipitation())
function getPrecipitation() {
	if (!internalSelectedField.value || !internalSelectedField.value.data) return 0

	const currentDate = getCurrentDateFormatted()
	const index = internalSelectedField.value.data.date.indexOf(currentDate)

	if (index === -1) return 0

	const precipitation = internalSelectedField.value.data.rain[index] || 0

	return Math.round(precipitation * 100) / 100
}

// Computed property to get the current day's health status and determine the tag
const healthStatus = computed(() => {
	if (!internalSelectedField.value || !internalSelectedField.value.data) {
		return { value: 'Select Field', severity: 'contrast' }
	}

	const currentDate = getCurrentDateFormatted()
	const index = internalSelectedField.value.data.date.indexOf(currentDate)

	if (index === -1) return { value: 'Unknown', severity: 'secondary' }

	const currentHealth = internalSelectedField.value.data.pred_health[index] * 100 || 0

	if (currentHealth >= 70) {
		return { value: 'Healthy', severity: 'primary', healthScore: Number(currentHealth.toFixed(2)) }
	} else if (currentHealth >= 40) {
		return { value: 'Moderate', severity: 'warning', healthScore: Number(currentHealth.toFixed(2)) }
	} else {
		return { value: 'Severe', severity: 'danger', healthScore: Number(currentHealth.toFixed(2)) }
	}
})

const yieldStatus = computed(() => {
	if (!internalSelectedField.value || !internalSelectedField.value.data) {
		return { value: 'Select Field', severity: 'contrast', percentageDifference: `Select Field` }
	}

	const currentDate = getCurrentDateFormatted()
	const index = internalSelectedField.value.data.date.indexOf(currentDate)

	if (index === -1) return { value: 'Unknown', severity: 'secondary' }

	const currentYield = internalSelectedField.value.data.pred_yield[index] || 0

	const percentageDifference = calculatePercentageDifference(currentYield, internalSelectedField.value?.pastYieldAvg)

	if (percentageDifference >= 0) {
		return {
			value: 'Healthy',
			severity: 'primary',
			yieldScore: currentYield.toFixed(2),
			percentageDifference: `${percentageDifference}%`,
		}
	} else if (percentageDifference >= -9.99) {
		return {
			value: 'Moderate',
			severity: 'warning',
			yieldScore: currentYield.toFixed(2),
			percentageDifference: `${percentageDifference}%`,
		}
	} else {
		return {
			value: 'Severe',
			severity: 'danger',
			yieldScore: currentYield.toFixed(2),
			percentageDifference: `${percentageDifference}%`,
		}
	}
})

const yieldOptions = ref({
	responsive: true,
	maintainAspectRatio: false, // Ensure the chart fits its container
	plugins: {
		legend: {
			display: false, // No legend
		},
		tooltip: {
			enabled: false,
		},
	},
	scales: {
		x: {
			display: false, // No x-axis labels or grid
		},
		y: {
			display: false, // No y-axis labels or grid
		},
	},
	interaction: {
		mode: 'none', // Disable click and hover interactions
	},
	hover: {
		mode: null, // Disable hover effects
	},
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
