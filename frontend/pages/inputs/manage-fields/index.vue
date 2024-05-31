<template>
	<div class="h-screen w-full flex flex-col gap-5">
		<div class="flex flex-row justify-between items-center">
			<span class="font-bold text-xl">Fields</span>
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
		<GoogleMap ref="googleMapRef" :isDrawingEnabled="isDrawingEnabled" @polygonDrawn="handlePolygonDrawn" />
	</div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import GoogleMap from '~/components/GoogleMap.vue'
import { useConfirm } from 'primevue/useconfirm'

const googleMapRef = ref() // Reference to the GoogleMap component
const isDialogVisible = ref(false)
const isDrawingEnabled = ref(false)
const fieldName = ref('')
const selectedCropType = ref(null)
const cropOptions = ref([
	{ name: 'Corn', value: 'corn' },
	{ name: 'Soybeans', value: 'soybeans' },
	{ name: 'Wheat', value: 'wheat' },
])
const fieldsData = ref([])
const confirm = useConfirm()

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

const handlePolygonDrawn = () => {
	isDrawingEnabled.value = false
	googleMapRef.value.setDrawingMode(false)
	showConfirmationDialog(polygonPaths)
}

const showConfirmationDialog = () => {
	confirm.require({
		message: 'Are you sure you want to save this field?',
		header: 'Confirmation',
		icon: 'pi pi-exclamation-triangle',
		accept: () => {
			saveField(polygonPaths)
		},
		reject: () => {
			cancelAddField() // Clear the polygon and reset the dialog
		},
	})
}

const saveField = () => {
	const paths = googleMapRef.value.getPolygonPaths()
	if (paths.length > 0) {
		fieldsData.value.push({
			name: fieldName.value,
			cropType: selectedCropType.value,
			paths,
		})
		// Reset for the next field
		fieldName.value = ''
		selectedCropType.value = null
	}
}
</script>
