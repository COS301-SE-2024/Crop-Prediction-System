<template>
	<div class="h-full w-full flex flex-col items-center justify-center gap-5">
		<div v-show="!isLoading" class="flex flex-col sm:flex-row justify-start items-center gap-4 mt-4 w-full">
			<InputText v-model="searchQuery" placeholder="Search Field Name..." class="w-full sm:w-[375px]" />
			<Dropdown
				v-model="selectedCropType"
				:options="cropOptions"
				optionLabel="name"
				placeholder="Filter by Crop Type"
				class="w-full sm:w-[250px]"
				showClear
			/>
		</div>

		<div v-if="isLoading" class="w-full h-full mt-48 gap-5 flex flex-col items-center justify-center">
			<ProgressSpinner />
			<h2 class="dark:text-white font-bold">Fetching Fields...</h2>
		</div>

		<div v-else class="grid lg:grid-cols-3 xl:grid-cols-4 sm:grid-cols-2 grid-cols-1 gap-4 w-full">
			<Card v-for="field in filteredFields" :key="field.id">
				<template #header>
					<div class="text-center p-2">
						<h2 class="text-2xl font-bold">{{ field.field_name }}</h2>
					</div>
				</template>
				<template #content>
					<div class="text-gray-600 dark:text-gray-300 flex flex-col justify-between items-start gap-2">
						<span> <strong>Crop Type: </strong>{{ capitalizeFirstCharacter(field.crop_type) }}</span>
						<span><strong>Field Size: </strong>{{ field.hectare.toFixed(2) }}ha</span>
						<span><strong>Field ID: </strong>{{ field.id }}</span>
					</div>
				</template>
				<template #footer>
					<div class="flex gap-3">
						<Button label="Delete" severity="danger" size="small" outlined class="w-full" />
						<Button label="View or Edit" size="small" class="w-full" @click="editField(field)" />
					</div>
				</template>
			</Card>
		</div>

		<Dialog
			maximizable
			modal
			header="View/Edit Field"
			v-model:visible="editAndViewVisible"
			class="w-[95%] md:w-[740px] lg:w-[950px]"
		>
			<div class="flex flex-col justify-between items-start gap-4">
				<div class="flex flex-col gap-2 w-full">
					<label for="fieldname">Field Name</label>
					<InputText id="fieldname" class="w-full sm:w-[250px]" :placeholder="selectedField?.field_name" />
				</div>

				<div class="flex flex-col gap-2 w-full">
					<label for="croptype">Crop Type</label>
					<Dropdown
						class="w-full sm:w-[250px]"
						v-model="selectedCropType"
						:options="cropOptions"
						optionLabel="name"
						:placeholder="capitalizeFirstCharacter(selectedField?.crop_type as string)"
						showClear
					/>
				</div>

				<div class="flex flex-col gap-2 w-full">
					<div class="w-full h-[400px] rounded overflow-hidden">
						<GoogleMapsField
							:selectedField="selectedField"
							:fields="teamFields"
							@update:selectedField="updateSelectedField"
						/>
					</div>
				</div>
			</div>
		</Dialog>

		<Toast />
	</div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useConfirm } from 'primevue/useconfirm'
import Card from 'primevue/card'
import GoogleMapsField from '~/components/GoogleMapsField.vue'
import InputText from 'primevue/inputtext'

// TODO: Maybe add toasts to notify users that they have updated or deleted a field
// TODO: Move Add Field to a new page (with a search bar for places API)
// TODO: Add controls to edit field on map
// TODO: Implement Edit Field put request functionality
// TODO: Add drawing controls to GoogleMapsField on edit field

// PERF: Get team_id and load fields
const isLoading = ref(true)
const currentUser = useSupabaseUser()

const teamFields = ref([])

onMounted(async () => {
	try {
		isLoading.value = true
		const teamID = await $fetch('/api/getTeamID', {
			params: { userid: currentUser?.value?.id },
		})

		teamFields.value = await $fetch('/api/getTeamFields', {
			params: { team_id: teamID.team_id },
		})
	} catch (error) {
		console.error('Error fetching user fields:', error)
	} finally {
		isLoading.value = false
	}
})

// PERF: Dialog on Field info

const editAndViewVisible = ref(false)
const selectedField = ref(null)

