<template>
	<div class="w-full">
		<Panel
			:header="!selectedField ? 'Select a field to view stats' : 'More Field Stats'"
			:toggleable="!!selectedField"
			collapsed
		>
			<div class="w-full flex flex-col justify-center items-center gap-4 relative">
				<div class="flex w-full gap-4 mol:flex-row mos:flex-col justify-between items-center">
					<SelectButton
						:modelValue="filter"
						@update:modelValue="$emit('update:filter', $event)"
						:options="filterOptions"
						optionLabel="name"
					/>
					<Button icon="pi pi-question-circle" outlined severity="secondary" size="small" class="h-full" />
				</div>
				<div v-if="selectedField" class="grid gap-4 w-full" :class="filter.value === 30 ? 'grid-cols-1' : 'grid-cols-2'">
					<StatsCard v-for="(data, key) in chartData" :key="key" :title="getTitle(key)" :chartData="data" />
				</div>
			</div>
			<Skeleton v-if="!selectedField" height="200px"></Skeleton>
		</Panel>
	</div>
</template>

<script setup>
import { computed } from 'vue'
import StatsCard from './StatsCard.vue'

const props = defineProps({
	selectedField: Object,
	filter: Object,
	filterOptions: Array,
	chartData: Object,
})

const emit = defineEmits(['update:filter'])

const getTitle = (key) => {
	const titles = {
		soilMoisture: 'Soil Moisture',
		soilTemperature: 'Soil Temperature (°C)',
		temperature: 'Temperature (°C)',
		dewPoint: 'Dew Point (°C)',
		humidity: 'Humidity',
		pressure: 'Pressure',
		uv: 'UV Index',
		sprayability: 'Sprayability',
		precipitation: 'Precipitation (mm)',
	}
	return titles[key] || key
}
</script>
