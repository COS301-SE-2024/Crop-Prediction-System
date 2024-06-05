<template>
	<div class="flex flex-col h-full">
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
					<Button label="Save" class="w-full" />
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

// Fetch fields from backend here
const selectedField = ref()
const fields = ref([
	{ name: 'Wheat Field' },
	{ name: 'Corn Field' },
	{ name: 'Soya Field' },
	{ name: 'Underberg' },
	{ name: 'Down Under' },
])

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
