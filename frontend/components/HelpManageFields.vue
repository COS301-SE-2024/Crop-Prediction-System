<template>
	<Card v-if="activeIndex === 2" class="mt-6 p-5">
		<template #content>
			<div class="w-full flex flex-col justify-between items-start gap-4">
				<h1 class="text-2xl font-semibold">Manage Fields Help</h1>
				<p>
					Welcome to the Manage Fields page! This page allows you to view, edit, train, and delete your team's fields.
					Here's how to use it:
				</p>

				<h2 class="text-xl font-semibold">1. Searching and Filtering Fields</h2>
				<p>Use the search bar to find fields by name. You can also filter fields by crop type using the dropdown menu.</p>
				<div class="flex flex-col sm:flex-row justify-start items-center gap-4 mt-4 w-full">
					<InputText placeholder="Search Field Name..." class="w-full sm:w-[375px]" />
					<Dropdown
						v-model="selectedItem"
						:options="cropOptions"
						optionLabel="name"
						placeholder="Filter by Crop Type"
						class="w-full sm:w-[250px]"
						showClear
					/>
				</div>

				<h2 class="text-xl font-semibold">2. Training Fields</h2>
				<p>You can train individual fields or all fields at once:</p>
				<ul class="list-disc ml-6">
					<li>
						<strong>Train All:</strong> Click the
						<Button label="Train All" icon="pi pi-microchip-ai" size="small" severity="secondary" outlined /> button
						to schedule training for all fields.
					</li>
					<li>
						<strong>Train Individual Field:</strong> Click the
						<Button label="Train" icon="pi pi-microchip-ai" size="small" severity="secondary" outlined /> button on a
						field card to schedule training for that specific field.
					</li>
				</ul>
				<p>Training updates the field's data based on the latest information.</p>

				<h2 class="text-xl font-semibold">3. Viewing Field Details</h2>
				<p>Each field is displayed as a card containing key information:</p>
				<ul class="list-disc ml-6">
					<li><strong>Field Name:</strong> The name of the field.</li>
					<li><strong>Crop Type:</strong> The type of crop planted.</li>
					<li><strong>Field Size:</strong> The size of the field in hectares.</li>
					<li><strong>Field ID:</strong> The unique identifier for the field.</li>
				</ul>
				<p>
					Use the buttons at the bottom of each card to <strong>View or Edit</strong> the field or to
					<strong>Delete</strong> it.
				</p>

				<h2 class="text-xl font-semibold">4. Editing a Field</h2>
				<p>
					Click the <Button label="View or Edit" size="small" /> button on a field card to open the field's details in a
					dialog. In this dialog, you can:
				</p>
				<ul class="list-disc ml-6">
					<li>
						<strong>Edit Field Name:</strong> Click the <i class="pi pi-pencil" /> icon next to the field name to
						enable editing. After changing the name, click the <i class="pi pi-check" /> icon to save.
					</li>
					<li>
						<strong>Edit Crop Type:</strong> Click the <i class="pi pi-pencil" /> icon next to the crop type to select
						a new crop from the dropdown. Click the <i class="pi pi-check" /> icon to save.
					</li>
					<li>
						<strong>Edit Field Map:</strong> Click the
						<Button label="Edit Map" icon="pi pi-pencil" size="small" severity="secondary" outlined /> button to
						enable map editing. Adjust the field polygon by dragging the corners or moving the entire polygon. Click
						the <Button label="Save Changes" icon="pi pi-check" size="small" severity="info" outlined /> button to
						save your changes.
					</li>
				</ul>

				<h2 class="text-xl font-semibold">5. Deleting a Field</h2>
				<p>
					To delete a field, click the <Button label="Delete" severity="danger" size="small" /> button on the field
					card. A confirmation dialog will appear to ensure you want to proceed with the deletion.
				</p>

				<h2 class="text-xl font-semibold">6. Loading Indicators</h2>
				<p>
					While fields are being fetched or actions are being performed, loading indicators and messages will appear.
					Please wait until the operations are complete.
				</p>
				<div class="w-full h-full mt-4 gap-5 flex flex-col items-center justify-center">
					<ProgressSpinner />
					<h2 class="dark:text-white font-bold">Fetching Fields...</h2>
				</div>

				<h2 class="text-xl font-semibold">7. No Fields Available</h2>
				<p>
					If you have no fields available, you can start adding fields on the
					<NuxtLink to="/inputs/add-field" class="underline">Add Field Page</NuxtLink>.
				</p>
			</div>
		</template>
	</Card>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
	activeIndex: {
		type: Number,
		default: 0,
	},
})

const selectedItem = ref()
const cropOptions = ref([
	{ name: 'Wheat', id: 1 },
	{ name: 'Maize', id: 2 },
	{ name: 'Soybeans', id: 3 },
	{ name: 'Canola', id: 4 },
	{ name: 'Barley', id: 5 },
	{ name: 'Sunflower', id: 6 },
	{ name: 'Groundnuts', id: 7 },
	{ name: 'Sorghum', id: 8 },
	{ name: 'Oats', id: 9 },
])
</script>
