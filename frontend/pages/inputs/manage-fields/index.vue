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
					<div class="w-full h-[400px] md:h-[600px] rounded overflow-hidden">
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

// PERF: Training of individual fields
const loadingStates = ref(new Map())

const showIndividualTrainSuccess = (field) => {
	toast.add({
		severity: 'success',
		summary: 'Trained field',
		detail: `You have successfully trained the field: ${field.field_name}`,
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

async function trainField(field) {
	loadingStates.value.set(field.id, true)
	try {
		await $fetch('/api/trainField', {
			params: { field_id: field.id },
		})
	} catch (error) {
		showIndividualTrainFailure(field)
	} finally {
		loadingStates.value.set(field.id, false)
		showIndividualTrainSuccess(field)
	}
}

// PERF: Training of all fields
const trainAllLoading = ref(false)

const showAllTrainSuccess = () => {
	toast.add({
		severity: 'info',
		summary: 'Trained all fields',
		detail: 'You have successfully trained all fields.',
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
			await trainField(field)
		}
	} catch (error) {
		showAllTrainFailure()
	} finally {
		teamFields.value.forEach((field) => {
			loadingStates.value.set(field.id, false)
		})
		trainAllLoading.value = false
		setTimeout(() => {
			showAllTrainSuccess()
		}, 3000)
	}
}

function capitalizeFirstCharacter(str: string) {
	if (!str) return '' // Handle empty strings
	return str.charAt(0).toUpperCase() + str.slice(1)
}
</script>
