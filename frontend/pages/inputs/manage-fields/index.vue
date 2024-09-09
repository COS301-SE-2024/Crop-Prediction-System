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
			<Button
				label="Train All"
				icon="pi pi-microchip-ai"
				class="sm:w-auto w-full"
				severity="secondary"
				:loading="trainAllLoading"
				:disabled="!checkTeamFields"
				@click="trainAllFields"
				outlined
			/>
		</div>

		<div v-if="isLoading" class="w-full h-full mt-48 gap-5 flex flex-col items-center justify-center">
			<ProgressSpinner />
			<h2 class="dark:text-white font-bold">Fetching Fields...</h2>
		</div>

		<div v-else class="grid lg:grid-cols-3 xl:grid-cols-4 sm:grid-cols-2 grid-cols-1 gap-4 w-full">
			<h2 class="dark:text-white font-bold text-xl col-span-12" v-if="!checkTeamFields">
				Go to the add fields to start adding fields.
			</h2>
			<Card v-else v-for="field in filteredFields" :key="field.id">
				<template #title>
					<div class="flex flex-row justify-between items-center">
						<h2 class="text-2xl font-bold">{{ field.field_name }}</h2>
						<Button
							:key="field.id"
							:id="field.id"
							size="small"
							severity="secondary"
							icon="pi pi-microchip-ai"
							label="Train"
							outlined
							:loading="loadingStates.get(field.id) || false"
							@click="trainField(field)"
						/>
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
						<Button
							label="Delete"
							severity="danger"
							size="small"
							outlined
							class="w-full"
							@click="openDeleteDialog(field)"
						/>
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
					<div class="flex items-center gap-2">
						<InputText
							id="fieldname"
							v-model="newFieldName"
							class="w-full sm:w-[250px]"
							:placeholder="selectedField?.field_name"
							:disabled="!isEditingFieldName"
						/>
						<Button
							size="small"
							text
							severity="secondary"
							:icon="isEditingFieldName ? 'pi pi-check' : 'pi pi-pencil'"
							@click="toggleNameEditMode"
						/>
					</div>
				</div>

				<div class="flex flex-col gap-2 w-full">
					<label for="croptype">Crop Type</label>
					<div class="flex gap-2">
						<Dropdown
							class="w-full sm:w-[250px]"
							v-model="editingSelectedCropType"
							:options="editingCropOptions"
							optionLabel="name"
							:placeholder="capitalizeFirstCharacter(selectedField?.crop_type as string)"
							:disabled="!isEditingCropType"
						/>
						<Button
							text
							:icon="isEditingCropType ? 'pi pi-check' : 'pi pi-pencil'"
							severity="secondary"
							size="small"
							@click="toggleCropEditMode"
						/>
					</div>
				</div>

				<div class="w-full flex flex-row justify-between items-center">
					<h4 class="text-lg font-bold">Field Map</h4>
					<Button
						:severity="isFieldEditMode ? 'info' : 'secondary'"
						:label="isFieldEditMode ? 'Save Changes' : 'Edit Map'"
						:icon="isFieldEditMode ? 'pi pi-check' : 'pi pi-pencil'"
						size="small"
						outlined
						@click="toggleFieldEditMode"
					/>
				</div>

				<p class="mt-2" v-show="isFieldEditMode">
					Adjust the size or shape of the field by pressing and dragging the dots on the corners of the field polygon.
					If you wish to move the polygon, simply press and hold in the middle of the polygon and drag it.
				</p>
				<div class="flex flex-col gap-2 w-full">
					<div class="w-full h-[400px] md:h-[600px] rounded overflow-hidden">
						<GoogleMapsField
							:selectedField="selectedField"
							:fields="teamFields"
							:isEditMode="isFieldEditMode"
							@update:selectedField="updateSelectedField"
							@savePolygonCoords="handlePolygonUpdate"
						/>
					</div>
				</div>
			</div>
		</Dialog>

		<!-- Delete field dialog -->
		<Dialog header="Confirm Delete" v-model:visible="deleteDialogVisible" modal :style="{ width: '25rem' }">
			<p>
				Are you sure you want to delete the field "<strong>{{ fieldToDelete?.field_name }}</strong
				>"?
			</p>
			<div class="flex justify-end gap-2 mt-4">
				<Button label="Cancel" outlined severity="secondary" @click="cancelDelete" />
				<Button label="Delete" severity="danger" @click="deleteField" />
			</div>
		</Dialog>

		<Toast />
	</div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Card from 'primevue/card'
import GoogleMapsField from '~/components/GoogleMapsField.vue'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'
import { useToast } from 'primevue/usetoast'

