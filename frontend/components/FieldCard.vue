<template>
	<Card style="overflow: hidden; padding: 10px">
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
		<template #title>{{ internalSelectedField?.crop_type.toUpperCase() || 'Select a field' }}</template>
		<template #subtitle>
			<div class="flex flex-col justify-between items-start gap-1">
				<h4 class="text-lg">
					{{ internalSelectedField?.field_tph ? `Expected T/H: ${internalSelectedField.field_tph}` : '' }}
				</h4>
				<Tag value="Healthy" severity="success" rounded></Tag>
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
import { ref, watch, onMounted } from 'vue'
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
})

const lineChartData = ref()
const lineChartOptions = ref()
const barChartData = ref()
const barChartOptions = ref()

onMounted(() => {
	lineChartData.value = setLineChartData()
	lineChartOptions.value = setChartOptions()
	barChartData.value = setBarChartData()
	barChartOptions.value = setBarChartOptions()
})

const setLineChartData = () => {
	return {
		labels: ['07-25', '07-26', '07-27', '07-28', '07-29', '07-30', '07-31', '08-01'],
		datasets: [
			{
				label: 'Field Health',
				data: [65, 59, 80, 81, 56, 55, 82, 95],
				fill: false,
				backgroundColor: 'rgba(76, 175, 80, 0.2)',
				borderColor: '#4CAF50',
				tension: 0.4,
			},
		],
	}
}

const sprayAbility = [0.6, 0.4, 0, 0.05, 0.8, 0.92, 0.82, 0.37]

const getColor = (value: number, opacity: number) => {
	if (value <= 0.4) {
		return `rgba(255, 99, 132, ${opacity})` // Red
	} else if (value <= 0.74) {
		return `rgba(255, 205, 86, ${opacity})` // Orange
	} else {
		return `rgba(76, 175, 80, ${opacity})` // Green
	}
}

const setBarChartData = () => {
	const backgroundColors = sprayAbility.map((value) => getColor(value, 0.2))
	const borderColors = sprayAbility.map((value) => getColor(value, 1))

	return {
		labels: ['07-25', '07-26', '07-27', '07-28', '07-29', '07-30', '07-31', '08-01'],
		datasets: [
			{
				label: 'Precipitation',
				data: [2.3, 5.14, 0.0, 12, 1.8, 0.9, 2.1, 4.7],
				backgroundColor: backgroundColors,
				borderColor: borderColors,
				borderWidth: 1,
				barPercentage: 0.8,
				categoryPercentage: 0.8,
				maxBarThickness: 45,
			},
		],
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
				beginAtZero: true,
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
				beginAtZero: true,
				ticks: {
					stepSize: 5,
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

<style scoped>
/* Add any necessary styles here */
</style>
