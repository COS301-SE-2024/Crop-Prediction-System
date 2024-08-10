<template>
	<div class="flex w-full justify-center items-start p-4">
		<div class="flex flex-col justify-start items-start gap-4 w-full">
			<div class="flex flex-col md:flex-row w-full gap-5">
				<div class="w-full md:w-1/3">
					<FieldCard v-model="selectedField" :fields="userFieldsWithData" />
				</div>
				<div class="w-full md:w-2/3 h-96 md:h-auto rounded overflow-hidden border-surface-600 shadow-md">
					<GoogleMapsField :selectedField="selectedField" :fields="userFieldsWithData" />
				</div>
			</div>
			<div class="w-full">
				<Fieldset legend="View More Statistics" :toggleable="true" collapsed>
					<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
						<StatsCard v-if="selectedField" title="Soil Moisture" :chartData="soilMoistureChartData" />
						<StatsCard v-if="selectedField" title="Soil Temperature" :chartData="soilTemperatureChartData" />
						<StatsCard v-if="selectedField" title="Temperature" :chartData="temperatureChartData" />
						<StatsCard v-if="selectedField" title="Dew Point" :chartData="dewPointChartData" />
						<StatsCard v-if="selectedField" title="Humidity" :chartData="humidityChartData" />
						<StatsCard v-if="selectedField" title="Pressure" :chartData="pressureChartData" />
						<StatsCard v-if="selectedField" title="UV Index" :chartData="uvChartData" />
					</div>
				</Fieldset>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, watch } from 'vue'
import FieldCard from '~/components/FieldCard.vue'
import GoogleMapsField from '~/components/GoogleMapsField.vue'
import StatsCard from '~/components/StatsCard.vue'

const selectedField = ref(null)

function transformData(data) {
	const result = {}

	data.forEach((item) => {
		Object.keys(item).forEach((key) => {
			if (key === 'field_id') {
				// Skip adding field_id to the result object
				if (!result[key]) {
					result[key] = item[key] // Just assign the field_id once
				}
			} else {
				if (!result[key]) {
					result[key] = []
				}

				if (key === 'date') {
					// Format the date as "MM-DD"
					const formattedDate = item[key].slice(5) // Get the "MM-DD" part of the date
					result[key].push(formattedDate)
				} else {
					result[key].push(item[key])
				}
			}
		})
	})

	return result
}

const currentUser = useSupabaseUser()

const teamId = await $fetch('/api/getTeamID', {
	params: { userid: currentUser.value.id },
})

const userFields = await $fetch('/api/getUserFields', {
	params: { team_id: teamId.team_id },
})

function getCurrentDateApiRequestFormatted() {
	const date = new Date()

	const year = date.getFullYear() // getFullYear() returns the full year (e.g., 2024)
	const month = String(date.getMonth() + 1).padStart(2, '0') // getMonth() is zero-based, so add 1
	const day = String(date.getDate()).padStart(2, '0') // getDate() gives the day of the month

	return `${year}-${month}-${day}`
}

const currentApiDateFormat = getCurrentDateApiRequestFormatted()

const userFieldsWithData = await Promise.all(
	userFields.map(async (field) => {
		// Fetch field data for each field
		const fieldData = await $fetch('/api/getFieldData', {
			params: { fieldid: field.id, input_date: currentApiDateFormat },
		})

		// Transform the field data
		const transformedFieldData = transformData(fieldData)

		// Add the transformed data to the field object
		return {
			...field,
			data: transformedFieldData,
		}
	}),
)

const soilMoistureChartData = ref({})
const soilTemperatureChartData = ref({})
const temperatureChartData = ref({})
const dewPointChartData = ref({})
const humidityChartData = ref({})
const pressureChartData = ref({})
const uvChartData = ref({})

// Watch for changes to selectedField and update chart data accordingly
watch(selectedField, (newField) => {
	if (newField && newField.data) {
		soilMoistureChartData.value = {
			labels: newField.data.date,
			datasets: [
				{
					label: 'Soil Moisture',
					data: newField.data.soil_moisture,
					fill: false,
					backgroundColor: 'rgba(6, 182, 212, 0.2)',
					borderColor: 'rgba(6, 182, 212, 1)',
					tension: 0.4,
				},
			],
		}

		soilTemperatureChartData.value = {
			labels: newField.data.date,
			datasets: [
				{
					label: 'Soil Temperature',
					data: newField.data.soil_temperature,
					fill: false,
					backgroundColor: 'rgba(248, 114, 22, 0.2)',
					borderColor: 'rgba(248, 114, 22, 1)',
					tension: 0.4,
				},
			],
		}

		temperatureChartData.value = {
			labels: newField.data.date,
			datasets: [
				{
					label: 'Temp Max',
					data: newField.data.tempmax,
					fill: false,
					backgroundColor: 'rgba(76, 175, 80, 0.2)',
					borderColor: 'rgba(76, 175, 80, 1)',
					tension: 0.4,
				},
				{
					label: 'Temp Mean',
					data: newField.data.tempmean,
					fill: false,
					backgroundColor: 'rgba(255, 205, 86, 0.2)',
					borderColor: 'rgba(255, 205, 86, 1)',
					tension: 0.4,
				},
				{
					label: 'Temp Min',
					data: newField.data.tempmin,
					fill: false,
					backgroundColor: 'rgba(255, 99, 132, 0.2)',
					borderColor: 'rgba(255, 99, 132, 1)',
					tension: 0.4,
				},
			],
		}

		dewPointChartData.value = {
			labels: newField.data.date,
			datasets: [
				{
					label: 'Dew Point',
					data: newField.data.dew_point,
					fill: false,
					backgroundColor: 'rgba(226, 226, 226, 0.2)',
					borderColor: 'rgba(226, 226, 226, 1)',
					tension: 0.4,
				},
			],
		}

		humidityChartData.value = {
			labels: newField.data.date,
			datasets: [
				{
					label: 'Humidity',
					data: newField.data.humidity,
					fill: false,
					backgroundColor: 'rgba(168,84,246, 0.2)',
					borderColor: 'rgba(168,84,246, 1)',
					tension: 0.4,
				},
			],
		}

		pressureChartData.value = {
			labels: newField.data.date,
			datasets: [
				{
					label: 'Pressure',
					data: newField.data.pressure,
					fill: false,
					backgroundColor: 'rgba(255, 99, 132, 0.2)',
					borderColor: 'rgba(255, 99, 132, 1)',
					tension: 0.4,
				},
			],
		}

		uvChartData.value = {
			labels: newField.data.date,
			datasets: [
				{
					label: 'UV Index',
					data: newField.data.uvi,
					fill: false,
					backgroundColor: 'rgba(255, 205, 86, 0.2)',
					borderColor: 'rgba(255, 205, 86, 1)',
					tension: 0.4,
				},
			],
		}
	}
})

definePageMeta({
	middleware: 'auth',
})
</script>
