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
							<label for="minmaxfraction" class="font-medium block mb-2"> Temperature </label>
							<InputNumber
								v-model="weather_temperature"
								inputId="minmaxfraction"
								:min-fraction-digits="1"
								:max-fraction-digits="2"
								suffix="°C"
							/>
						</div>

						<div class="flex-auto">
							<label for="minmaxfraction" class="font-medium block mb-2"> Humidity </label>
							<InputNumber
								v-model="weather_humidity"
								inputId="minmaxfraction"
								:min-fraction-digits="1"
								:max-fraction-digits="2"
							/>
						</div>

						<div class="flex-auto">
							<label for="minmaxfraction" class="font-medium block mb-2"> Rainfall </label>
							<InputNumber
								v-model="weather_rainfall"
								inputId="minmaxfraction"
								:min-fraction-digits="1"
								:max-fraction-digits="2"
								suffix="mm"
							/>
						</div>

						<div class="flex-auto">
							<label for="minmaxfraction" class="font-medium block mb-2"> UV Index </label>
							<InputNumber
								v-model="weather_uv"
								inputId="minmaxfraction"
								:min-fraction-digits="1"
								:max-fraction-digits="2"
							/>
						</div>

						<div class="flex-auto">
							<label for="minmaxfraction" class="font-medium block mb-2"> Soil Moisture </label>
							<InputNumber
								v-model="soil_moisture"
								inputId="minmaxfraction"
								:min-fraction-digits="1"
								:max-fraction-digits="2"
							/>
						</div>

						<div class="flex-auto">
							<label for="minmaxfraction" class="font-medium block mb-2"> Soil PH </label>
							<InputNumber
								v-model="soil_ph"
								inputId="minmaxfraction"
								:min-fraction-digits="1"
								:max-fraction-digits="2"
							/>
						</div>

						<div class="flex-auto">
							<label for="minmaxfraction" class="font-medium block mb-2"> Soil Conductivity </label>
							<InputNumber
								v-model="soil_conductivity"
								inputId="minmaxfraction"
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
import { ref } from 'vue'

const user = useSupabaseUser()
const userID = user.value?.id

// Fetch fields from backend here
const selectedField = ref()
const userFields = await $fetch('/api/getUserFields', {
	params: { userid: userID },
})

console.log('User Fields', userFields)
// Map field_name in userFields to name for dropdown
const fields = ref([])
if (userFields) {
	fields.value = userFields.map((field: { field_name: any }) => {
		return { name: field.field_name }
	})
} else {
	fields.value.push({ name: 'No Fields Found' })
}

async function saveFieldData() {
	const field_id = ref()
	// for (let index = 0; index < userFields.length; index++) {
	// 	if (selectedField.value.name === userFields[index].field_name) {
	// 		field_id.value = userFields[index].id
	// 	}
	// }
	const data = {
		field_id: field_id.value,
		weather_temperature: weather_temperature.value,
		weather_humidity: weather_humidity.value,
		weather_rainfall: weather_rainfall.value,
		weather_uv: weather_uv.value,
		soil_moisture: soil_moisture.value,
		soil_ph: soil_ph.value,
		soil_conductivity: soil_conductivity.value,
		is_manual: true,
	}

	// try {
	// 	const response = await $fetch('/api/createEntry', {
	// 		method: 'POST',
	// 		body: data,
	// 	})
	// 	console.log('Response:', response)
	// } catch (error) {
	// 	console.error('Error:', error)
	// }
}

const weather_temperature = ref(0)
const weather_humidity = ref(0)
const weather_rainfall = ref(0)
const weather_uv = ref(0)
const soil_moisture = ref(0)
const soil_ph = ref(0)
const soil_conductivity = ref(0)

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
