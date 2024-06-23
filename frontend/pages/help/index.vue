<template>
	<div class="p-6">
		<TabMenu :model="tabs" v-model:activeIndex="activeIndex" />
		<Card v-if="activeIndex === 0" class="mt-6">
			<template #title>
				<p>Home Dashboard</p>
			</template>
			<template #content>
				<h2 class="text-xl font-bold mb-4">Data Cards</h2>
				<ul class="list-disc ml-6 mb-4">
					<li>
						<strong>Overall Crop Health:</strong> Shows the average health of all fields. Includes a graph, percentage
						change from last week, and a health status pill (e.g., Severe is displayed red, Moderate is displayed
						orange, Healthy is displayed green).
					</li>
					<li>
						<strong>Current Temperature:</strong> Displays the upcoming temperature trends. Includes a graph,
						percentage change from last week, and a status pill.
					</li>
					<li>
						<strong>Soil Moisture:</strong> Indicates the average soil moisture levels across all fields. Includes a
						graph, percentage change from last week, and a status pill.
					</li>
					<li>
						<strong>Rainfall:</strong> Shows upcoming rainfall predictions. Includes a graph, percentage change from
						last week, and a status pill.
					</li>
					<li>
						<strong>Humidity:</strong> Displays upcoming humidity levels. Includes a graph, percentage change from
						last week, and a status pill.
					</li>
				</ul>
				<h2 class="text-xl font-bold mb-4">Farm Map</h2>
				<p class="mb-4">A map-based interface that provides a visual overview of your fields. Features include:</p>
				<ul class="list-disc ml-6 mb-4">
					<li><strong>Map/Satellite View:</strong> Toggle between map and satellite views.</li>
					<li>
						<strong>Edit Button:</strong> Click the edit icon to navigate to the manage fields page where you can add
						or modify fields.
					</li>
				</ul>
				<h2 class="text-xl font-bold mb-4">Fields Table</h2>
				<p class="mb-4">A table listing all fields with the following columns:</p>
				<ul class="list-disc ml-6 mb-4">
					<li>
						<strong>Field Name:</strong> Displays the name of the field with a health status pill (green for healthy,
						orange for moderate, red for severe).
					</li>
					<li><strong>T/H:</strong> Predicted tons per hectare.</li>
					<li><strong>Crop Type:</strong> The type of crop planted in each field.</li>
				</ul>
				<h2 class="text-xl font-bold mb-4">Polar Stats</h2>
				<p class="mb-4">Provides a summary of various environmental factors affecting your fields:</p>
				<ul class="list-disc ml-6 mb-4">
					<li>
						<strong>Progress Bars:</strong> Show the current status of moisture, temperature, humidity, soil, and
						rainfall.
					</li>
					<li>
						<strong>Polar Chart:</strong> Visual representation of the data with the outer bound indicating the best
						case.
					</li>
				</ul>
			</template>
		</Card>
		<Card v-if="activeIndex === 1" class="mt-6">
			<template #title>
				<p>Add Field Data</p>
			</template>
			<template #content>
				<h2 class="text-xl font-bold mb-4">Manual Field Inputs</h2>
				<p class="mb-4">To add data, follow these steps:</p>
				<ol class="list-decimal ml-6 mb-4">
					<li>
						<strong>Select a Field:</strong> Use the "Add Field Data" dropdown menu to select the specific field you
						want to input data for.
					</li>
					<li>
						<strong>Enter Data:</strong>
						<ul class="list-disc ml-6 mb-4">
							<li>Temperature: Input the current temperature for the field in degrees Celsius.</li>
							<li>Humidity: Input the humidity level for the field.</li>
							<li>Rainfall: Input the rainfall amount for the field in millimeters.</li>
							<li>UV Index: Input the UV index for the field.</li>
							<li>Soil Moisture: Input the soil moisture level for the field.</li>
							<li>Soil pH: Input the pH level of the soil for the field.</li>
							<li>Soil Conductivity: Input the soil conductivity for the field.</li>
						</ul>
					</li>
					<li>
						<strong>Save or Cancel:</strong> Click the "Save" button to store the entered data or click the "Cancel"
						button to discard the changes.
					</li>
				</ol>
			</template>
		</Card>
		<Card v-if="activeIndex === 2" class="mt-6">
			<template #title>
				<p>Manage Fields</p>
			</template>
			<template #content>
				<h2 class="text-xl font-bold mb-4">Adding a Field</h2>
				<ol class="list-decimal ml-6 mb-4">
					<li>
						<strong>Add Field Button:</strong> Click the "Add Field" button at the top right corner of the page. This
						will open a popup dialog.
					</li>
					<li>
						<strong>Popup Dialog:</strong>
						<ul class="list-disc ml-6 mb-4">
							<li>Field Name: Enter the name of the field.</li>
							<li>Crop Type: Select the crop type from the dropdown menu.</li>
							<li>Cancel Button: Click to discard changes and close the dialog.</li>
							<li>Save Button: Click to proceed to the map interaction.</li>
						</ul>
					</li>
					<li>
						<strong>Interactive Map:</strong> After clicking "Save," the map becomes interactive, allowing you to draw
						your field. Click on points on the map to define the boundary of your field. Continue adding points until
						you return to the original point to close the field.
					</li>
					<li>
						<strong>Confirm Dialog:</strong> Once the field is drawn, a confirmation dialog will pop up, prompting you
						to save the field.
					</li>
				</ol>
			</template>
		</Card>
		<Card v-if="activeIndex === 3" class="mt-6">
			<template #title>
				<p>View Logs</p>
			</template>
			<template #content>
				<h2 class="text-xl font-bold mb-4">Data Entry Table</h2>
				<p class="mb-4">The table includes the following columns:</p>
				<ul class="list-disc ml-6 mb-4">
					<li><strong>Entry ID:</strong> The unique identifier for each entry.</li>
					<li><strong>Created At:</strong> The timestamp when the entry was created.</li>
					<li><strong>Temperature:</strong> Recorded temperature value.</li>
					<li><strong>Humidity:</strong> Recorded humidity level.</li>
					<li><strong>UV Index:</strong> Recorded UV index value.</li>
					<li><strong>Rainfall:</strong> Recorded rainfall amount.</li>
					<li><strong>Moisture:</strong> Recorded soil moisture level.</li>
					<li><strong>pH:</strong> Recorded soil pH value.</li>
					<li><strong>Conductivity:</strong> Recorded soil conductivity.</li>
					<li><strong>Field ID:</strong> The identifier of the field to which the entry belongs.</li>
					<li>
						<strong>Manual Entry:</strong> Indicates if the data was entered manually (green tick) or recorded by an
						IoT sensor (red cross).
					</li>
				</ul>
				<h2 class="text-xl font-bold mb-4">Table Features</h2>
				<ul class="list-disc ml-6 mb-4">
					<li><strong>Search Bar:</strong> Use the keyword search to filter entries.</li>
					<li>
						<strong>Sorting:</strong> Click on the column headers to sort the data in ascending or descending order.
					</li>
					<li><strong>Selection:</strong> Use the radio/check buttons to select specific entries.</li>
					<li>
						<strong>Pagination:</strong> Navigate through the entries using the paginator at the bottom. You can
						adjust the number of entries displayed per page via the dropdown menu or navigate pages using the left and
						right icons.
					</li>
				</ul>
				<h2 class="text-xl font-bold mb-4">Actions</h2>
				<ul class="list-disc ml-6 mb-4">
					<li><strong>Export Button:</strong> Exports the selected entries as a CSV file.</li>
					<li><strong>Print Button:</strong> Prints the selected entries to a PDF.</li>
				</ul>
			</template>
		</Card>
	</div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import TabMenu from 'primevue/tabmenu'
import Card from 'primevue/card'

const activeIndex = ref(0)
const tabs = [
	{ label: 'Home Dashboard', icon: 'pi pi-fw pi-home' },
	{ label: 'Add Field Data', icon: 'pi pi-fw pi-plus' },
	{ label: 'Manage Fields', icon: 'pi pi-fw pi-map' },
	{ label: 'View Logs', icon: 'pi pi-fw pi-list' },
]
</script>

<style>
.help-menu {
	padding: 20px;
}
</style>
