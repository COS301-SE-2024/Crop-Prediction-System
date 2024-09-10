<template>
	<div class="sm:px-32 sm:py-8 lg:px-52 flex justify-center">
		<Stepper :orientation="isMobile ? 'vertical' : 'horizontal'" linear>
			<!-- Step 1: Field Info -->
			<StepperPanel header="Field Info">
				<template #content="{ nextCallback }">
					<div class="flex flex-col w-full justify-center items-center">
						<div class="flex flex-col gap-2">
							<label for="field_name">Field Name</label>
							<InputText
								id="field_name"
								v-model="newField.field_name"
								class="w-full sm:w-[250px]"
								placeholder="Name"
							/>
							<small id="field_name">Enter your new field name above.</small>
							<Dropdown
								v-model="newField.crop_type"
								:options="cropOptions"
								optionLabel="name"
								optionValue="value"
								placeholder="Select a Crop Type"
								class="w-full sm:w-[250px] mt-4"
							/>
						</div>
					</div>
					<div class="flex pt-4 justify-end">
						<Button
							label="Next"
							size="small"
							icon="pi pi-arrow-right"
							iconPos="right"
							@click="nextCallback"
							:disabled="!newField.crop_type || newField.field_name === ''"
						/>
					</div>
				</template>
			</StepperPanel>

			<!-- Step 2: Field Map -->
			<StepperPanel header="Field Map">
				<template #content="{ prevCallback, nextCallback }">
					<div class="flex-auto flex justify-center items-center">
						<GoogleMap @polygonDrawn="handlePolygonDrawn" @polygonUpdated="handlePolygonUpdated" />
					</div>
					<div class="flex pt-4 justify-between">
						<Button
							label="Back"
							size="small"
							severity="secondary"
							class="mr-2"
							icon="pi pi-arrow-left"
							@click="prevCallback"
						/>
						<Button label="Next" size="small" icon="pi pi-arrow-right" iconPos="right" @click="nextCallback" />
					</div>
				</template>
			</StepperPanel>

			<!-- Step 3: Confirm -->
			<StepperPanel header="Confirm">
				<template #content="{ prevCallback }">
					<div class="flex flex-column h-12rem">
						<div class="flex-auto flex justify-center align-items-center font-medium">
							<div class="flex flex-col gap-2">
								<h2 class="text-2xl"><strong>Field Name:</strong> {{ newField.field_name }}</h2>
								<p><strong>Crop Type:</strong> {{ capitalizeFirstCharacter(newField.crop_type) }}</p>
								<p>
									<strong>Field Map:</strong>
									<Tag
										class="ml-2"
										:severity="severity.valueOf()"
										:value="severity.valueOf() === 'warning' ? 'INCOMPLETE' : 'DRAWN'"
									></Tag>
								</p>
							</div>
						</div>
					</div>
					<div class="flex pt-4 justify-between">
						<Button label="Back" size="small" severity="secondary" icon="pi pi-arrow-left" @click="prevCallback" />
						<Button label="Save Field" size="small" icon="pi pi-check" @click="saveField" :loading="isLoading" />
					</div>
				</template>
			</StepperPanel>
		</Stepper>
		<Toast />
	</div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import GoogleMap from '~/components/GoogleMap.vue'
import { useToast } from 'primevue/usetoast'

// INFO: Define a ref to store the user info (including team_id)
const newField = ref({
	field_name: '',
	crop_type: '',
	field_area: [], // This will hold the polygon coordinates
	team_id: '', // This will be fetched dynamically
})

// INFO: Refs for state
const isMobile = ref(false)
const toast = useToast()

// INFO: Crop options
const cropOptions = ref([
	{ name: 'Maize', value: 'maize' },
	{ name: 'Wheat', value: 'wheat' },
	{ name: 'Groundnuts', value: 'groundnuts' },
	{ name: 'Sunflower', value: 'sunflower' },
	{ name: 'Sorghum', value: 'sorghum' },
	{ name: 'Soybeans', value: 'soybeans' },
	{ name: 'Barley', value: 'barley' },
	{ name: 'Canola', value: 'canola' },
	{ name: 'Oats', value: 'oats' },
])

// Function to check for mobile responsiveness
const checkDeviceWidth = () => {
	isMobile.value = window.innerWidth <= 640
}

// Fetch team_id dynamically based on the user
async function fetchTeamID() {
	const currentUser = useSupabaseUser()
	try {
		if (currentUser.value) {
			// Fetch the team_id from your API using the user ID
			const response = await $fetch('/api/getTeamID', {
				params: { userid: currentUser.value.id },
			})
			newField.value.team_id = response.team_id // Dynamically set team_id
		}
	} catch (error) {
		console.error('Error fetching team ID:', error)
		toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to fetch team ID.' })
	}
}

// Capture the drawn polygon and store its coordinates in field_area
function handlePolygonDrawn(paths) {
	newField.value.field_area = {
		type: 'Polygon', // Polygon type for geojson-like structure
		coordinates: paths, // Wrap paths in an array of coordinates
	}
	severity.value = 'success'
}

// Capture updated polygon coordinates when edited
function handlePolygonUpdated(paths) {
	newField.value.field_area.coordinates = paths // Update the coordinates
}

const severity = ref('warning')
const isLoading = ref(false)
// Save the field (submit to API)
async function saveField() {
	if (!newField.value.field_area.coordinates) {
		toast.add({ severity: 'warn', summary: 'Incomplete Map', detail: 'Please draw the field on the map.', life: 3000 })
		return
	}

	severity.value = 'success'
	console.log(newField.value)
	try {
		isLoading.value = true
		await $fetch('/api/saveField', {
			method: 'POST',
			body: {
				field_name: newField.value.field_name,
				crop_type: newField.value.crop_type,
				team_id: newField.value.team_id,
				field_area: newField.value.field_area,
			},
		})
	} catch (error) {
		toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to save field. Try again later.' })
	} finally {
		isLoading.value = false
		toast.add({ severity: 'success', summary: 'Success', detail: 'Field saved successfully!' })
	}
}

function capitalizeFirstCharacter(str: string) {
	if (!str) return '' // Handle empty strings
	return str.charAt(0).toUpperCase() + str.slice(1)
}

// Fetch team_id on component mount
onMounted(() => {
	checkDeviceWidth()
	window.addEventListener('resize', checkDeviceWidth)
	fetchTeamID() // Fetch team_id on mount
})

onUnmounted(() => {
	window.removeEventListener('resize', checkDeviceWidth)
})
</script>
