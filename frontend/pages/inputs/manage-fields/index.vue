<template>
	<div class="h-screen w-full flex flex-col gap-5">
		<div class="flex flex-row justify-between items-center">
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
		<GoogleMap ref="googleMapRef" :isDrawingEnabled="isDrawingEnabled" @polygonDrawn="handlePolygonDrawn" />
	</div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import GoogleMap from '~/components/GoogleMap.vue'
import { useConfirm } from 'primevue/useconfirm'

// get userID
const session = useSupabaseClient()
let currentUser = null
if (session) {
	const {
		data: { user },
	} = await session.auth.getUser()
	if (user) currentUser = user
	console.log('user: ', user.id)
}

definePageMeta({
	middleware: 'auth',
})

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
const drawnPolygonPaths = ref([])

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
			paths: drawnPolygonPaths.value,
		})
		console.log('Field saved:', {
			name: fieldName.value,
			cropType: selectedCropType.value,
			paths: drawnPolygonPaths.value.toLocaleString(),
		})
		// class Field(BaseModel):
		// field_id: Optional[int] = None
		// field_area: Optional[object] = None
		// field_name: Optional[str] = None
		// field_tph: Optional[float] = None
		// field_health: Optional[float] = None
		// crop_type: Optional[str] = None
		// user_id: Optional[str] = None
		//  create an array called dataArray of objects to be sent to the backend
		const FieldsDataPaths: number[][] = []
		// convert fieldsData from string to float. '(23.00000,22.123)' to [23.00000, 22.123]
		fieldsData.value.forEach((field: { name: string; cropType: { name: string }; paths: [] }) => {
			const fieldPaths: number[] = []
			field.paths.forEach((path: string) => {
				const pathString = path.toString().replace('(', '').replace(')', '').split(',')
				const pathFloat: number[] = pathString.map((path: string) => parseFloat(path))
				fieldPaths.push(...pathFloat)
			})
			FieldsDataPaths.push(fieldPaths)
		})
		//  ! fix type to give the correct type
		if (currentUser) {
			// convert to string
			currentUser.id = currentUser.id.toString()
		}
		const returnData = {
			field_name: fieldName.value,
			crop_type: selectedCropType.value.name,
			field_area: {
				type: 'Polygon',
				coordinates: FieldsDataPaths,
			},
			user_id: currentUser ? currentUser.id : 'null',
		}
		console.log('returnData:', returnData)

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
</script>
