<template>
	<div class="flex w-full justify-center items-start p-4">
		<div class="flex flex-col justify-start items-start gap-4 w-full">
			<!-- Ensure that FieldCard and GoogleMapsField are rendered even if userFieldsWithData is empty -->
			<div class="flex flex-col md:flex-row w-full gap-5">
				<div class="w-full md:w-1/3">
					<FieldCard v-model="selectedField" :fields="userFieldsWithData" />
				</div>
				<div class="w-full md:w-2/3 h-96 md:h-auto rounded overflow-hidden border-surface-600 shadow-md">
					<GoogleMapsField :selectedField="selectedField" :fields="userFieldsWithData" />
				</div>
			</div>

			<!-- Render the Fieldset and StatsCards even if no field is selected -->
			<div class="w-full">
				<Fieldset legend="View More Statistics" :toggleable="true" collapsed>
					<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
						<!-- These StatsCard components will render, but they may not show any data if selectedField is null -->
						<StatsCard title="Soil Moisture" :chartData="soilMoistureChartData" />
						<StatsCard title="Soil Temperature" :chartData="soilTemperatureChartData" />
						<StatsCard title="Temperature" :chartData="temperatureChartData" />
						<StatsCard title="Dew Point" :chartData="dewPointChartData" />
						<StatsCard title="Humidity" :chartData="humidityChartData" />
						<StatsCard title="Pressure" :chartData="pressureChartData" />
						<StatsCard title="UV Index" :chartData="uvChartData" />
					</div>
				</Fieldset>
			</div>
			<!-- Show a message if no fields are available -->
			<div v-if="userFieldsWithData.length === 0">
				<p class="text-center text-gray-500">You have no fields available.</p>
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
				if (!result[key]) {
					result[key] = item[key]
				}
			} else {
				if (!result[key]) {
					result[key] = []
				}

				if (key === 'date') {
					const formattedDate = item[key].slice(5)
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

let userFields = []
const userFieldsResponse = await $fetch('/api/getUserFields', {
	params: { team_id: teamId.team_id },
})

if (Array.isArray(userFieldsResponse)) {
	userFields = userFieldsResponse
} else {
	console.error('Error fetching user fields:', userFieldsResponse.error || userFieldsResponse)
}

const userFieldsWithData = await Promise.all(
	(userFields.length > 0 ? userFields : []).map(async (field) => {
		const fieldData = await $fetch('/api/getFieldData', {
			params: { fieldid: field.id, input_date: getCurrentDateApiRequestFormatted() },
		})

		const transformedFieldData = transformData(fieldData)

		return {
			...field,
			data: transformedFieldData,
		}
	}),
)

function getCurrentDateApiRequestFormatted() {
	const date = new Date()
	const year = date.getFullYear()
	const month = String(date.getMonth() + 1).padStart(2, '0')
	const day = String(date.getDate()).padStart(2, '0')
	return `${year}-${month}-${day}`
}

const soilMoistureChartData = ref({})
const soilTemperatureChartData = ref({})
const temperatureChartData = ref({})
const dewPointChartData = ref({})
const humidityChartData = ref({})
const pressureChartData = ref({})
const uvChartData = ref({})

watch(selectedField, (newField) => {
	if (newField && newField.data) {
		soilMoistureChartData.value = {
			labels: newField.data.date || [],
			datasets: [
				{
					label: 'Soil Moisture',
					data: newField.data.soil_moisture || [],
					fill: false,
					backgroundColor: 'rgba(6, 182, 212, 0.2)',
					borderColor: 'rgba(6, 182, 212, 1)',
					tension: 0.4,
				},
			],
		}

		soilTemperatureChartData.value = {
			labels: newField.data.date || [],
			datasets: [
				{
					label: 'Soil Temperature',
					data: newField.data.soil_temperature || [],
					fill: false,
					backgroundColor: 'rgba(248, 114, 22, 0.2)',
					borderColor: 'rgba(248, 114, 22, 1)',
					tension: 0.4,
				},
			],
		}

		temperatureChartData.value = {
			labels: newField.data.date || [],
			datasets: [
				{
					label: 'Temp Max',
					data: newField.data.tempmax || [],
					fill: false,
					backgroundColor: 'rgba(76, 175, 80, 0.2)',
					borderColor: 'rgba(76, 175, 80, 1)',
					tension: 0.4,
				},
				{
					label: 'Temp Mean',
					data: newField.data.tempmean || [],
					fill: false,
					backgroundColor: 'rgba(255, 205, 86, 0.2)',
					borderColor: 'rgba(255, 205, 86, 1)',
					tension: 0.4,
				},
				{
					label: 'Temp Min',
					data: newField.data.tempmin || [],
					fill: false,
					backgroundColor: 'rgba(255, 99, 132, 0.2)',
					borderColor: 'rgba(255, 99, 132, 1)',
					tension: 0.4,
				},
			],
		}

		dewPointChartData.value = {
			labels: newField.data.date || [],
			datasets: [
				{
					label: 'Dew Point',
					data: newField.data.dew_point || [],
					fill: false,
					backgroundColor: 'rgba(226, 226, 226, 0.2)',
					borderColor: 'rgba(226, 226, 226, 1)',
					tension: 0.4,
				},
			],
		}

		humidityChartData.value = {
			labels: newField.data.date || [],
			datasets: [
				{
					label: 'Humidity',
					data: newField.data.humidity || [],
					fill: false,
					backgroundColor: 'rgba(168,84,246, 0.2)',
					borderColor: 'rgba(168,84,246, 1)',
					tension: 0.4,
				},
			],
		}

		pressureChartData.value = {
			labels: newField.data.date || [],
			datasets: [
				{
					label: 'Pressure',
					data: newField.data.pressure || [],
					fill: false,
					backgroundColor: 'rgba(255, 99, 132, 0.2)',
					borderColor: 'rgba(255, 99, 132, 1)',
					tension: 0.4,
				},
			],
		}

		uvChartData.value = {
			labels: newField.data.date || [],
			datasets: [
				{
					label: 'UV Index',
					data: newField.data.uvi || [],
					fill: false,
					backgroundColor: 'rgba(255, 205, 86, 0.2)',
					borderColor: 'rgba(255, 205, 86, 1)',
					tension: 0.4,
				},
			],
		}
	} else {
		// Clear chart data if no field is selected
		soilMoistureChartData.value = {}
		soilTemperatureChartData.value = {}
		temperatureChartData.value = {}
		dewPointChartData.value = {}
		humidityChartData.value = {}
		pressureChartData.value = {}
		uvChartData.value = {}
	}
})

definePageMeta({
	middleware: 'auth',
})
</script>