// TODO: Implement Edit Field Functionality (with dialog to confirm)
// TODO: Implement Delete Field Functionality (with dialog to confirm)
// HACK: Maybe add toasts to notify users that they have updated or deleted a field
// TODO: Move Add Field to a new page (with a search bar for places API)
// TODO: Add controls to edit field on map
// TODO: Implement Edit Field put request functionality
// TODO: Add drawing controls to GoogleMapsField on edit field
// TODO: Add functionality to 'Train' button on Cards to train fields
// TODO: Add functionality to retrain all fields

// PERF: Page Meta
definePageMeta({
	middleware: 'auth',
})

// INFO: toast initialize for messages
const toast = useToast()

// PERF: Get team_id and load fields
const isLoading = ref(true)
const currentUser = useSupabaseUser()

const teamFields = ref([])
const checkTeamFields = ref(true)

onMounted(async () => {
	try {
		isLoading.value = true
		const teamID = await $fetch('/api/getTeamID', {
			params: { userid: currentUser?.value?.id },
		})

		console.log(teamID)

		const response = await $fetch('/api/getTeamFields', {
			params: { team_id: teamID.team_id },
		})

		// Check if the response contains an error
		if (response.error) {
			toast.add({
				severity: 'info',
				summary: 'No Fields Found',
				detail: 'No fields are associated with this team.',
				life: 3000,
			})
			teamFields.value = [] // Set teamFields to an empty array
			checkTeamFields.value = false
		} else {
			teamFields.value = response
		}
	} catch (error) {
		console.error('Error fetching user fields:', error)
		toast.add({
			severity: 'error',
			summary: 'Error',
			detail: 'An error occurred while fetching fields.',
			life: 3000,
		})
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
	{ name: 'Sunflower', value: 'sunflower' },
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

// PERF: Training of individual fields
const loadingStates = ref(new Map())

const showIndividualTrainSuccess = (field) => {
	toast.add({
		severity: 'info',
		summary: 'Training scheduled',
		detail: `The following field has been scheduled for training: ${field.field_name}`,
		life: 3000,
	})
}

const showIndividualTrainFailure = (field) => {
	toast.add({
		severity: 'error',
		summary: 'Training field failed',
		detail: `The following field could not be trained: ${field.field_name}`,
		life: 3000,
	})
}

async function trainField(field, from: string) {
	loadingStates.value.set(field.id, true)
	try {
		await $fetch('/api/trainField', {
			params: { field_id: field.id },
		})
	} catch (error) {
		showIndividualTrainFailure(field)
	} finally {
		loadingStates.value.set(field.id, false)
		if (from !== 'trainAll') {
			showIndividualTrainSuccess(field)
		}
	}
}

// PERF: Training of all fields
const trainAllLoading = ref(false)

const showAllTrainSuccess = () => {
	toast.add({
		severity: 'success',
		summary: 'Training scheduled',
		detail: 'All fields have been scheduled for training.',
		life: 3000,
	})
}

const showAllTrainFailure = () => {
	toast.add({
		severity: 'error',
		summary: 'Training fields failed',
		detail: `There was en error training all fields.`,
		life: 3000,
	})
}

const trainAllFields = async () => {
	trainAllLoading.value = true

	teamFields.value.forEach((field) => {
		loadingStates.value.set(field.id, true)
	})

	try {
		for (const field of teamFields.value) {
			await trainField(field, 'trainAll')
		}
	} catch (error) {
		showAllTrainFailure()
	} finally {
		teamFields.value.forEach((field) => {
			loadingStates.value.set(field.id, false)
		})
		trainAllLoading.value = false
		showAllTrainSuccess()
	}
}

function capitalizeFirstCharacter(str: string) {
	if (!str) return '' // Handle empty strings
	return str.charAt(0).toUpperCase() + str.slice(1)
}

// PERF: Editing Field Map
const isFieldEditMode = ref(false) // Tracks if the map is in edit mode

const toggleFieldEditMode = () => {
	// Toggle edit mode
	isFieldEditMode.value = !isFieldEditMode.value
}

async function handlePolygonUpdate(newCoords) {
	const transformedCoords = newCoords.map((coord) => [coord.lat, coord.lng])
	try {
		const response = await $fetch('/api/updateFieldArea', {
			method: 'PUT',
			body: {
				field_id: selectedField.value.id, // The ID of the selected field
				field_area: transformedCoords, // The new polygon coordinates
			},
		})

		if (response.statusCode === 200) {
			toast.add({
				severity: 'success',
				summary: 'Field Map Updated',
				detail: 'The field area has been updated successfully.',
				life: 3000,
			})

			const fieldToUpdate = teamFields.value.find((field) => field.id === selectedField.value.id)
			if (fieldToUpdate) {
				fieldToUpdate.field_area = transformedCoords
			}
		} else {
			toast.add({
				severity: 'error',
				summary: 'Update Failed',
				detail: response.message || 'Failed to update the field area.',
				life: 3000,
			})
		}
	} catch (error) {
		toast.add({
			severity: 'error',
			summary: 'Error',
			detail: 'Failed to update the field area. Please try again.',
			life: 3000,
		})
		console.error('API error:', error)
	}
}

// TODO: Editing Field Crop Type
const isEditingCropType = ref(false)

const editingSelectedCropType = ref(null)
const editingCropOptions = ref([
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

const toggleCropEditMode = async () => {
	if (isEditingCropType.value) {
		try {
			const response = await $fetch('/api/updateFieldCropType', {
				method: 'PUT',
				body: {
					field_id: selectedField.value.id, // The ID of the selected field
					crop_type: editingSelectedCropType.value.value, // The updated crop type
				},
			})

			if (response.statusCode === 200) {
				toast.add({
					severity: 'success',
					summary: 'Crop Type Updated',
					detail: 'The crop type has been updated successfully.',
					life: 3000,
				})

				const fieldToUpdate = teamFields.value.find((field) => field.id === selectedField.value.id)
				if (fieldToUpdate) {
					fieldToUpdate.crop_type = editingSelectedCropType.value.value // Update the local crop type
				}
			} else {
				toast.add({
					severity: 'error',
					summary: 'Update Failed',
					detail: response.message || 'Failed to update crop type.',
					life: 3000,
				})
			}
		} catch (error) {
			toast.add({
				severity: 'error',
				summary: 'Error',
				detail: 'Failed to update the crop type. Please try again.',
				life: 3000,
			})
			console.error('API error:', error)
		}
	}

	isEditingCropType.value = !isEditingCropType.value
}

// PERF: Editing Field name
const isEditingFieldName = ref(false)
const newFieldName = ref('')

const toggleNameEditMode = async () => {
	if (isEditingFieldName.value) {
		try {
			const response = await $fetch('/api/updateFieldName', {
				method: 'PUT',
				body: {
					field_id: selectedField.value.id, // Field ID from selected field
					field_name: newFieldName.value, // New field name
				},
			})

			if (response.statusCode === 200) {
				const fieldToUpdate = teamFields.value.find((field) => field.id === selectedField.value.id)
				if (fieldToUpdate) {
					fieldToUpdate.field_name = newFieldName.value // Update the local field name
				}

				toast.add({
					severity: 'success',
					summary: 'Success',
					detail: 'Field name updated successfully.',
					life: 3000,
				})
			} else {
				toast.add({
					severity: 'error',
					summary: 'Error',
					detail: response.message || 'Failed to update field name.',
					life: 3000,
				})
			}
		} catch (error) {
			toast.add({
				severity: 'error',
				summary: 'Error',
				detail: 'Failed to update field name. Please try again.',
				life: 3000,
			})
			console.error('API error:', error)
		}
	}

	// Toggle the edit mode after the update
	isEditingFieldName.value = !isEditingFieldName.value
}

// PERF: Deleting a field
const deleteDialogVisible = ref(false)
const fieldToDelete = ref(null)

const openDeleteDialog = (field) => {
	fieldToDelete.value = field
	deleteDialogVisible.value = true
}

const deleteField = async () => {
	try {
		const response = await $fetch('/api/deleteField', {
			method: 'POST',
			body: { field_id: fieldToDelete.value.id }, // Send the field ID to delete
		})

		if (response.statusCode === 200) {
			// Remove the deleted field from the local teamFields array
			teamFields.value = teamFields.value.filter((field) => field.id !== fieldToDelete.value.id)

			toast.add({
				severity: 'info',
				summary: 'Field Deleted',
				detail: `Field "${fieldToDelete.value.field_name}" has been deleted successfully.`,
				life: 3000,
			})
		} else {
			toast.add({
				severity: 'error',
				summary: 'Delete Failed',
				detail: response.message || 'Failed to delete the field.',
				life: 3000,
			})
		}
	} catch (error) {
		toast.add({
			severity: 'error',
			summary: 'Error',
			detail: 'Failed to delete the field. Please try again.',
			life: 3000,
		})
		console.error('API error:', error)
	}

	// Close the delete dialog
	deleteDialogVisible.value = false
	fieldToDelete.value = null
}

const cancelDelete = () => {
	deleteDialogVisible.value = false
	fieldToDelete.value = null
}
</script>