const editField = (field: any) => {
	selectedField.value = field
	editAndViewVisible.value = true
}

function updateSelectedField(newField) {
	selectedField.value = newField
}

// PERF: Search by Field Name and filter by Crop Type functionality
const filteredFields = ref([])
const searchQuery = ref('')
const selectedCropType = ref(null)
const cropOptions = ref([
	{ name: 'Maize', value: 'maize' },
	{ name: 'Wheat', value: 'wheat' },
	{ name: 'Groundnuts', value: 'groundnuts' },
	{ name: 'Sunflower', value: 'sunflowerseed' },
	{ name: 'Sorghum', value: 'sorghum' },
	{ name: 'Soybeans', value: 'soybeans' },
	{ name: 'Barley', value: 'barley' },
	{ name: 'Canola', value: 'canola' },
	{ name: 'Oats', value: 'oats' },
])

watchEffect(() => {
	filteredFields.value = teamFields.value.filter((field) => {
		const matchesSearchQuery = field.field_name.toLowerCase().includes(searchQuery.value.toLowerCase())
		const matchesCropType = selectedCropType.value
			? field.crop_type.toLowerCase() === selectedCropType.value.value.toLowerCase()
			: true
		return matchesSearchQuery && matchesCropType
	})
})

const googleMapRef = ref() // Reference to the GoogleMap component
const isDialogVisible = ref(false)
const isDrawingEnabled = ref(false)
const fieldName = ref('')

const fieldsData = ref([])
const confirm = useConfirm()
const drawnPolygonPaths = ref<google.maps.LatLng[]>([])

const proceedToDrawing = () => {
	isDialogVisible.value = false
	isDrawingEnabled.value = true // Enable drawing mode after saving details
	googleMapRef.value.setDrawingMode(true)
}

const cancelAddField = () => {
	isDialogVisible.value = false
	isDrawingEnabled.value = false
	googleMapRef.value.clearPolygon()
}

const handlePolygonDrawn = (paths: google.maps.LatLng[]) => {
	drawnPolygonPaths.value = paths
	isDrawingEnabled.value = false
	googleMapRef.value.setDrawingMode(false)
	showConfirmationDialog()
}

const showConfirmationDialog = () => {
	confirm.require({
		message: 'Are you sure you want to save this field?',
		header: 'Confirmation',
		icon: 'pi pi-exclamation-triangle',
		accept: () => {
			saveField()
		},
		reject: () => {
			cancelAddField() // Clear the polygon and reset the dialog
		},
	})
}

const saveField = async () => {
	if (drawnPolygonPaths.value.length > 0) {
		fieldsData.value.push({
			name: fieldName.value,
			cropType: selectedCropType.value,
			paths: drawnPolygonPaths.value.map((latLng) => [latLng.lat(), latLng.lng()]), // convert paths to array of arrays
		})

		const FieldsDataPaths: number[] = []
		fieldsData.value.forEach((field: { name: string; cropType: { name: string }; paths: number[][] }) => {
			field.paths.forEach((path: number[]) => {
				FieldsDataPaths.push(...path)
			})
		})

		// convert FieldsDataPaths to array of arrays
		const coordinatesArray: number[][] = []
		for (let index = 1; index < FieldsDataPaths.length; index += 2) {
			const newPoint: number[] = [FieldsDataPaths[index - 1], FieldsDataPaths[index]]
			console.log(`Adding new point: [${FieldsDataPaths[index - 1]}, ${FieldsDataPaths[index]}]`)
			coordinatesArray.push(newPoint)
		}

		const returnData = {
			field_name: fieldName.value,
			crop_type: selectedCropType.value.name.toLowerCase(),
			field_area: {
				type: 'Polygon',
				coordinates: coordinatesArray,
			},
			team_id: teamID.team_id,
		}

		console.log('Return Data:', returnData)
		try {
			const response = await $fetch('/api/createField', {
				method: 'POST',
				body: returnData,
			})
		} catch (error) {
			console.error('Error:', error)
		}

		// Reset for the next field
		fieldName.value = ''
		selectedCropType.value = null
	}
}

function capitalizeFirstCharacter(str: string) {
	if (!str) return '' // Handle empty strings
	return str.charAt(0).toUpperCase() + str.slice(1)
}

// PERF: Page Meta
definePageMeta({
	middleware: 'auth',
})
</script>
