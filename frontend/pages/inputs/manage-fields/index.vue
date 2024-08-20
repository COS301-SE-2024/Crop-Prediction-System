<template>
	<div class="h-full w-full flex flex-col gap-5">
		<div class="flex flex-row justify-between items-center _mb-4">
			<span class="font-bold text-xl dark:text-white">Fields</span>
			<Button label="Add Field" @click="isDialogVisible = true" />
		</div>

		<Dialog v-model:visible="isDialogVisible" header="Add Field" :modal="true" :style="{ width: '450px' }">
			<div class="flex flex-col space-y-2 mb-4">
				<InputText v-model="fieldName" placeholder="Field Name" />
				<Dropdown v-model="selectedCropType" :options="cropOptions" optionLabel="name" placeholder="Crop Type" />
			</div>
			<template #footer>
				<Button label="Cancel" severity="danger" icon="pi pi-times" @click="cancelAddField" />
				<Button label="Save" icon="pi pi-check" @click="proceedToDrawing" />
			</template>
		</Dialog>

		<ConfirmDialog />
		<div class="p-3 border border-surface-300 rounded-md dark:border-surface-600">
			<GoogleMap ref="googleMapRef" :isDrawingEnabled="isDrawingEnabled" @polygonDrawn="handlePolygonDrawn" />
		</div>
	</div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import GoogleMap from '~/components/GoogleMap.vue'
import { useConfirm } from 'primevue/useconfirm'
import FieldTable from '~/components/FieldTable.vue'

// get userID
const currentUser = useSupabaseUser()

definePageMeta({
	middleware: 'auth',
})

const googleMapRef = ref() // Reference to the GoogleMap component
const isDialogVisible = ref(false)
const isDrawingEnabled = ref(false)
const fieldName = ref('')
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

const teamID = await $fetch('/api/getTeamID', {
	params: { userid: currentUser?.value?.id },
})

console.log(teamID.team_id)

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

const userFields = await $fetch('/api/getTeamFields', {
	params: { team_id: teamID.team_id },
})
</script>
