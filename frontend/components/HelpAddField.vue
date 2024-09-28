<template>
	<Card v-if="activeIndex === 3" class="mt-6 p-5">
		<template #content>
			<div class="w-full flex flex-col justify-between items-start gap-4">
				<h1 class="text-2xl font-semibold">Add Field Help</h1>
				<p>
					Welcome to the Add Field page! This page guides you through the process of adding a new field to your account.
					The process consists of three main steps:
				</p>

				<h2 class="text-xl font-semibold">1. Field Info</h2>
				<p>In this step, you provide basic information about your new field:</p>
				<ul class="list-disc ml-6">
					<li><strong>Field Name:</strong> Enter a unique name for your field.</li>
					<li><strong>Crop Type:</strong> Select the type of crop you are planting from the dropdown menu.</li>
				</ul>
				<p>Example:</p>
				<div class="flex flex-col gap-2">
					<label for="field_name">Field Name</label>
					<InputText id="field_name" placeholder="Name" class="w-full sm:w-[250px]" />
					<small id="field_name">Enter your new field name above.</small>
					<Dropdown
						v-model="selectedItem"
						:options="cropOptions"
						optionLabel="name"
						placeholder="Select a Crop Type"
						class="w-full sm:w-[250px] mt-4"
					/>
				</div>

				<h2 class="text-xl font-semibold">2. Field Map</h2>
				<p>In this step, you draw the boundaries of your field on the map:</p>
				<ul class="list-disc ml-6">
					<li>Use the map to locate your field's area.</li>
					<li>Use the drawing tools to outline the field's boundaries.</li>
					<li>You can edit the shape by dragging the corners or edges of the polygon.</li>
				</ul>

				<h2 class="text-xl font-semibold">3. Confirm</h2>
				<p>In the final step, review the information you have entered:</p>
				<ul class="list-disc ml-6">
					<li><strong>Field Name:</strong> Verify the field name is correct.</li>
					<li><strong>Crop Type:</strong> Ensure you have selected the correct crop type.</li>
					<li><strong>Field Map:</strong> Check that the field area has been properly drawn.</li>
				</ul>
				<p>
					If everything is correct, click the <Button label="Save Field" size="small" icon="pi pi-check" /> button to
					save your new field.
				</p>

				<h2 class="text-xl font-semibold">Navigation Buttons</h2>
				<p>Use the navigation buttons at the bottom of each step to move between steps:</p>
				<ul class="list-disc ml-6">
					<li class="mb-2"><Button label="Back" size="small" icon="pi pi-arrow-left" />: Go to the previous step.</li>
					<li>
						<Button label="Next" size="small" icon="pi pi-arrow-right" iconPos="right" />: Proceed to the next step.
					</li>
				</ul>

				<h2 class="text-xl font-semibold">Loading Indicators</h2>
				<p>
					When saving the field, a loading indicator will appear on the
					<Button label="Save Field" size="small" icon="pi pi-check" /> button. Please wait until the process is
					complete.
				</p>

				<h2 class="text-xl font-semibold">Success Message</h2>
				<p>
					After successfully saving the field, a success message will appear confirming that your field has been saved.
				</p>
				<p>Example:</p>
				<div class="flex items-center gap-2">
					<i class="pi pi-check-circle text-green-500"></i>
					<span class="text-green-500">Field saved successfully!</span>
				</div>
			</div>
		</template>
	</Card>
</template>

<script setup>
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
