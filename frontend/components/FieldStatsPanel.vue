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
					<StatsCard
						v-for="(data, key) in chartData"
						:key="key"
						:title="getTitle(key)"
						:subtitle="getSubtitle(key)"
						:chartData="data"
					/>
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

const getSubtitle = (key) => {
	const subtitles = {
		soilMoisture: 'The amount of water in the soil as a percentage',
		soilTemperature: 'The temperature of the soil in degrees Celsius',
		temperature: 'The temperature in degrees Celsius',
		dewPoint: 'The temperature at which air becomes saturated with water vapor',
		humidity: 'The amount of water vapor in the air as a percentage',
		pressure: 'The force exerted by the atmosphere on a surface',
		uv: 'The strength of ultraviolet radiation from the sun',
		sprayability: 'The suitability to spray chemicals on crops',
		precipitation: 'The amount of rain that has fallen in millimeters',
	}
	return subtitles[key] || key
}
</script>
