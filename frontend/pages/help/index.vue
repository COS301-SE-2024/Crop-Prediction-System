<template>
	<div class="p-6">
		<TabMenu :model="tabs" v-model:activeIndex="activeIndex" />
		<Card v-if="activeIndex === 0" class="mt-6">
			<template #title>
				<p>Home Dashboard</p>
			</template>
			<template #content>
				<div class="w-full flex flex-col justify-between items-start gap-4">
					<h1 class="text-2xl font-semibold">Field Card</h1>
					<div class="flex flex-row justify-between items-center gap-2">
						<p>To select a field, use the dropdown at the top of the FieldCard:</p>
					</div>
					<Dropdown v-model="selctedField" :options="fields" optionLabel="name" placeholder="Select a Field" />
					<p class="font-semibold">
						The FieldCard displays information about the selected field. The card includes the following data:
					</p>
					<ul class="list-disc ml-6">
						<li>AI Weather Summary: Provides an overview of the field's weather conditions.</li>
						<li>Field Health Chart: Displays the field's health status over time.</li>
						<li>Precipitation and Sprayability Chart: Displays the field's precipitation and sprayability.</li>
					</ul>
					<div class="flex flex-row justify-between items-center">
						<p>
							Both of the charts have a help button that displays more information about them. Click the question
							mark button to learn more.
						</p>
						<p></p>
					</div>
					<Button icon="pi pi-question-circle" severity="secondary" rounded size="small" text v-tooltip />
					<h1 class="text-2xl font-semibold">Advanced Statistics</h1>
					<p>Click on the Advanced Statistics button to open the Advanced Statistics panel.</p>
					<Button icon="pi pi-plus" severity="secondary" label="View More Statistics" size="small" outlined v-tooltip />
					<p>The Advanced Statistics panel provides additional statistics about the selected field.</p>
					<h1 class="text-2xl font-semibold">Graphs</h1>
					<p>
						All graphs are interactive and allow you to filter the data on the graph. This can be achieved by pressing
						the legend above the field to filter the data.
					</p>
					<p>To interact with the graph, click on either First Dataset or Second Dataset.</p>
					<Chart type="line" :data="chartData" :options="chartOptions" class="h-34 w-full" />
					<h1 class="text-2xl font-semibold">Maps Interface</h1>
					<p>
						The Maps Interface allows you to view the field's location on a map. Selected fields will be filled with a
						green color, and unselected fields will be filled with a purple color.
					</p>
				</div>
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
					<li><strong>Date:</strong> The date of the entry.</li>
					<li><strong>Field Name:</strong> The name of the field to which the entry belongs.</li>
					<li><strong>Crop Type:</strong> The crop type of the field.</li>
					<li><strong>Max Temperature:</strong> Recorded maximum temperature.</li>
					<li><strong>Min Temperature:</strong> Recorded minimum temperature.</li>
					<li><strong>Mean Temperature:</strong> Recorded mean temperature.</li>
					<li><strong>Humidity:</strong> Recorded humidity level.</li>
					<li><strong>Pressure:</strong> Recorded atmospheric pressure.</li>
					<li><strong>Dew Point:</strong> Recorded dew point temperature.</li>
					<li><strong>UV Index:</strong> Recorded UV index value.</li>
					<li><strong>Rainfall:</strong> Recorded rainfall amount.</li>
					<li><strong>Soil Moisture:</strong> Recorded soil moisture level.</li>
					<li><strong>Soil Temperature:</strong> Recorded soil temperature.</li>
					<li><strong>Health Index:</strong> Recorded health index value.</li>
					<li><strong>Yield:</strong> Recorded yield amount.</li>
					<li><strong>Sprayability:</strong> Recorded sprayability level.</li>
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
import { ref, onMounted } from 'vue'
import TabMenu from 'primevue/tabmenu'
import Card from 'primevue/card'
import Chart from 'primevue/chart'

onMounted(() => {
	chartData.value = setChartData()
	chartOptions.value = setChartOptions()
})

const chartData = ref()
const chartOptions = ref()

const setChartData = () => {
	const documentStyle = getComputedStyle(document.documentElement)

	return {
		labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
		datasets: [
			{
				label: 'First Dataset',
				data: [65, 59, 80, 81, 56, 55, 40],
				fill: false,
				borderColor: documentStyle.getPropertyValue('--cyan-500'),
				tension: 0.4,
			},
			{
				label: 'Second Dataset',
				data: [28, 48, 40, 19, 86, 27, 90],
				fill: false,
				borderColor: documentStyle.getPropertyValue('--gray-500'),
				tension: 0.4,
			},
		],
	}
}
const setChartOptions = () => {
	return {
		maintainAspectRatio: false,
		responsive: true,
		plugins: {
			legend: {
				display: true,
			},
		},
		scales: {
			x: {
				ticks: {
					autoSkip: false,
				},
				grid: {
					color: 'rgba(192, 192, 192, 0.3)',
					display: true,
				},
			},
			y: {
				beginAtZero: false,
				ticks: {
					stepSize: 10,
				},
				grid: {
					color: 'rgba(192, 192, 192, 0.3)',
					display: true,
				},
			},
		},
	}
}

const activeIndex = ref(0)
const tabs = [
	{ label: 'Home Dashboard', icon: 'pi pi-fw pi-home' },
	{ label: 'Add Field Data', icon: 'pi pi-fw pi-plus' },
	{ label: 'Manage Fields', icon: 'pi pi-fw pi-map' },
	{ label: 'View Logs', icon: 'pi pi-fw pi-list' },
]

const fields = [{ name: 'Field 1' }, { name: 'Field 2' }, { name: 'Field 3' }]

const selctedField = ref(null)
</script>

<style>
.help-menu {
	padding: 20px;
}
</style>
