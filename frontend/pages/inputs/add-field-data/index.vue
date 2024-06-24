<template>
	<div class="flex flex-col h-full px-4 sm:px-6 md:px-8 lg:px-0 py-4 sm:py-6 md:py-8 lg:py-0">
		<Card class="border border-surface-border p-fluid h-full">
			<template #title>
				<h1>Manual Field Inputs</h1>
			</template>
			<template #content>
				<div class="flex flex-col items-center gap-5">
					<div class="flex items-center gap-5 p-5">
						<h2 class="font-medium text-md">Add Field Data</h2>
						<Dropdown
							v-model="selectedField"
							editable
							:options="fields"
							optionLabel="name"
							placeholder="Select a Field"
							class="w-full md:w-[14rem]"
						/>
					</div>
					<div class="flex flex-wrap gap-3 p-fluid">
						<div class="flex-auto">
							<label for="temperature" class="font-medium block mb-2">Temperature</label>
							<InputNumber
								v-model="weather_temperature"
								inputId="temperature"
								:min-fraction-digits="1"
								:max-fraction-digits="2"
								suffix="°C"
							/>
						</div>
						<div class="flex-auto">
							<label for="humidity" class="font-medium block mb-2">Humidity</label>
							<InputNumber
								v-model="weather_humidity"
								inputId="humidity"
								:min-fraction-digits="1"
								:max-fraction-digits="2"
							/>
						</div>
						<div class="flex-auto">
							<label for="rainfall" class="font-medium block mb-2">Rainfall</label>
							<InputNumber
								v-model="weather_rainfall"
								inputId="rainfall"
								:min-fraction-digits="1"
								:max-fraction-digits="2"
								suffix="mm"
							/>
						</div>
						<div class="flex-auto">
							<label for="uv" class="font-medium block mb-2">UV Index</label>
							<InputNumber v-model="weather_uv" inputId="uv" :min-fraction-digits="1" :max-fraction-digits="2" />
						</div>
						<div class="flex-auto">
							<label for="soilMoisture" class="font-medium block mb-2">Soil Moisture</label>
							<InputNumber
								v-model="soil_moisture"
								inputId="soilMoisture"
								:min-fraction-digits="1"
								:max-fraction-digits="2"
							/>
						</div>
						<div class="flex-auto">
							<label for="soilPh" class="font-medium block mb-2">Soil PH</label>
							<InputNumber v-model="soil_ph" inputId="soilPh" :min-fraction-digits="1" :max-fraction-digits="2" />
						</div>
						<div class="flex-auto">
							<label for="soilConductivity" class="font-medium block mb-2">Soil Conductivity</label>
							<InputNumber
								v-model="soil_conductivity"
								inputId="soilConductivity"
								:min-fraction-digits="1"
								:max-fraction-digits="2"
							/>
						</div>
					</div>
				</div>
			</template>
			<template #footer>
				<div class="flex gap-3">
					<Button label="Cancel" severity="secondary" outlined class="w-full" />
					<Button label="Save" class="w-full" @click="saveFieldData" />
				</div>
			</template>
		</Card>
	</div>
</template>

<script setup lang="ts">
import Card from 'primevue/card'
import Dropdown from 'primevue/dropdown'
import InputNumber from 'primevue/inputnumber'
import { ref, onMounted } from 'vue'

const user = useSupabaseUser()
const userID = user.value?.id

const selectedField = ref()
const weather_temperature = ref(0)
const weather_humidity = ref(0)
const weather_rainfall = ref(0)
const weather_uv = ref(0)
const soil_moisture = ref(0)
const soil_ph = ref(0)
const soil_conductivity = ref(0)

const fields = ref([])

const loadUserFields = async () => {
	try {
		const userFields = await $fetch('/api/getUserFields', {
			params: { userid: userID },
		})

		console.log('User Fields', userFields)
		// Map field_name in userFields to name for dropdown
		const newFields = [
			{
				name: 'Field 1',
				health: 0.5,
				yield: 0,
				cropType: 'Mize',
			},
			{
				name: 'Field 2',
				health: 0.7,
				yield: 0,
				cropType: 'Wheat',
			},
			{
				name: 'Field 3',
				health: 0.3,
				yield: 0,
				cropType: 'Barley',
			},
		]

		if (!userFields.length) {
			for (let i = 0; i < newFields.length; i++) {
				fields.value.push(newFields[i])
			}
		} else {
			fields.value = userFields.map((field: { field_name: string; id: number }) => {
				return { name: field.field_name, id: field.id }
			})
		}
	} catch (error) {
		console.error('Error loading user fields:', error)
	}
}

onMounted(() => {
	// Add a delay before loading user fields
	setTimeout(() => {
		loadUserFields()
	}, 2000) // 2-second delay
})

async function saveFieldData() {
	console.log('Save Field Data called')

	let field_id = null
	for (let index = 0; index < fields.value.length; index++) {
		if (selectedField.value.name === fields.value[index].name) {
			field_id = fields.value[index].id
			break
		}
	}

	const data = {
		field_id,
		weather_temperature: weather_temperature.value,
		weather_humidity: weather_humidity.value,
		weather_rainfall: weather_rainfall.value,
		weather_uv: weather_uv.value,
		soil_moisture: soil_moisture.value,
		soil_ph: soil_ph.value,
		soil_conductivity: soil_conductivity.value,
		is_manual: true,
	}

	console.log('Data to be sent:', data)

	try {
		const response = await fetch('/api/createEntry', {
			method: 'POST',
			body: JSON.stringify(data),
			headers: {
				'Content-Type': 'application/json',
			},
		})

		console.log('Response:', response)
		if (!response.ok) {
			const errorData = await response.json()
			console.error('Error response:', errorData)
		} else {
			const responseData = await response.json()
			console.log('Success response:', responseData)
		}
	} catch (error) {
		console.error('Error:', error)
	}
}

definePageMeta({
	middleware: 'auth',
})
</script>

<style>
.card {
	max-width: 800px;
	margin: 0 auto;
}
</style>
