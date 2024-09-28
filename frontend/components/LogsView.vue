<template>
	<Toast />
	<DataTable
		v-model:value="entries"
		ref="dataEntries"
		scrollable
		scrollHeight="450px"
		size="small"
		class="bg-surface-100 dark:bg-surface-800 rounded-md"
		paginator
		@cell-edit-complete="onCellEditComplete"
		@cell-edit-init="onCellEditInit"
		editMode="cell"
		:rows="10"
		:rowsPerPageOptions="[5, 10, 20, 50, 100]"
		tableStyle="min-width: 70rem"
		paginatorTemplate="FirstPageLink PrevPageLink CurrentPageReport NextPageLink LastPageLink RowsPerPageDropdown"
		currentPageReportTemplate="{first} to {last} of {totalRecords}"
		v-model:selection="selectedDataEntries"
		:selectAll="selectAll"
		@select-all-change="onSelectAllChange"
		@row-select="onRowSelect"
		@row-unselect="onRowUnselect"
		v-model:filters="filters"
		:globalFilterFields="[
			'field_name',
			'date',
			'crop_type',
			'tempmax',
			'tempmin',
			'tempmean',
			'pressure',
			'humidity',
			'dew_point',
			'rain',
			'uvi',
			'soil_moisture',
			'soil_temperature',
			'health',
			'yield',
			'sprayability',
		]"
	>
		<template #header>
			<div class="grid gap-2">
				<div class="flex flex-wrap items-center justify-between gap-2 sticky">
					<p class="text-xl text-900 font-bold">Data Entry Logs</p>
					<div class="flex text-xs gap-2">
						<Button icon="pi pi-external-link" severity="secondary" label="Export" @click="exportSelectedCSV" />
						<Button
							icon="pi pi-chart-line"
							severity="success"
							label="Generate Field Report"
							@click="visible = true"
						/>
					</div>
				</div>
				<Dialog v-model:visible="visible" modal header="Print" :style="{ width: '25rem' }">
					<span class="text-surface-500 dark:text-surface-400 block mb-8"
						>Which farms data would you like to Print?</span
					>

					<div class="flex w-full items-center gap-4 mb-8">
						<div class="card w-full flex justify-content-center">
							<Dropdown
								v-model="selectedField"
								:options="uniqueFieldNames"
								placeholder="Select a Field"
								class="w-full"
							/>
						</div>
					</div>
					<div class="flex justify-end gap-2">
						<Button type="button" label="Cancel" severity="secondary" @click="visible = false"></Button>
						<Button
							type="button"
							label="Print"
							@click="
								() => {
									visible = false
									triggerPrint()
								}
							"
						></Button>
					</div>
				</Dialog>
				<div class="flex justify-content-center text-xs gap-2">
					<IconField iconPosition="left">
						<InputIcon>
							<i class="pi pi-search" />
						</InputIcon>
						<InputText v-model="filters['global'].value" placeholder="Keyword Search" />
					</IconField>
				</div>
				<p class="text-sm text-surface-700 dark:text-surface-0 font-normal">
					To edit the table, select the value you'd like to modify, input the new value, and press 'Enter'. A
					confirmation message will appear if the change is successfully saved.
					<br />
					<span class="font-bold">
						Note: The following fields cannot be edited: Date, Field Name, Crop Type, Health, Yield, and Sprayability.
					</span>
				</p>
			</div>
		</template>
		<template #empty>
			<div class="flex flex-col gap-3">
				<Skeleton height="20px"></Skeleton>
				<Skeleton height="20px"></Skeleton>
				<Skeleton height="20px"></Skeleton>
			</div>
		</template>

		<template #loading> Loading data entries. Please wait.</template>
		<Column selectionMode="multiple" headerStyle="width: 3rem" :rowEditor="true"></Column>
		<Column
			v-for="col of columns"
			:key="col.field"
			style="min-width: 9rem; font-size: 0.8rem"
			:field="col.field"
			:header="col.header"
			sortable
		>
			<template #editor="{ data, field }">
				<template
					v-if="
						field !== 'date' &&
						field !== 'field_name' &&
						field !== 'crop_type' &&
						field !== 'health' &&
						field !== 'yield' &&
						field !== 'sprayability'
					"
				>
					<InputNumber
						:disabled="userRole === 'data_analyst'"
						v-model="data[field]"
						autofocus
						size="small"
						:minFractionDigits="0"
						:maxFractionDigits="10"
					/>
				</template>
				<template v-else>
					<p>{{ data[field] }}</p>
				</template>
			</template>
		</Column>
	</DataTable>
	<Dialog header="Selected Rows" v-model:visible="dialogVisible" :modal="true" :closable="true">
		<Button label="Print" icon="pi pi-print" @click="triggerPrint" />
		<pre>{{ printableContent }}</pre>
	</Dialog>
</template>

<script setup lang="ts">
import { ref, toRaw, onMounted } from 'vue'
import { FilterMatchMode } from 'primevue/api'
import { useToast } from 'primevue/usetoast'
import { Chart } from 'chart.js/auto'

const visible = ref(false)
const selectedDataEntries = ref([])
const dialogVisible = ref(false)
const printableContent = ref('')
const dataEntries = ref()
const selectAll = ref<boolean>()
const toast = useToast()

// Define your columns
const columns = [
	{ field: 'date', header: 'Date' },
	{ field: 'field_name', header: 'Field Name' },
	{ field: 'crop_type', header: 'Crop Type' },
	{ field: 'tempmax', header: 'Max Temp (°C)' },
	{ field: 'tempmin', header: 'Min Temp (°C)' },
	{ field: 'tempmean', header: 'Mean Temp (°C)' },
	{ field: 'pressure', header: 'Pressure (hPa)' },
	{ field: 'humidity', header: 'Humidity (%)' },
	{ field: 'dew_point', header: 'Dew Point (°C)' },
	{ field: 'rain', header: 'Rainfall (mm)' },
	{ field: 'uvi', header: 'UV Index ' },
	{ field: 'soil_moisture', header: 'Soil Moisture (wfv)' },
	{ field: 'soil_temperature', header: 'Soil Temp (°C)' },
	{ field: 'pred_health', header: 'Health Index (%)' },
	{ field: 'pred_yield', header: 'Yield (t/ha)' },
	{ field: 'pred_sprayability', header: 'Sprayability (%)' },
]

const filters = ref({
	global: { value: null, matchMode: FilterMatchMode.CONTAINS },
	field_name: { value: null, matchMode: FilterMatchMode.CONTAINS },
	date: { value: null, matchMode: FilterMatchMode.DATE_IS },
	tempmax: { value: null, matchMode: FilterMatchMode.EQUALS },
	tempmin: { value: null, matchMode: FilterMatchMode.EQUALS },
	tempmean: { value: null, matchMode: FilterMatchMode.EQUALS },
	pressure: { value: null, matchMode: FilterMatchMode.EQUALS },
	humidity: { value: null, matchMode: FilterMatchMode.EQUALS },
	dew_point: { value: null, matchMode: FilterMatchMode.EQUALS },
	rain: { value: null, matchMode: FilterMatchMode.EQUALS },
	uvi: { value: null, matchMode: FilterMatchMode.EQUALS },
	soil_moisture: { value: null, matchMode: FilterMatchMode.EQUALS },
	soil_temperature: { value: null, matchMode: FilterMatchMode.EQUALS },
	health: { value: null, matchMode: FilterMatchMode.EQUALS },
	yield: { value: null, matchMode: FilterMatchMode.EQUALS },
	sprayability: { value: null, matchMode: FilterMatchMode.EQUALS },
	crop_type: { value: null, matchMode: FilterMatchMode.CONTAINS },
})

// Fetch user data and entries from the API
const entries = ref([])
const userRole = ref('')
const fetchEntryData = async () => {
	const user = useSupabaseUser()

	const teamID = await $fetch('/api/getTeamID', {
		params: { userid: user?.value?.id },
	})
	userRole.value = teamID.role

	const entryData = await $fetch('/api/getTeamFieldData', {
		params: { team_id: teamID.team_id },
	})

	entries.value = entryData.map((entry: any) => ({
		...entry,
		yield: entry.pred_yield === null ? 'N/A' : entry.pred_yield.toFixed(2),
	}))
}

onMounted(async () => {
	await fetchEntryData()
	console.log('User Role: ', userRole.value)
})

const onSelectAllChange = (event: { checked: boolean }) => {
	selectAll.value = event.checked

	if (selectAll.value) {
		selectedDataEntries.value = [...entries.value]
	} else {
		selectedDataEntries.value = []
	}
}

const onRowSelect = () => {
	selectAll.value = selectedDataEntries.value.length === entries.value.length
}

const onRowUnselect = () => {
	selectAll.value = false
}

const printContent = ref('')

// Function to prepare print content
const preparePrintContent = async () => {
	if (!selectedField.value) {
		toast.add({
			severity: 'error',
			summary: 'No field selected',
			detail: 'Please select a field to print',
			life: 3000,
		})
		return false
	}
	const fieldEntries = entries.value.filter((entry) => entry.field_name === selectedField.value)
	if (fieldEntries.length === 0) {
		toast.add({
			severity: 'warn',
			summary: 'No Data',
			detail: 'No data available for the selected field',
			life: 3000,
		})
		return false
	}

	// Prepare data for the chart
	const labels = fieldEntries.map((entry) => entry.date)
	const tempMaxData = fieldEntries.map((entry) => entry.tempmax)
	const tempMinData = fieldEntries.map((entry) => entry.tempmin)
	const tempMeanData = fieldEntries.map((entry) => entry.tempmean)
	const pressureData = fieldEntries.map((entry) => entry.pressure)
	const humidityData = fieldEntries.map((entry) => entry.humidity)
	const dewPointData = fieldEntries.map((entry) => entry.dew_point)
	const rainfallData = fieldEntries.map((entry) => entry.rain)
	const uviData = fieldEntries.map((entry) => entry.uvi)
	const soilMoistureData = fieldEntries.map((entry) => entry.soil_moisture)
	const soilTemperatureData = fieldEntries.map((entry) => entry.soil_temperature)
	const healthData = fieldEntries.map((entry) => entry.pred_health)
	const yieldData = fieldEntries.map((entry) => entry.pred_yield)
	const sprayabilityData = fieldEntries.map((entry) => entry.pred_sprayability)

	// Create a canvas element
	const canvas = document.createElement('canvas')
	canvas.width = 800
	canvas.height = 400
	document.body.appendChild(canvas)
	const canvas1 = document.createElement('canvas')
	canvas1.width = 800
	canvas1.height = 400
	document.body.appendChild(canvas1)
	const canvas2 = document.createElement('canvas')
	canvas2.width = 800
	canvas2.height = 400
	document.body.appendChild(canvas2)
	const canvas3 = document.createElement('canvas')
	canvas3.width = 800
	canvas3.height = 400
	document.body.appendChild(canvas3)
	const canvas4 = document.createElement('canvas')
	canvas4.width = 800
	canvas4.height = 400
	document.body.appendChild(canvas4)
	const canvas5 = document.createElement('canvas')
	canvas5.width = 800
	canvas5.height = 400
	document.body.appendChild(canvas5)
	const canvas6 = document.createElement('canvas')
	canvas6.width = 800
	canvas6.height = 400
	document.body.appendChild(canvas6)
	const canvas7 = document.createElement('canvas')
	canvas7.width = 800
	canvas7.height = 400
	document.body.appendChild(canvas7)
	const canvas8 = document.createElement('canvas')
	canvas8.width = 800
	canvas8.height = 400
	document.body.appendChild(canvas8)
	const canvas9 = document.createElement('canvas')
	canvas9.width = 800
	canvas9.height = 400
	document.body.appendChild(canvas9)
	const canvas10 = document.createElement('canvas')
	canvas10.width = 800
	canvas10.height = 400
	document.body.appendChild(canvas10)

	const chart = new Chart(canvas, {
		type: 'line',
		data: {
			labels: labels,
			datasets: [
				{
					label: 'Max Temperature',
					data: tempMaxData,
					borderColor: 'rgba(76, 175, 80, 1)',
					fill: false,
				},
				{
					label: 'Mean Temperature',
					data: tempMeanData,
					borderColor: 'rgba(255, 205, 86, 1)',
					fill: false,
				},
				{
					label: 'Min Temperature',
					data: tempMinData,
					borderColor: 'rgba(255, 99, 132, 1)',
					fill: false,
				},
			],
		},
		options: {
			responsive: false,
			animation: false,
			scales: {
				y: {
					title: {
						display: true,
						text: 'Temperature (°C)',
					},
				},
			},
		},
	})
	const chart1 = new Chart(canvas1, {
		type: 'line',
		data: {
			labels: labels,
			datasets: [
				{
					label: 'Pressure',
					data: pressureData,
					borderColor: 'rgba(255, 99, 132, 1)',
					fill: false,
				},
			],
		},
		options: {
			responsive: false,
			animation: false,
			scales: {
				y: {
					title: {
						display: true,
						text: 'Pressure (hPa)',
					},
				},
			},
		},
	})
	const chart2 = new Chart(canvas2, {
		type: 'line',
		data: {
			labels: labels,
			datasets: [
				{
					label: 'Humidity',
					data: humidityData,
					borderColor: 'rgba(168,84,246, 1)',
					fill: false,
				},
			],
		},
		options: {
			responsive: false,
			animation: false,
			scales: {
				y: {
					title: {
						display: true,
						text: 'Humidity (%)',
					},
				},
			},
		},
	})
	const chart3 = new Chart(canvas3, {
		type: 'line',
		data: {
			labels: labels,
			datasets: [
				{
					label: 'Dew Point',
					data: dewPointData,
					borderColor: 'rgba(115, 155, 208, 1)',
					fill: false,
				},
			],
		},
		options: {
			responsive: false,
			animation: false,
			scales: {
				y: {
					title: {
						display: true,
						text: 'Dew Point (°C)',
					},
				},
			},
		},
	})
	const chart4 = new Chart(canvas4, {
		type: 'line',
		data: {
			labels: labels,
			datasets: [
				{
					label: 'Rainfall',
					data: rainfallData,
					borderColor: 'rgba(6, 182, 212, 1)',
					fill: false,
				},
			],
		},
		options: {
			responsive: false,
			animation: false,
			scales: {
				y: {
					title: {
						display: true,
						text: 'Rainfall (mm)',
					},
				},
			},
		},
	})
	const chart5 = new Chart(canvas5, {
		type: 'line',
		data: {
			labels: labels,
			datasets: [
				{
					label: 'UV Index',
					data: uviData,
					borderColor: 'rgba(255, 205, 86, 1)',
					fill: false,
				},
			],
		},
		options: {
			responsive: false,
			animation: false,
			scales: {
				y: {
					title: {
						display: true,
						text: 'UV Index',
					},
				},
			},
		},
	})
	const chart6 = new Chart(canvas6, {
		type: 'line',
		data: {
			labels: labels,
			datasets: [
				{
					label: 'Soil Moisture',
					data: soilMoistureData,
					borderColor: 'rgba(6, 182, 212, 1)',
					fill: false,
				},
			],
		},
		options: {
			responsive: false,
			animation: false,
			scales: {
				y: {
					title: {
						display: true,
						text: 'Soil Moisture',
					},
				},
			},
		},
	})
	const chart7 = new Chart(canvas7, {
		type: 'line',
		data: {
			labels: labels,
			datasets: [
				{
					label: 'Soil Temperature',
					data: soilTemperatureData,
					borderColor: 'rgba(248, 114, 22, 1)',
					fill: false,
				},
			],
		},
		options: {
			responsive: false,
			animation: false,
			scales: {
				y: {
					title: {
						display: true,
						text: 'Soil Temperature (°C)',
					},
				},
			},
		},
	})
	const chart8 = new Chart(canvas8, {
		type: 'line',
		data: {
			labels: labels,
			datasets: [
				{
					label: 'Health Index',
					data: healthData,
					borderColor: 'green',
					fill: false,
				},
			],
		},
		options: {
			responsive: false,
			animation: false,
			scales: {
				y: {
					title: {
						display: true,
						text: 'Health Index (%)',
					},
				},
			},
		},
	})
	const chart9 = new Chart(canvas9, {
		type: 'line',
		data: {
			labels: labels,
			datasets: [
				{
					label: 'Yield',
					data: yieldData,
					borderColor: 'green',
					fill: false,
				},
			],
		},
		options: {
			responsive: false,
			animation: false,
			scales: {
				y: {
					title: {
						display: true,
						text: 'Yield (t/ha)',
					},
				},
			},
		},
	})
	const chart10 = new Chart(canvas10, {
		type: 'line',
		data: {
			labels: labels,
			datasets: [
				{
					label: 'Sprayability',
					data: sprayabilityData,
					borderColor: 'rgba(255, 205, 86, 1)',
					fill: false,
				},
			],
		},
		options: {
			responsive: false,
			animation: false,
			scales: {
				y: {
					title: {
						display: true,
						text: 'Sprayability (%)',
					},
				},
			},
		},
	})

	// Wait for the chart to render
	await new Promise((resolve) => setTimeout(resolve, 100))

	// Convert the chart to an image
	const chartImage = canvas.toDataURL('image/png')
	const chartImage1 = canvas1.toDataURL('image1/png')
	const chartImage2 = canvas2.toDataURL('image2/png')
	const chartImage3 = canvas3.toDataURL('image3/png')
	const chartImage4 = canvas4.toDataURL('image4/png')
	const chartImage5 = canvas5.toDataURL('image5/png')
	const chartImage6 = canvas6.toDataURL('image6/png')
	const chartImage7 = canvas7.toDataURL('image7/png')
	const chartImage8 = canvas8.toDataURL('image8/png')
	const chartImage9 = canvas9.toDataURL('image9/png')
	const chartImage10 = canvas10.toDataURL('image10/png')

	// Remove the canvas from the DOM
	document.body.removeChild(canvas)
	document.body.removeChild(canvas1)
	document.body.removeChild(canvas2)
	document.body.removeChild(canvas3)
	document.body.removeChild(canvas4)
	document.body.removeChild(canvas5)
	document.body.removeChild(canvas6)
	document.body.removeChild(canvas7)
	document.body.removeChild(canvas8)
	document.body.removeChild(canvas9)
	document.body.removeChild(canvas10)

	// Prepare the print content
	printContent.value = `
	<div class="headings">
    	<h2>Field: ${selectedField.value}</h2>
		<div style="text-align: center;">
      		<img src=" data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAA+gAAAPoCAYAAABNo9TkAAAACXBIWXMAAAsSAAALEgHS3X78AAAgAElEQVR4nOzdTW+U55Y/6tVbtoU4PrIPbSTTIraP4kjOS4MjoiaDIKxk0MkomfQY/p+g8w02HyH/T7DZ4z04YZTag6SJvAcQBeGQAJYwOsaF2pbKzbHV1ZZlW9pn4CowhBe/VNX9PPdzXVKUxAHXCmCrfs9a97r/4e9//3sAAIfXqNeGI2L6hQ/PvOSHvuxj0fq5Qx0s6TDWI2LuFf/t+j4+Nnfyrc/XOlkQAFTNPwjoAPDMC2F7ovVXRMSLIfxi76oqpR/3/PNi668X/1moB4A9BHQAKuGF4D3T+vtEPAvgAnda7UC/GM8C/PX2x06+9fliAEDmBHQAstCo16bjWZd7798nImI8XWV00KPYDe9rsTuO//TvJ9/6/FXj+QBQGgI6AKWwpwM+0fprbxBPfX6bYmifo28H98XWX0bpASgFAR2AQmnUazPxLHi3Q7jxczrhx3gW3tud9+tJKwKAPQR0AJJoBfGJ1l/tfzaKTgrt0fnrrb8vCu4ApCCgA9BVrbPh7dH0mRDEKY8Xg/ucs+4AdJOADkBH7Dkjvvevs0mLgu74JZ6Nyc+FM+4AdIiADsCB7QnjM/EsjOuKU2WP4llgvx5COwCHIKAD8Eat8+J7A7kwDm/WDu3XYzewX09aDQCFJ6AD8JxGvTYRz4L4TBhTh076JVqBPSKun3zr88Wk1QBQKAI6QMW1uuMz8SyQu1Mcemc9ng/s15NWA0BSAjpAhbTOjs/EszDufnEonh/j+dDuLDtARQjoABnbE8jbfxlXh/Jpj8VfD4EdIGsCOkBGBHKoBIEdIFMCOkDJ7TlDPhNG1qGK2iPxzrADlJyADlAyrS3rX8WzUG6pG9DWXjp3PSK+tSUeoFwEdICC2zO23g7l7iAH9utRtMJ6GIcHKDwBHaCAGvVae8v6V2FsHeicH+NZWJ9LXQwAzxPQAQqiUa+1O+RfhS450H2P4llY/zZ1MQAI6ADJtEbXv4pno+vOkgOptM+ufxu7Z9eNwgMkIKAD9NCeBW9G14Eia4/CWzQH0EMCOkCXtc6Tt0O5e8mBsvklnoV159YBukhAB+iCVii/HM6TA3lpn1u/KqwDdJ6ADtAhQjlQMcI6QIcJ6ABHIJQDRISwDtARAjrAAe1Z9PZ1COUAL3oUEd+EBXMAByagA+zDnlB+OSx6A9ivXyLiagjrAPsioAO8wgv3lH+ZuByAsrsW7lkHeC0BHeAFjXqtHcq/ioihxOUA5GY9ngX1b1MXA1AkAjpAPB1h/zosewPopfZyuW+MwAMI6ECF7RlhvxwRF9NWA1B5P8az8+pG4IFKEtCBymldjdbulhthByiW9gj8N65sA6pGQAcqodUtvxyuRgMok/aVbVd11YEqENCBrDXqtZnYDeaX0lYCwBH9OXaD+vXUhQB0i4AOZEe3HCBruupAtgR0IBt7zpbrlgNUw5/DWXUgIwI6UHqNeu1y7Abzs4lLASCNX2I3qF9NXQjAUQjoQCm17i2/HLvB3CZ2ACJ2N8C3x98XE9cCcGACOlAqlr4BsE+WygGlI6ADpWCMHYBDMv4OlIaADhRWaxv712GMHYCja4+/f2P7O1BUAjpQOK3z5VfCGDsA3fHniLjinDpQNAI6UBit8+VfR8SXiUsBoBquxW5H/XrqQgAiBHSgAFrnyy9HxMW0lQBQUT/G7kK5q6kLAapNQAeSaQXzKxExnrYSAIiIiEexO/p+NXUhQDUJ6EBP7Vn8djkEcwCK6VFEXA0L5YAeE9CBnrCRHYASsvkd6CkBHegqwRyADAjqQE8I6EBX7Lkq7asQzAHIw3pEfBuuaAO6REAHOsod5gBUhLvUgY4T0IGOEMwBqChBHegYAR04EsEcACJCUAc6QEAHDqW1/O2bEMwBYK8/R8TXlskBhyGgAwdiKzsAvJGt78ChCOjAvgjmAHBggjpwIAI68EaNeu1KCOYAcFjrsRvSr6QuBCg2AR14pUa9djl2F8CNp60EALLwKHYXyV1NXQhQTAI68DuNeu2r2B3JE8wBoPMexe4iuW9TFwIUi4AOPNWo12Zit2N+MW0lAFAJP8ZuR/166kKAYhDQgfZd5t9ExJeJSwGAKroWux31xdSFAGkJ6FBhrc3sVyLi3xOXAgBE/O/Y7ajb+A4VJaBDRdnMDgCFZOM7VJiADhVjARwAlIJFclBBAjpURKNem47dYG4BHACUx4+xG9TnUhcCdJ+ADplrnTP/JiIupa4FADi0P8duUHc+HTL2h9QFAN3TOme+GMI5AJTdpYhYbNRrX6cuBOgeHXTIUOs+86vhnDkA5OhRRFx2fzrkR0CHjLjPHAAqxf3pkBkj7pCJ1jj7XAjnAFAVX0bEXOs9AJABHXQoOePsAEAYe4csCOhQUsbZAYCXMPYOJWbEHUrIODsA8ArG3qHEdNChRFrj7N9ExNnEpQAAxfdL7HbTr6cuBNgfAR1KoFGvDUfElYj498SlAADl878j4srJtz5fS10I8HoCOhRco177KnaXwA0lLgUAKK/12F0i923qQoBXE9ChoFpL4K5GxMW0lQAAGfkxdoP6YupCgN+zJA4KqFGvfR27S+CEcwCgky7G7hK5r1MXAvyeDjoUSKNem47drrklcABAt/0Su930udSFALt00KEgWteh3A7hHADojbMRcduVbFAcOuiQmK45AFAAuulQADrokJCuOQBQELrpUAA66JCArjkAUGCPIuIr3XToPR106DFdcwCg4MZDNx2S0EGHHtE1BwBKyNl06CEddOgBXXMAoKScTYce0kGHLtI1BwAyopsOXaaDDl3SqNe+Dl1zACAf7W7616kLgVzpoEOHNeq1idjtml9MWwkAQNf8GLvd9MXUhUBOdNChgxr12lcRMRfCOQCQt4sRMdd67wN0iA46dECjXhuO3a75l4lLAQDotWux201fS10IlJ0OOhxRo16bid2uuXAOAFTRl7HbTZ9JXQiUnYAOR9C6cuQ/ImI8cSkAACmNR8R/uI4NjsaIOxxCaxHct2FDOwDAi36JiK8skIOD00GHA9qzCE44BwD4vbNhgRwcig467FNrEdw3EXEpdS0AACXx54j42gI52B8BHfahUa9Nx+6Wdl1zAICD+SV2t7zPpS4Eis6IO7xBo167HBHXQzgHADiMsxFxvfWeCngNHXR4BSPtAAAdZ+QdXkNAh5cw0g4A0DVG3uEVjLjDC4y0AwB0lZF3eAUddGgx0g4A0HNG3mEPAR0iolGvTUTEt6FrDgDQa79ExFcn3/p8MXUhkJoRdyqvUa99FRFzIZwDAKRwNiLmWu/JoNIEdCqtUa9diYj/JyKGEpcCAFBlQxHx/7Tem0FlGXGnklrnzb+NiIupawEA4Dk/xu7Iu3PpVI4OOpXTukJtLoRzAIAiuhi7I+/TqQuBXhPQqZQ9V6iNp60EAIDXGA9XsVFBAjqV0ajXvomIP4Xz5gAAZTAUEX9qvYeDSnAGnew5bw4AUHrOpVMJOuhkzXlzAIAsOJdOJQjoZMt5cwCArDiXTvYEdLLUukPTeXMAgLy0z6VfSV0IdIMz6GSldd78akR8mbgUAAC661pEXHYunZwI6GSjUa9NxO4yuLOJSwEAoDd+id3lcYupC4FOENDJQmthyPUw0g4AUDXrETFz8q3P51IXAkflDDqlt2cZnHAOAFA9Q2F5HJkQ0Ck1y+AAAAjL48iEEXdKq1GvXY2IS6nrAACgUP588q3PL6cuAg5DQKd0Wpvar4dlcAAAvNwvsXsu3YZ3SsWIO6WyZxmccA4AwKucjd1z6dOpC4GD0EGnNGxqBwDggGx4p1R00CkFm9oBADgEG94pFR10Cq/1DfVPqesAAKDU/tfJtz6/mroIeB0BnUKzqR0AgA6y4Z1CM+JOYQnnAAB02KXWe0woJB10Csc1agAAdJlr2CgkHXQKRTgHAKAH2tewDacuBPYS0CmM1jVqcyGcAwDQfWcjYs5d6RSJEXcKwR3nAAAk4q50CkMHneQa9dpMCOcAAKTRvit9JnUhIKCTVOuO8/8I4RwAgHSGIuI/Wu9NIRkBnWRa3wD/lLoOAABo+ZOQTkoCOkkI5wAAFJSQTjICOj3XqNeuhnAOAEBx/alRr32TugiqxxZ3eqoVzi+lrgMAAPbhzyff+vxy6iKoDh10ekY4BwCgZC613sNCTwjo9IRwDgBASQnp9IyATtcJ5wAAlJyQTk84g07XNOq14Yi4HhFnE5cCAACd8EtEzJx86/O11IWQJx10ukI4BwAgQ2cj4nrrvS50nIBOxwnnAABkTEinawR0Oko4BwCgAoR0ukJAp2OEcwAAKkRIp+MEdDpCOAcAoIKEdDpKQOfIhHMAACpMSKdjBHSORDgHAAAhnc4Q0Dk04RwAAJ4S0jkyAZ1DEc4BAOB3hHSOREDnwIRzAAB4JSGdQxPQORDhHAAA3khI51AEdA7qegjnAADwJmdj970z7JuAzr416rWrIZwDAMB+nW29h4Z9EdDZl9Y3lkup6wAAgJK5JKSzXwI6byScAwDAkQjp7IuAzmsJ5wAA0BFCOm8koPNKjXrtmxDOAQCgUy613mPDS/3D3//+99Q1UECNeu1yRPwpdR0AAJCh/3Xyrc+vpi6C4tFB53eEcwAA6Ko/td5zw3MEdJ4jnAMAQE8I6fyOEXeeatRr0xFxO3UdAABQIR+efOvzudRFUAw66ETE03B+PXUdAABQMddb78VBQOe5cD6UuBQAAKiaoRDSaTHiXnGNem04IuYiYjx1LQAAUGGPImL65Fufr6UuhHR00CusFc6vh3AOAACpjcduJ304dSGkI6BX2/WIOJu6CAAAICJ235tfT10E6QjoFdWo166GcA4AAEVztvVenQoS0Cuo9QV/KXUdAADAS10S0qtJQK+YRr12OYRzAAAoukut9+5UiIBeIa0v8D+lrgMAANiXPwnp1eKatYpw1zkAAJTSekTMnHzr87nUhdB9OugVIJwDAEBpDcXu9WvTqQuh+wT0zLXuUbwawjkAAJTVUERcdUd6/gT0/F0P16kBAEDZuSO9AgT0jLnrHAAAsuKO9MwJ6Jlq1GtXwnVqAACQm0ut9/pkyBb3DLlODQAAsve/Tr71+dXURdBZAnpmbGwHAIBKcP1ahgT0jLS2Oi6GcA4AAFWwHhETJ9/6fC11IXSGM+iZaIXz6yGcAwBAVbTvSHf9WiYE9Hx8Eza2AwBA1ZyN3SxABgT0DNjYDgAAlWazeyacQS85G9sBAIAWm91LTkAvMRvbAQCAPWx2LzkBvaRaiyDmImI8dS0AAEBhPIqIaZvdy8kZ9PL6NoRzAADgeeOxmxUoIQG9hBr12jcRcTF1HQAAQCFdbGUGSsaIe8lYCgcAAOyTpXElo4NeIq2lcJ6EQZfdXXicugQAgE74ppUhKAkBvSRaS+G+DRvboatWVtfip18X4sHSSupSAACOaigivm1lCUpAQC8PS+GgB27fX4yIiLn7i7G1vZO2GACAo7M0rkQE9BJo1GtXwlI46LoHSyuxsrp7I0lzY9OoOwCQi4utTEHBCegF16jXvoqIP6auA6pgrtU9b7v38LEuOgCQiz+2sgUFJqAXWKNem4iIq4nLgEq4fX8xmhubz31sa3snbt5ZSFQRAEDHXW1lDApKQC8oS+Ggd7a2d+Lew5ePsy8srfwuuAMAlJSlcQUnoBfXNxFxNnURUAW337AQThcdAMjI2XB1c2EJ6AXUqNcuR8Sl1HVAFTQ3Nl/ZPW9bWl59ujwOACADl1qZg4IR0AumUa9Nhyda0DP77Y7ffmGBHABAyX3Tyh4UiIBeIK2zIFfDuXPoiZXVtVhaXu34jwUAKIGh2F0a5zx6gQjoxeLcOfTQQbvizqIDAJlxHr1gBPSCcO4ceuvB0sqBz5U3Nzbj7sLrz6sDAJSM8+gFIqAXgHPn0HtzhzxTPjf/+o3vAAAl5Dx6QQjoiTl3Dr13+/7ioe8239re0UUHAHLjPHpBCOjpXQnnzqFntrZ33nit2pvce/j40AEfAKCgzsZuNiEhAT2hRr32VUT8e+o6oEpu3z/6iPrW9o5r1wCAHP17K6OQiICeSKNem4jd0XagR5obm0funrctLK3Ek/VmRz4XAECBXG1lFRIQ0NO5Gs6dQ091+po0164BABkaCo3EZAT0BBr12pWIuJi6DqiSldW1WFpe7fjnPOhVbQAAJXCxlVnoMQG9x1rXF/wxdR1QNd06M66LDgBk6o+uXus9Ab2HWtcWfJu6DqiaB0srXet0P1lvxoOlla58bgCAxL519VpvCei99U1EjKcuAqpmrssb1+c6sBkeAKCAxmM3w9AjAnqPtK4ruJS6Dqia2/cXu35neXNjM+4udGY7PABAwVxy9VrvCOg94Eo1SGNre6dj16q9yb2Hj3XRAYBcuXqtRwT03rgarlSDnrvdw9Hzre0dC+MAgFy5eq1HBPQua9RrX4cr1aDnmhubPeuety0srXR9nB4AIJGLrWxDFwnoXdS6luBK6jqgilJ1s2dvzSd5XQCAHrji6rXuEtC762oYbYeeW1ldi6Xl1WSv3a0r3QAAEjPq3mUCepc06rUrEXE2dR1QRbe7fK3amziLDgBk7Gwr69AFAnoXtMY+/pi6DqiiB0sryTvYT9ab8WBpJWkNAABd9Eej7t0hoHfH1dQFQBVtbe/EXOLuedtPdxZcuwYA5Oxq6gJyJKB3mNF2SOfuwuPCbFHf2t6Juwu93SIPANBDRt27QEDvIKPtkM7W9k7Pr1V7k3sPi/PAAACgC4y6d5iA3llXUxcAVXWzgCPlW9s7yRfWAQB02dXUBeREQO8Qo+2QTnNjMxYKupRtoQBL6wAAusioewcJ6B1gtB3Smr01n7qE13LtGgCQOaPuHSKgd8bV1AVAVa2srhW+Q+3aNQCgAq6mLiAHAvoRGW2HtIrePW9z7RoAkDmj7h0goB+B0XZI68HSSmm2pLt2DQCoAKPuRySgH803qQuAqtra3omfSna2e25+sTQPFAAADklGOgIB/ZAa9drXEXExdR1QVXcXHpdyZNzCOAAgcxdbWYlDENAPoVGvTUTElcRlQGU1NzZjbn4xdRmHsrS8WvildgAAR3SllZk4IAH9cK5GxFDqIqCqbt9fTF3CkZS9fgCANxgKW90PRUA/oEa99lUYbYdkVlbXYqHkV5atrK65dg0AyN3FVnbiAAT0A2jUa8PhSRAklUv3ee7+YinP0AMAHMDVVoZinwT0g7kSRtshmQdLK9mc325ubLp2DQDI3VDY3XUgAvo+Neq1mYj499R1QFVtbe/EXCbd87Z7D8u5iR4A4AD+vZWl2AcBff/c5wcJ3V14nN0d4lvbO9mM7AMAvIYstU8C+j607vE7m7oOqKrmxmbce5jnOPi9h/k9eAAAeMFZd6Pvj4D+Bu48h/RuZ75QTRcdAKgAd6Pvg4D+Zt+ExXCQzJP1ZumvVXuThYyW3wEAvMJQGHV/IwH9NVrLDL5MXQdU2c07C6lL6AlddACgAr60MO71BPTXu5q6AKiyldW1ynSWq/T/CgBU2tXUBRSZgP4KjXrtSkSMp64Dqmz21nzqEnpKFx0AqIDxVtbiJQT0l2gtL7BlEBJ6sLRSue3mK6tr8SDz8/YAABHxtYVxLyegv5zFcJDYXEW7yVX9/wYAKsXCuFcQ0F9gMRykV8XueVtzY1MXHQCoAgvjXkJA/72rqQuAKtva3omfKrK5/VV00QGAiriauoCiEdD3aNRrX4fFcJDU3YXHsbW9k7qMpHTRAYCKGG9lMFoE9JZGvTYcEVdS1wFVtrW9E/cePk5dRiHoogMAFXGllcUIAX0vi+EgMd3zZ3TRAYCKsDBuDwE9Ihr12nREXEpdB1SZ7vnv6aIDABVxqZXJKk9A3+WJDSSme/57uugAQIXIZCGgR6Ne+yoiLqauA6pO9/zldNEBgIq42MpmlVb5gB6e1EByD5ZWdM9fQRcdAKiQymezSgd016pBMegSv97CIwEdAKiEyl+7VtmA7lo1KIYHSyvR3NhMXUahrayuxcrqWuoyAAB6odLXrlU2oEfE1+FaNUju3oKz5/tx25QBAFANQ7Gb1SqpkgG9Ua9NRMQfU9cBVbeyuhZP1pupyyiFldU1kwYAQFX8sZXZKqeSAT2MtkMh3NU9PxBddACgQq6kLiCFygX0Rr02ExGXUtcBVdfc2Iyl5dXUZZTKgvP6AEB1XGplt0qpXECPij6JgaLRDT6cBza6AwDVcSV1Ab1WqYDeegJzMXUdUHVb2zu654d076FjAQBAZVysWhe9UgE9Iq6mLgCIeLS8GlvbO6nLKKWt7Z14sKSLDgBUxtXUBfRSZQJ6o167HBHjqesAIuaMtx+Jq+kAgAoZb2W5SqhMQI8Knl+AInJd2NE9WW+6ng4AqJIrqQvolUoE9Ea99nXonkMhWHLWGa6oAwAqZLyV6bKXfUBv1GvDUaEnLlBkW9s7seD8dEcsOccPAFTLlVa2y1r2AT0ivo6IodRFALvL4eiMre0dv54AQJUMxW62y1rWAb31hCX730QoC8vNOsuvJwBQMV/n3kXPOqCH7jkURnNj02KzDrMsDgComOy76NkGdN1zKBZLzbrD0j0AoGKy7qJnG9BD9xwKZcl56a6wdA8AqJisu+hZBvRGvTYRGf+mQdk8WW+6+7xLtrZ3PPwAAKom2y56lgE9dq9V0z2HgjCG3V2P/lNABwAqZSgivkldRDdkF9Bb3fNLqesAnjGG3V3uRAcAKuhSK/tlJbuAHrvdc6Agnqw3hccucyc6AFBRV1IX0GlZBXTdcyge4+29sWTMHQConuy66FkF9MjwCQqUnQVmvWHMHQCoqCupC+ikbAJ6a4uf7jkUiO3tvbWyupa6BACAXruU00b3bAJ6uFYNCsd28d7y6w0AVFQ2WTCLgN56YpLNbwrkwnh7b/n1BgAqKpt70bMI6LEbzt17DgWytb0TT9abqcuolK3tHWPuAEAVDUUmDdvSB3Tdcygm136lYcwdAKioLLropQ/ooXsOhbTS0MlNQQcdAKioLLropQ7ouudQXIJiGjbnAwAVVvoueqkDekRcDt1zKJzmxqaQmNCyhyMAQDUNxW5GLK2yB3Tdcygg56DTcrwAAKiwUmfE0gb0Rr12OSLGU9cB/J7t7Wk5XgAAVNh4KyuWUmkDekRcSV0A8HICYlqOGAAAFXcldQGHVcqA3qjXvgrdcygk4bAYnEMHACpsvJUZS6eUAT1Kfq4Acma8vRicQwcAKq6UmbF0Ab1Rr81ExMXUdVBcK6trsbW9k7qMyloWDAvBgxIAoOIutrJjqZQuoEfJ1+bTfcuNtfjLX2/Eg6WV1KVUkmBYDE/Wmx5UAQBVdzl1AQdVqoDeqNcmIuJS6joovq3tnfjbrfn4bnbOeegesyCuODws6Z2V1bX4/sZv8d3sXNy+v5i6HABg16VWhiyNvtQFHNCV1AVQLiura3Hth59jemoi3p88nbqc7AmExbLcWIvRkeHUZWRv9tZ8LOyZ2Gk/pPrw3YlEFQEAe1yJEnXSS9NBb9RrwxFRyk18pLW1vRM//bqgm94Dfn2LxQOT7tra3onvZueeC+dtL/sYAJDEV60sWQqlCeixu4VvKHURlNfK6u7ZdOOn3fNfawJhkQjo3dOeznnVkQ4PqwCgMIaiRBvdyxTQL6cugDzMzS/GtR9+Fl66wPnzYhESO29reydm97HfYvD4sR5WBQC8weXUBexXKQJ6o167HBHjqesgH0/Wm3Hth5/j9v1Fm647SCAsHg9NOmdpeTX+8tcb+xpfF9ABoFDGW5my8EoR0KNEIwmUS7ubLsR0hoBePP/t9+TImhub8f2N3+L7G7/t+4GegA4AhVOKTFn4gN66XP5s6jrIV3NjM76bnYubdxZ004/AkYFiav6PgH4Udxcex7Uffo6l5dUD/TwBHQAK52wrWxZaGa5Zu5y6AKrh3sPHsbS8GufPTMbYqZHU5ZSOhxvFZDrkcJ6sN+PmnQW/fgCQl8sRcT1xDa9V6A5661L5S6nroDoOM8rKruWGIEMebt939AUAMnWplTELq9ABPXTPSaS9DOqgY61QNI4e7F/76rS5+cXUpQAA3XM5dQGvU/SAXoqD/ORpa3snvr/x2xuvU2KXbmMxmQR5s63tnbh5ZyG+m53zQAMA8lfojFnYgN5agz+Uug5od9XuLjxOXQrQYUvLq3Hth5/j3kNf3wBQEUNFvnKtsAE9Cj56QLVsbe/ET78u6Ka/hs4jZdKekPn+xm++pgGgei6nLuBVChnQG/XadERcTF0HvKjdTb99fzF1KYVjlJqyuLvw2I4JAKi2i63MWTiFDOhR8HMBVNvW9k7Mze9uedY13iWcUwbNjc34bnYufvp1wZ9ZAKCQmbNwAb1Rrw1HxFep64A3ebLe1E1v8aCiuE4MDaYuoRBu31+Mv/z1hmWGAEDbV63sWSh9qQt4ia/CcjhKZG5+MZaWV+P8mckYHSnc1zgVN3j8WOoSklpZXYubdxY8RAIAXjQUu9nzauI6nlO4DnpEXEldABzUk/VmfDc7FzfvGJ2lWKr60MjVaQDAPlxJXcCLChXQG/XaTESMp64DDuvew8dx7YefjdFSGOP/NJK6hJ5rL3N0dRoA8AbjrQxaGIUK6FHgdfewX+1FVFXqpld9jLqoxk6NVOr3pn11musQAYADuJy6gL0KE9BbB/Qvpa4DOqVK3fTB48csIyugD9+dSF1CzzxYWnF1GgBwGJeKtCyuMAE9CvbkAjqh3U3//sZv2XfTL5ybSl0Ce7z39ulKPDRpf4397dZ89l9jAEDXXE5dQJuADj2wtLyafXfvxNBgfPnpR5UaqS6qE0ODleie376/WJkpFQCgqy6nLqCtEAG9Ua9NR8TZ1HVAN7XPx+bcTW+H9OmpidSlVNZAf1989vEHMdBfxFs0O+PJejOu/fBzzM0vZvu1BAD01NlWJk2uEAE9Ir5OXXcUVLAAACAASURBVAD0Su7d9IH+vvjw3Yn48tOPKjFiXSQD/X3xxYXpbKcYtrZ3nnbNXZ0GAHRYITLpP/z9739PWkDrQP5i7F4UD0d2+/5izM0vpi5jX8ZOjcSFc1NZdzvL9PtRZieGBuOLC9PZ/llaWV2L2VvzpdnOPj01UYljBgCQkfWImDj51udJz84VoYP+VQjnVFS7m/5gaSV1KV2jm9597719OttwvrW9EzfvLLg6DQDotqHYzaZJFSGgX05dAKS0tb0Tf7s1n3UAcTa9OwaPH4svLkzH+TOTWYbz9gOsew8fpy4FAKiGy6kLSDri3qjXJiLi/01WAFkq80j1QH9fTE9NxPuTp1OX0jVlG1UuqvfePh0fvjuRZTDf2t6J2Vvzpd7TYMQdAErr/z751ueLqV48dQf9cuLXh0LZ2t6Jn37dHefNdQnW6MhwfPnpRzF2aiR1KaWUe9f87sLjrJcoAgCFdznliwvoUEArq2tx7Yef4/b9xdSldEX7KrB/+efJ1KWUyntvn44vP/0oRkeGU5fScc2Nzfhudi5++nXB1WkAQEqXU754soDeqNdmImI81etDGczNL8Zf/nojVlaTLpPsmvcndwNnjp3gTmo/0Mi5a37th5+z/XMOAJTKeCurJpGyg3454WtDabQ7izfv5NlZPDE0GP/2rx/b8v4K7QV7OR4JeLLe1DUHAIrocqoXTtmKSb7CHsrk3sPHsbC0EhfOTWUX1gb6++LLTz+K2VvzsZDxlXMH9d7bp+P8mTyPAZR5meN+DP4fx1KXAAAcXrKsmqSD3qjXLoe7z+HAtrZ34vsbv2V7JduFc1Pxybmp1GUkN9DfF5+cm8oynD9Zb8a1H37OOpxHRPyfxwV0ACixoVZm7blUI+6653AE7SVydxfyux/6nbHR+OzjD7I8a70fA/198cWF6XhnbDR1KR13+/5iXPvh52xvKAAAspIks/b8HvRGvTYcEf9fT1+USsl9dPZFJ4YG48K5qezOcLfPJ1fpbPKJocH44sJ0dg8nVlbXYvbWfJZTH6/yxYXpLLftA0DF/F8n3/q8p1tsU3TQLyd4TchWe2T49v3FrMJsO6zm9uDhVUZHhrML51vbO3HzzkK2RzIAgOxd7vULCuiQibn5xeyuqqpKSJ8cG80unLePYdx7mN8xjP34bw8kACAHl3v9gj0N6I16bSIizvbyNaFKcrySrX0mO9eQPjk2GhcyWoyna76r+T/V/X8HgIycbWXYnul1B91yOOiBew8fx1/+eiOWlldTl9IRuYb0994+nVU4r3rXHADIUk8zbK8D+uUevx5UVvtKtu9v/JZFNz23kJ7TNWq65gBAxi738sV6FtCNt0MaS8ur2XTTcwnpn5ybyuYaNV1zACBzPR1z72UH/esevhawR07d9LKH9OmpiSzCua45AFAhPcuyvQzozp9DYrl008sa0ifHRuPDdydSl3FkuuYAQMX0LMv2JKA36rXpiBjvxWsBr5dLN71sIT2Xbe265gBABY23Mm3X9aqDfrlHrwPsUw7d9HZIHzx+LHUpr5VDOH+y3tQ1BwCq7HIvXqRXAd14OxRQDt30gf6++OzjD2Kgvy91KS91Ymiw9Nvab99fjGs//BxP1pupSwEASKUnmbbrAd14OxTf0vJqXPvh51hZXUtdyqGcGBqMLy70ZOroQNp1FfXhwZu0u+Zz84upSwEASK0nY+696KBf7sFrAEfU3NiM72bn4uadhdSlHMqJocH4pEBj5AP9fXHh3FRpw/ndhce65gAAz7vc7RfoRUA33g4lcu9heYPZO2OjMT01kbqMiIj47OMPSrPAbq/2g5qffi3ngxoAgC7qerbtakBvXehuvB1K5sl6M76bnYsHSyupSzmwD9+diMnE94x/cm4qRkeGk9ZwGGU/6lAkfg0BIEvjrYzbNd3uoOueQ0ltbe/E327Nl3KB3Pkzk8m615Njo/FO4gcEB7W1vROzJf29BgDosa5m3G4H9Mtd/vxAl7W7qmUaeU+12b2MG9vb0xILJZyWAABI4HI3P3nXAnqr9X+2W58f6J3mxmZc++HnuLtQnjuwB48fi88+/qBnr1f0695e5sHSSnw3O1eqhy8AAImd7eaYezc76MbbITM//boQs7fmSzMGPToy3LOlcRfOTcXg8WM9ea1OuHlnIf5Wot9LAIAC6VrW7WZAn+ni5wYSWShZ1/XDdydi7NRIV1/jvbdPd/01OmVreyeu/fBz3HtYnmkIAICCmenWJ+5KQG/Ua8MR8WU3PjeQXvvc8tLyaupS9qWb3e0ynTt/st4s3T4BAIAC+rKVeTuuWx104+2Qua3tnfj+xm+lOJc+0N8XF85NlebzdsPS8mp8NzsXzY3N1KUAAOSgK5m3WwF9pkufFyiY9rn0ouvGefTpqYlk17kdxIOlFVeoAQB01kw3PqkOOtkp0xbtXLTPpRc9AH74bucC9ejIcLw/ebojn6ub2svgAADoqHJ00Bv12kxEDHX688J+/eNw8TuaOVpZXStFSO/EVWhlGW2fvTVvGRwAQHcMtbJvR3Wjg657DhVVhiVkg8ePHXnUfXpqovBXqs3emo+FpZXUZQAA5Kzj2VdABzqqubFZ+GvY3p88HaMjh1u8WfTR9q3tHeEcAKA3ih3QG/XaRESMd/JzAuWztb1T+JB+4dzUgUfdiz7a3v51F84BAHpivJWBO6bTHXTdcyAiih/SDzPq/t7bpws72l70X28AgEx1NAN3OqDPdPjzASVW9NB4kFH3E0OD8eG7E90t6Ahmb80X9tcZACBjM538ZJ0O6F92+PMBJVf0kH7+zGRHf1wKs7fmY2l5NXUZ7HHYHQcAQOl0NAN3LKA36jXj7cBLtUN6c2MzdSm/c2Jo8I2j7pNjo4UNXBbCAQCk1cks3MkO+kwHPxccWlHPCFfd1vZOfH/jt0Lek/7+5KvPlg/09xW2e37zzoJwDgCQ3kynPlEnA7oOOoUgoBfXk/VmfDc7V7iQ/rrt7NNTEwfe9t4LD5ZW4t7Dx6nL4BWK+GcGAOiaYnXQXa8G7NeT9WbcvLOQuozfGR0ZjrFTI8997MTQYCHvPF9ZXYu/3ZpPXQav8Y/Dg6lLAAB6p2PXrXWqg657DuzbwtJKIUP6i6PsRbzz/Ml6M76/8VvqMgAAeF5HMnGnAvpMhz4PdERRF3rxzL2Hj+NBwc5P770bfXpqIk4MFasLurW9E7O35gt3RIDfK9qfHQCg62Y68UkEdCCZn+4sFO76tfcnTxd2tN1d5+XhDDoAVM5MJz7JkQN6o16bjoihDtQCHePNcTkUcbP7QH9ffPnpR4X7M3T7/qK7zkvCokoAqKShVjY+kk500J0/p3CMl5ZHc2MzZi08e62V1bWYm19MXQb7JKADQGUdORt3IqDPdOBzQEcVrfvJ6y0tr8bdBVeGvUx7yoDyENABoLJmjvoJOhHQL3bgc0BHueKofH76tXjn0YugaEcAeDMBHQAq68jZ+EgBvVGvzRy1AOgGHfRysqH8eXcXHsfK6lrqMjggDwgBoLqOmpGP2kF3/pxCcga9nJ6sN+P2/cXUZRTCk/Wmc+clpYMOAJV2pIx81IA+c8SfD10jpJfTvYe6xhGmCcrM9x4AqLSZo/zkQwf0Rr02HBFnj/Li0E3G3Mur6lvd7y48dh6/pIRzAKi8s62sfChH6aDPHOHnQteNjhz664LEmhublR11b25sGm0vMQEdAIgjZGUBnWxZ1FRuc/OL0dzYTF1GzxltLzcBHQCIRAF9+gg/F7rOoqbyq9qo+9LyqvP3JefBIAAQR8jKRwno7j+n0HSyym9ldS2WlldTl9EzN+8spC6BI3K0BgCII2TlQwV0959TFt4sl19VQuvt+9Uc6c+Jh4IAQNthM/NhO+iHejHoNQG9/Jobm3F34XHqMrpqa3sn7j3M+/+xCny/AQD2mDnMTxLQyZrzoHmYm1/MenHazTsLWf//VcWpkwI6APDUzGF+0mEDuvPnlIKOVh62tney7aI3NzZjYWkldRl0gO83AMAeh8rMBw7ozp9TJgP9fc6FZuLew8dZdpmret97bk4MDcZAf1/qMgCAAjlMdj5MB931apSKrlYecuyi657nw/cZAOAlDpydDxPQZw7xcyAZ50LzkVsXXfc8H+P/NJK6BACgeGYO+hN00Mne2ClvnHOxtb0TDx7l0XHWPc/HQH+fDjoA8DLd7aA36rWJiBg/6ItAakJ6PnK5jiy3cf0q8/0FAHiF8VaG3reDdtB1zykl3a18NDc240HJO89b2zu65xkZdYwGAHi1A2Xogwb0mQP+eCgE50PzslDyMfcHj1ayOktfdeM66ADAq80c5AfroFMJg8ePuW4tIyura9Hc2ExdxqHlMqbP7ni769UAgNfoagf9UJetQxFMjo2mLoEOKusZ7rI/XOB574z7vgIAvNaBMvS+A/phLlmHIjHmnpeynuHOZQs9u9vbLYgDAN7kIFn6IB104+2U2uDxY5bFZWRreyeWlldTl3EglsPlRTgHAPZp31laQKdSJo2jZqVs3eiy1cvrvT95OnUJAEA5COjwMuMWOmVlaXm1VNvQdc/zcWJo0OJJAGC/uhLQzx6iECgUZ0bz86gkY+7Njc14st5MXQYd8p7uOQCwf/vO0vsK6BbEkRNjqXlZ+s9yBPRHJamTNxvo73P3OQBwIPvN1PvtoBtvJxsnhgYti8tIWcbcjbfnY3Js1FEZAOCg9pWpBXQqybK4vKysrqUu4bWMt+fFFA4AcAgCOrzKO2OjMXj8WOoy6JCij48XvT72b9L3DgDgcDoa0C2IIzvvva0Llouid9CLXh/79+G7E6lLAADKaV+Z+o0B3YI4cvXOuHOkuSj6CPlSSTbN83qjI8O65wDAoe0nW++ng268nSwN9PfpomdkuVHMLrXueT50zwGAI3pjthbQqbT3J0/romeiqEG4qA8OOJixUyNufwAAjqojAX3i6HVAMemi56OoAb2odXEw589Mpi4BACi/iTf9gP0E9ItHrwOK6/3J086VZmBre6eQ59AF9PKzuR0A6JA3ZuvXBvRGvWa8newN9PfFtLOlWfivggX0Ij4w4GAG+vucPQcAOuZNGftNHfSJzpUCxfXO2GicGBpMXQZH9GStWIG4aA8MOLj33jZhAwB01MTr/uObAroOOpXhjGn5Fa1jXbQHBhzM4PFj8f6kHRUAQEcdqYMuoFMZoyPDMTk2mroMjqBo572L9sCAgzl/ZtItDwBApwnosF/ekJdfkUJxkWrhYMZOjcTYqZHUZQAA+TlSQB/vYCFQeAP9fTE9NZG6DI6gubGZuoSI2N0qv7W9k7oMDmGgv8+RFwCgW16bsV8Z0Bv12kzHS4ESeH/ydIyODKcug0P6r4Kc+9Y9L6/pqQmL4QCArnld1n5dB32i45VASVw4N2XUvaSKEoz/uyCdfA5mdGTYYjgAoNsmXvUfBHR4icHjx4y6l1RRxsqb/yOgl81Af19cODeVugwAIH8Tr/oPrwvoMx0vA0rEqHs5FWWTe1E6+ezfv5yZNNoOAPTCzKv+gw46vMZnH39g1L2EitBFL0IN7N/YqZF4xzWLAEBvTLzqP7wuoNvgTuUN9PfFZx9/kLoMDqgI3euibJPnzQaPHzPaDgD00iuz9ksDeqNec/85tIyODDuPzoEJ6OVhUgYA6LVXZe5XddAnulcKlM+H7044j14iy41inEOn+D45NxUnhgZTlwEAVM/Eyz74qoCugw4v+OzjD7yRZ1+KMGLPm02OjTp3DgCkooMOR9G+gskobPGlXtCW+vV5sxNDg86dAwApTbzsgwI6HMCJoUFL40pAB5vXGejviy8uGBQDAJKaeNkHjbjDAY2ODMcnOm+8xn9bEFdY7XBuEgYASOxAI+5DXSwESu+dsdF47+3TqcugoJr/I6AXlV0SAEBBvDRz/y6gN+q1ma6XAhk4f2YyJi2YKiQj7rzMJ+em3MYAABTGy7L3yzro3r3APl04NyWkF5Albbzok3NTNrYDAEXzu+z9soDu/DkcgJAOxeY6NQCgoH6XvV8W0Ce6XwfkRUhnr6YlcYUxOTbqOjUAoKgmXvyAgA4dIqTTJqAXg3AOABTcxIsfENChg4R0KAbhHAAogYkXP/CygD7e/TogX0I6pCWcAwAl8bvs/VxAb9RrFsRBB1w4N+WedEhAOAcAyuTFDP5iB90Va9Ah589MxieCQjLuQq+eT85NCecAQNk8l8FfDOg66NBB74yNxmcffxAD/X2pS6kcd6FXi3vOAYCS0kGHXho7NRJfXJiOwePHUpcC2Rno74svLkwL5wBAWb22gz7RuzqgOk4MDcaXn34UoyOegUGntMO5rysAoMQm9v6LgA490g4TlsfB0Z0YGox/+9eP48TQYOpSAACOYmLvv7x4MHYigK46f2YyTgwPxk93FpyThkOYHBuN82cm7XYAAHIwsfdfXnx34w506IF3xkbjH4cGY/bWvG3jcAD/8s+T8f6kKRQAIBvPZfCnI+6Nes0hPuih9rl0I+/wZu0jIsI5AJCbvVl87xl0V6xBAufPTMYXF6aN68IrtM+bWwYHAGTqaRZ/cUkckMDoyHD8279+HGOnRlKXAoXy3tun48tPP/IACwCoBB10KIiB/r747OMP4pNzU8IIldceaT9/ZjJ1KQAA3fY0i+9NAWYHoQDeGRuNUyPDMXtrPlZW11KXAz03dmokLnhQBQBUx0vPoE/0vg7gZQaPH4svLkzHv/yzq6SojoH+vviXf56Mzz7+wJ97AKBKJtr/0PeyDwLF8P7k6Rj/pxHddLI3OjIcF85NxeDxY6lLAQDotYn2P2hRQMG1u+l3Fx7HT78upC4HOmqgvy+mpyZcnwYAEM8HdEvioMDenzwdp07unk1/st5MXQ4cma45AEBEvGJJ3FCCQoADODE0GF9++lHcvr8Yc/OLqcuBQxno74sL56ZcKwgAsOtpFv9DRESjXrPBHUrkw3cn4stPP4rREV+6lMt7b5+Of/vXj4VzAIA92pm83UE33k5WZm/NR3NjM8ZOjcQ746NZboQ+MTT49Gz63PxibG3vpC4JXunE0GBcODcVJ4YGU5fSFQ+WVmLh0UpE7B5H8QACADig6Yi4nl9qofKWlldjYWn3jfLK6lrce/g4zp+ZzPYNs03vFFnuS+C2tnfi+xu/Pfe1t7K6Fp+cm4p3xkYTVgYAlFH7HnRzsmTjv9aeX6DW3NiM72/8Ft/f+C3bLrN704ulubGZuoRCGDs1Ev/2rx9nG86bG5vx3ezcSx+MtbvpAAD7NBzxLKAbcSd7S8ur8Ze/3oil5dXUpXTN+5OnnU0vgKoH9PYDo88+/iDbB0Z3Fx7HtR9+dqMCANAp0xHuQadi2uOoY6dG4sK5qSzDQzscPVhaiZ/uLGQ7NUAxTU9NxIfvTqQuo2uaG5uOkwAAXdNOJ9ptZOPUyeGYm3/9j2l303O+6umdsdEYP7V7Nj3nqQGKoQp3mt++vxj3Hj720AsA6AZb3MnTi2fQX6XdTc85WAz098VnH38QS8urMXtrXrCg4wb6++JfzkxmvRDtyXozZm/NH2ic3TETAOCAjLiTp4OG0JXVtbj2w89Zb5puL+tqdwChE3I+KtJ2+/5izM0vpi4DAKiIfN9VwQFsbe/ET78uxNLyatbd9PNnJp9eyVb1RWYc3uDxY3Hh3FTWXeKV1TVfJwBAzxlxhz1WVtfiL3+9kfWiq9GR4fjy04/i7sJjnUEO7L23T8eH705k2zXf2t4xaQIApPDciPtQwkKgcObmF2NpeTXOn5nMsks40N8XH7478bSb7qoo3uTE0GBcODcVJ4YGU5fSNUvLq3HzzoKuOQCQwlCEEXd4pSfrzfhudi7rjuGJocH48tOPbKfmlQb6+55+DeRqa3vHbQcAQCHklzigw+49fPy0m57rlWwfvjsR74yPut+Z5+R8w0GbGw4AgCLpa9RrM6mLgKJrbmzG9zd+y3pr9eDxY/HFhel4sLQSP91ZEFgqbKC/L+tbDSJ2v6Y9kAIAiqRRr83klzKgi5aWV58ukcs1vLwzNhrjp0aM/FZUzg+h2toLEj2EAgCKJt93YNAlVbmS7bOPP7A0q0IG+vviwrmpbI9xROzulbh5Z0HXHAAoLAEdDqkKV7KNnRqJ0ZFh105lbnJsNM6fmcy6a377/qJrBQGAwusLd6DDkczNL8bC0kpcODeV7ZVs589Mxvg/jcTNOwuuZMvI4PFj2f65bXuy3nSVIABQFtN9EZHvOzPokebGZvZXso2ODD+9kk0nsvxy/rMasXsUxeQHAFAyw3m+M4NE7j18/LSbnutZ3g/fnXjaTXeWt3yq0DVfWV2L2VvzdicAAKUjoEOHbW3vxPc3fsv6DukTQ4PxxYVp27BLpn37gK45AEAx5fkuDQpgZXUtrv3w89NR4hy9P3k6xv9pxH3SBXdiaDAunJuKE0ODqUvpmqXl1Zi9Ne9hEQBQapbEQRdtbe/E3Pzi0yvZcgxIg8ePxRcXpuPB0kr8dGdBQCqYnG8ZiNj9Gpu9NR9Ly6upSwEAOCpL4qAXnqw3n+um5zhi/M7YaIyfGhGWCqIKXXMPhQCAzFgSB7107+HjWFpejfNnJrNcIjfQ3xefffyBcePEcu+aNzc2HasAALIkoEOPNTc24/sbv8XYqZG4cG4qy2762KmR+Ld//Thu3lmIhaWV1OVURs6LCdssJgQAcpZfMoCSWFpejb/89cbTzdq5GejviwvnpuKd8VFXXnXZQH9ftn+O2p6sN13tBwBkT0CHhLa2d+KnXxeeLpHLsfM5OjIcX376keuvuqQKXfPb9xdjbn4xdRkAAF0noEMBrKyuPe2m53h2eKC/L86fmXx6JZtu+tFVpWs+e2s+nqw3U5cCANATfRFxMXURwK72lWznz0zG6Eh+FyzopndG7l3zre2dp2fNAQAq5KIOOhTMk/VmfDc7l+2VbO1uevtsuu7o/rXP9ed4A0DbyuqaKQsAoLLyeucPGWlfyXbh3FSW3fQTQ4NPu+k6pW+W89b/iN2uuckKAKDq8nynB5lobmzGd7NzWYezD9+deHo2XTf993TNAQCq4w+pCwDerH0l29LyaupSuqLdTZ+emkhdSqG075PPNZxvbe/E9zd+i+9m54RzAIDQQYfSaIeZsVMjcf7MZJYLwj58d+Lp2fQy33c9OjJ8pPoHjx/L9mhD29Lyaszemo+t7Z3UpQAAFIaADiWztLwaK6tr2V6xNXj8WHxxYfrpFu+qBbhclwO2bW3vxOyt+WynQQAAjiLPd4CQua3tnfjp14WnS+Ry7Ka/P3n66dn0MnfT90vXHAAAAR1KbGV1La798LNuesEc9IFC+/cv1655c2OzMg9aAACOIs93g1AhuunldWJoMC6cm4oTQ4OpS+masj1cAQBISUCHTFSlm170Men9PkCYnpqID9+d6G4xCemaAwAcnIAOGalCN7199VhZF42Njgxn+3vTpmsOAHA4AjpkKPdu+kB/X3z28Qev7aanOs/9uuCtaw4AwOv8IXUBQHe0u+nfzc5Fc2MzdTld0e6mj50a+d1/S3Wue/D4sXjv7ecfigz098Un56ayDue37y/GtR9+Fs4BAI5ABx0y1+6mXzg39dIgW3btbvrK6lrM3pqP5sZm8qVr589MxonhwXiy1oyB/r54Z3w025H2J+vNmL01H0/Wm6lLAQAoPQEdKmBreye+v/FbjJ0aiQvnprK8zmt0ZDi+/PSjuH1/sRATA++MjUaMpa6iu27fX4y5+cXUZQAAZCO/d+nAKy0tr8Zf/noj6276+TOTlpN1ma45AEB3COhQMe1u+ntvn44P353Ispue4/9TUeiaAwB0j3exUFH3Hj6OpeXV+OzjD5Kf2ab4dM0BALpPQIcKa25sPr2OLecN4xyNrjkAQG8I6EDMzS/GyupaXDg3le22cQ5O1xwAoLfcgw5ExLPr2JaWV1OXQgG07zUXzgEAekcHHXiqvUBucmw0zp+ZtGytgnTNAQDS8e4b+J2FpZV4st6MC+emLJCrkLsLj+OnXxdSlwEAUFlG3IGXerLejO9m5+LB0krqUuiyre2d+G52TjgHAEhMBx14pa3tnfjbrflY+s/VuHBuysh7hpaWV2P21nxsbe+kLgUAoPJ00IE3Wlpeje9m55xLzszNOwvx/Y3fhHMAgIIQ0IF9MfKej/ZI+72Hj1OXAgDAHuZVgX1rj7yvNNZseS+p9oMWXXMAgOLx7ho4MFvey+nB0kr8dGdBOAcAKCgj7sChtDuxS8urqUthH27eWYi/WQYHAFBoAjpwaFvbO/H9jd/i9v3F1KXwClvbOzF7a955cwCAEvhDRPyYugig3ObmF13VVUDtZXALFvsBAJTBjzroQEcsLK1YPlYg7XDuajwAgPIQ0MmOzeLpPFlvxrUffhYKE3uy3oy//PWG3wcAgJIR0MnOPw7bKp5Sc2NT5zYh16gBAJSXgA50nPHqNIRzAIByE9CBrmiH9JXVtdSlVIJwDgBQfn+ICO+ega5oh/QHtoh3lXBePI7aAACHsPaHiJhLXQWQt7/dmjfu3iXCeTFZVgkAHMKcEXegJ5xJ77yt7Z34/sZvwjkAQCYEdLKjc1VMFsd1VvvXs7mxmboUAAA6REAnOyeGnP0sKqGyc76/8ZuHHQAAmbEkDugpY9lHN3tr3nZ8AID8WBIH9N6T9WZ8f+O31GWU0t2Fx7FgK37hjY4Mpy4BACgfS+LIkzH34ltZXYvZW/OpyyiVpeXV+OnXhdRlAADQJQI6WbIorhwWllbckb5PzY1NDzQAADInoANJuSP9zZzbLxcTPADAYf3h5FufX09dBHSa85/lIny+3s07Cx5ilIgJHgDgME6+9fl1HXQgOePbr/ZgacVSuJIR0AGAwxLQydI/DhsxLZul5dW4u/A4dRmF0tzYjJ/uWApXNkbcAYDDagf09aRVQIfp8qSrUAAAIABJREFUYJXT3PyiUe49Zm/NG/0vId9/AIBDWI94FtDdhU5WdLDKaWt7x6h7y92Fx7Gyupa6DA7BBA8AcAhzEUbcydRAf58uVkk9WW/G7fuLqctIqrmxGXPzi6nL4JAGjx9LXQIAUFICOtnSRS+vew8fR3NjM3UZyRhtLzcBHQA4LCPuZMub5PKq8qi70fZyc8UjAHBIz424ezdIdnTQy21ldS0eVOx6sa3tHaPtJefBIABwSGsRRtzJmEVN5Td3f7FSo9437yxU6v83Rx4MAgBHYcSdbHmjXH7Njc3K3I3+ZL0ZCxWbGMjRqZNG3AGAQzHiTt4G+vuMm2Zgbn6xEgvjbt5ZSF0CHeDBIABwSEbcyZ+FTXnI/dq1ldU1i+Ey4PsNAHBURtzJmm5WHhaWVrLuold1Y31uBHQA4AiejbiffOtzrRuy5DxoPnLtoj/I/OFDlYz/00jqEgCAkmpnciPuZO3E0GAM9PelLoMOyLWLPpfpg4eqGejvM7EDABzWevsf9gb0HxMUAl1n7DQfuXXRdc/z4fsMAHAET4+c66CTPW+c85FbF133PB9jxtsBgA7YG9AXUxUB3eRcaF5y6aKvrK5l9bCh6sZP+T4DABzaYvsfBHSyN3j8mPvQM7K0vBpb2zupyziyXB40YNcFAHBki+1/MOJOJYzpbmVja3snHjxaSV3GkTQ3Nt17npHJsdHUJQAA5fb0jeHegH6993VAb7huLS/3Hj5OXcKR6J7nxTEaAOCILImjWsZOjRhBzUhzYzOWlldTl3EoW9s7pa2d3zsxNOgIDQDQMXsD+twrfxRkwJh7Xh79ZzlD7qNMztCzy3g7ANABv++gn3zrcwciyZox1LwsLK2UMujeWyj3eD7P830FADiqvVn8xRH3Rz2uBXrGmHt+HpVsVLy5sRlP1pupy6BDxk6NGG8HAI7quQz+YkBf7F0d0HvGUfNStm703ZLVy+uN6Z4DAEe3uPdfXgzoxtzJ2jvjAnpOnqw3o7mxmbqMfbMcLh8D/X3xjgd+AMDRLe79lxcDukVxZO3E0GCcGBpMXQYdVJZlcWV7mMDrmcYBADpkce+/6KBTOe9Nnk5dAh20sLSSuoR9efCoHHWyP+/7PgIAdMZzGVwHncoZtywuK0/Wm6XY5r6y6vlnLkZHhi2HAwA65bkMroNO5Qz097kTPTNF3+Zue3tedM8BgA56dQf95Fuf66BTCR++O5G6BDpoqeDn0MtyTp43Gzx+zAM+AKBjXszgL3bQIyLWe1QLJDN4/JglTxkp+vh40etj/6Y93AMAOufRix94WUDXRacSXLmWj63tnUKPkAvoeXC1GgDQYYsvfuBlAf13PwhyNDoyHKMjw6nLoEOKOkZeliV2vNl7bzt7DgB01OKLHxDQqTRn0fNR1C71cqOYdXEwA/19lsMB/z979x4d91nf+/4jjWY0lkYa3UYe2ZIs23IsX+LY2ImNQXV2AkVOF8vksMIJNAuS0xygp9BCC+xy2wktUJrVFJfdrg2rTQndlEUOi9ZZZ9OYDaQOTogT4vgax7ElRZbkSLYu1tW6jTTnD2kUJbaluT+/y/v1D8EX6dM0Dvro+zzfBwDSre3tP8ARd7gaU3TnsOoRd6t+4wCJ2bi2mucZAQBAul3Tva9X0PlqEq7CFN0ZrHoPnYJuf0zPAQBAhlzzhSITdLheuKKEje4OYbXj5CNXx7l/7gC3balneg4AANIuVNN06O0/dk1BD9U0WesrXCALmKI7g9Um6FbLg8QFCvxsbgcAAJlw3efNrzdBl6RnMhgEsJxAgV9bG+pMx0CKrFaI+waslQeJ27ml3nQEAADgTNc9uX6jgt6WuRyANW2qr1agwG86BlJgtYLO/XN7C1eUqLaqwnQMAADgTG3X+0EKOjDH581jWuYAVirpI1fHTUdAChq3N5iOAAAAnKvtej94o4LOoji4Um1VBc+u2VwfBR1psLWhjhM1AAAgkzjiDsSjcXsDG5ttbGTUGqWY4+32FSjw86waAADItLbr/eB1C3qopokJOlyLhXH2ZpViPMz03Lb4Jh0AAMi0G3XuG03QJelChrIAlrepvpqj7jZllXfHrTLJR2I2ruXPPgAAyLgbdu3FCnpb+nMA9nHnrs1M0WzIKkviuH9uP4ECv7ZtqDMdAwAAOF/bjX5isYJ+KO0xABvxefPY4mxTVpiiU9Dth6PtAAAgSw7d6CeYoAOLqK2q0Ma1LIuyGytM0a3wTQLEb2tDHUfbAQBAtrTd6Cco6MASdm6pV1kwYDoGEmCFcmyFbxIgPmXBAEfbAQBANrXd6CduWNBDNU2HMpEEsCPuo9tL3wDlGPHxefN0567NpmMAAAAXWaxrLzZBl9jkDkiaXR7FF/GIF9Nz+7hz12YFCvymYwAAAPdYtGMvVdDb0pcDsLdwRYnezdI4WzBdkK1wxB5Lu+3meu6dAwCAbLvu++cxSxX0Q+nLAdjfutqw6mvDpmNgCRRkLKW+NqxN9SyABAAAWZdSQV/0NwNu1Li9gZKORXEH3trKggGeUAQAAKakVNDb0pcDcA42u1ub6TfImeBbV1kwoL2NW03HAAAA7tW22E8uWtBDNU1M0IHr8HnztLdxKyXdokwXdFhTbGM7LzIAAABTlurYS03QJemZNGUBHIWSjhthgm49sT+vbGwHAAAGLdmt4ynobannAJyJko7rMb1FHm/Fn1MAAGARbUv9gngKOsfcgUXwxT9gXfz5BAAAFrJkt6agA2lACbAe7qGDP5cAAMBiUi/ooZqmQ2mJAjgcZcBaKOjuxp9HAABgNfF063gm6JJ0IbUogDvESkG4osR0FBjEkjizKOcAAMCCTsTzi+It6BxzB+IUKwf1tWHTUWAIS+LMKQsGdM/7dlHOAQCA1cTVqSnoQIY0bm/Q1oY60zEA1whXlGhv41beOQcAAFaU1oJ+KPkcgHtt21Cnd29voDAAGVZfG6acAwAAK4uroMf7lQwTdCBJ62rDKg8G9Ksjp1lcBmTAu7c3aB1XSgAAgIXFu3w9rgl6qKZpQHFeagdwrbJgQPvu2MHyOCCNAgV+7btjB+UcAABYXdxdOt4j7hJTdCAlseVx3EsHUldbVaF9d+xgGRwAALCDuLs0BR3Ism0b6rS3casCBX7TUQDb8XnzdNvN9bpz12bumwMAALugoANWFq4o0b47dqi2qsJ0FMA2yoIB7W3cqk311aajAAAAJCL9BT3eS+0A4uPz5unOXZvZ8u4wk1MR0xEcaWtDHUfaAQCALSXSpROZoEvSMwn+egBLWFcbpng4SP/giOkIjhIo8Gtv41Zt21BnOgoAAEAyEurQiRZ0jrkDGRDbRs0COeBN9XPfvOL1AwAAYGMJdehEz9VS0IEM2rahTqtWVPBmOlzN581T4/YGdjQAAAAnOJTIL050gp7QBweQuNib6RvXsggL7lNbVaF73reLcg4AAJwioSF3QgU9VNPUJmkwkd8DIHE+b552buEpKbiHz5und29v4J95AADgJBfmOnTcEp2gS0zRgaxhmgg3iD07uK42bDoKAABAOiV8RZyCDlgcz7HBqXzePN12c732Nm5VoMBvOg4AAEC6HUr0NyTz1T6L4gAD1tWGVVVRosNHz6q7d8B0HCAl4YoSNW5voJgDAAAny/wEPZFH1gGkV+xN6NturmeaDltiag4AANwime6czBF3KcHH1gGk16b6at6Hhu2UBQPa27hVm+p5oQAAADheUp052RHcIUl7kvy9QMadb+/W8VfbJElbN9Q5cvlUbJr+SnOnjp9t0+RUxHQk4Ia2NtRp24Y60zEy6nx7t5ovdCtQ4Ffj9gbTcQAAgFmHkvlNqRT0h5L8vUBGdfcO6NmjZ+f/+7NHz6q7Z8CxXzBvqq9WVWj2bnr/4IjpOMBblAUDatzeoLJgwHSUjOnuHdDho2c1cnV8/sfCoRJHfmMQAADE7VAyvynZgs6iOFhWV8+1C9Sa27s1ORVRo0M3oZcFA9p3xw4de7VNx8+2mY4DSHL+1HxyKqJjr7bpTEvnNT83Mjp+nd8BAADcItndbUndQQ/VNA1IOpHM7wVMae/q1U9+fkTtXb2mo2TMtg112nfHDkdPK62Ov/dvfsPIyeW8u3dATz790nXLuSROswAA4G5J72xLZZR4SNItKfx+IOsmpyL61ZHTqq2q0M4t9Y7cIs003SwnntCIl8+bp41rqx1dzCenIjp89OyS3+hz8z8HAAAg+RPnqRb0P0nh9wMZUV6y9ASzvatX3b0D2tpQ59iN0ts21GnVigrupiMr3PCueXtXrw4fPRvXQkYn/30AAABLOpTsb0y1oAOWE+/kanIqohdPNau9q1c7t9Q78mhybJrOpndkis+b5+hvdEnxT80BAADmHEr2Nyb7Djr30OEYsbukx+aeZXMi3k1HJoQrSrTvjh2OLudu2F0BAADS6sRcV05KqpfkDol76HCI42fb1NzercbtDY4ssrybjnRxw9R85Oq4Dh89q+7epP/3FQAAuNOhVH5zOgo699DhGCNXx/XU4ePzi66cuOhpU331/N10ygcS5Ya75nwTCwAApOBAKr85pfYRqmk60NNxMJUPAVjSmZbO+bvptVUVpuOkHdN0JMrnzVPj9gZH/nmIYWoOAABSlez75zHpGA8+I2lPGj4OYCkjV8fnn2Rr3N7g2Gn6ulVhFmBhUU7+MxDDN6sAAEAaJP3+eUw6vto6JAo6HCy2JMqpd2593jzduWtzQk9IwR3cMDXvHxzhKUIAAJAuh1L9AElvcU9nCMDqYk+yPXX4uGO/kK+tqtA979vl6DKG+G1cW+34fx6OvdqmJ59+ybF/pgEAQNaldP9cSkNBnztjP5jqxwHswOlPssWm6Xsbtzp6CRhuLLafYOeWesceae8fHNGTT7+k42fbTEcBAADOMRiqaTqe6gdJ11dfhyTtS9PHAizP6U+yxd63PvZqm860dJqOgyxx8usFMcdebaOYAwCATDiUjg9CQYfj9A1k57iq059k83nztHNL/fyTbCNXx01HQoaUBQNq3N6gsmDAdJSM6e4dcNQ/x3njrcqZXvzfdVFPQBH/miwlAgDA9Q6l44Okq1EckPTtNH0sICXZXnJ2pqVzfpruxPu64YoS3fO+XUweHWprQ522bagzHSNjJqciljwJkjM9qrzxFklvLdt5463KmXmzeHtHT2Xk808V3jz/19HcN4v8wlIf8a9V1FOYkc8PAIADpXz/XEpTQQ/VNLX1dBy8IGlVOj4eYDeTU5H5J9l2bql35P3tbRvq5qfpLNWyv3BFiRq3Nzjyn9UYk1PznOikvKMn5Zm6pNzJS7P/OXVJnslLyp26nPU8b/f24u8bfv6Gv3bGW6lp33LNeJdr2rtcM77Z/6TAAwAw70KopqktHR8onWdyD0n6WBo/HmA77V296u4dcOyTbGXBgPbdsYM3o23M581z7D+fMVaYmi/r/YmC0WeNff50yp26PPdNhWun+VFPoSL+NYr412rGu3z+rynuAACXScv0XEpvQT8gCjow/yRbe1evdm6pd+S93k311fPT9O7eAdNxrsvk8r5wRYkl/744+YRHTHtXrw4fPcs3j7IkZ3pU3tFT10zkZ7yVivjXKuJfo6nCLZR2AIDTHUrXB0r3BB3AnNiTbE694xt7jut8e7dePNlMIbIwnzfPsTsSYianIjp89Kzau3pNR4Fmp+6+qcuzR+d7/lXSbGmPlfXZ/2SBHQDAGUI1TdaboIdqmgZ6Og4+I2lPuj4m4AROf5JtXW1Yq6oqKEcWVV8bdvSb5hJTc7vInbqs/IFfKl+/lDR7PH6qYIumCrdQ2AEAdvZkOj9Yur9iOyAKOnANNzzJdueuzY57ysrOAgV+x35TKGbk6rilr1lgcTnTo/INPz+/oC5W2CeL36mpwi2a9i43nBAAgLgcSucHy0RB57k14Abc8CTbvjt2GF/Q5XaxJXBO+0bQQiwqdJ63F/YZb6Umindrsmi2sAMAYFFpO94upbmg89wasDSnP8nm8+Zp55Z6rVpRoRdONvMkWxaVBQNq3N7gyMWEMUzN3SN36rKW9R3Qsr4DinoKNVn0Tk0U79ZUwRYWzgEArCJtz6vFZGK8ckDSn2Tg4wKO4vQn2RZO04+fbTMdx9F83rz56xNOFjuZwdTcfXKmR2fvrw/M3l+fLHqnJovfqYmi3ZR1AIBJaZ2eS5kp6IdEQQfisvBJtsbtDY6bpkvStg1189N0pp7pF64ocew/OzH9gyM6fPSsrU5jTMzkm47gaLGj8AH9rSZK3jN/FB4AgCw7lO4PmBONRtP9MdXTcXBAUjDtHxiIg50ntk59ki0mm/eG73nfLmOl9anDxzP+zQifN8+xpy8Wsuuf55plHbq35kemY7hK7Bj8WPndbIQHAGTDYKimKe3beDO1QeiQpH0Z+tiAYx0/26b2rl7t3FLvyO3bm+qrtWpFRVbuEI9cHXfsVLm2qkKN2xscvQSuu3eAHQZIyMJj8DPeSo2V363xkvdyBB4AkCmHMvFBM/XV3QFR0IGk9A+OOPpJtkCBX3sbt/J2dRICBX7t3FLvyBcAYianIrwCgJTlTl1WYff3VNj9PU2UvEfjJe9lEzwAIN3Sfv9cymxB/36GPjbgCmdaOufvpjtxml5bVaF73rdLh4+eVXtXr+k4lufUb9gs1N07oMNHz2rk6rjpKHCQhVP1q5X3sVgOAJAuGSnouZn4oKGapgFJz2TiYwNuMnJ1XE8dPu7YSbPPm6c7d23W3satjj2OnqrYiYOdW+odW84npyI6fPSsnjp8nHKOjMmduqzAxb9V2fmPqejio/JMXTIdCQBgX8/Mdd60y+RXewck7cngxwdco7m9e36a7sTjzQufZONo85tiS+CcWswlcdUBWbfwrvrsUrkPcPwdAJCojEzPpcwX9G9n8OMDrjI5FdGvjpx27IIwnzdPO7fUzy+Rc/MktSwYUOP2BpUFA6ajZExsas71BpgUe65tqvBmjZXfzVNtAIB4ZaygZ+SIuySFapraJJ3I1McH3Kq9q1c/+fkRvdLszElzuKJE97xvl7Y21JmOknWxp9P23bHD0eX8leZO/eTnRyjnsAzv6CkVt/+Fys59TP6BX5iOAwCwthNzXTcjMlbQ5zye4Y8PuNLkVEQvnmp29J3dbRucX1QXih3z37ahznSUjIntVHjxVDNH2mFJ8/fUKeoAgBt7PJMfPNMF/VCGPz7gat29A3ry6ZccO00vCwa0744djp6m+7x5uu3mescvyjv2apuefPoldfdmZJ8KkFYUdQDAIg5l8oNntKCHapqOS7qQyc8BuJ1bpun3vG+XbZ6b6x8cievX1VZVaN8dO7SpvjrDiczpHxzRk0+/pONn25iaw3YWFnXf8POm4wAAzLsw13EzJtMTdCmDF+gBvKm7d0A/+fkRHXu1zXSUjIg9N3bbzdZ/bmypIhp7Xu7OXZsdOzWfnIrMT83j/YYFYFW5U5dV3P4XCrZ9Qd7Rk6bjAADMyXi3zcZXuY9L+pMsfB4Ako6fbZt/ks2J97c31VfPb3q343Fpp27hX6i7d0CHX3pFI2NTpqMAaeUdPaXg6H/VZNE7NVr1CU17l5uOBADIrscz/QkyPkHnmDuQfbFjxW6eplvtmxMLp+ZOLeeTUxG9eOLV2esWlHM4mG/4eZWeu1+F3d9TzvSo6TgAgOzI+PF2KTsTdGn2KABTdCDL3DJNf+Fk81ue7AoU+I2W4HBFyVum+xvXVmvbhjrHFnNp9vm/wy+d0mQkx3QUSxiMBE1HQBYs6zsg/8AvdDV0n8bKP2A6DgAgs7JydTtbXy0+Lgo6YERsmr61oc6RT3gFCvy6c9dmdfcO6MIbveofHNHOLfVGM22qr1Z374DCFSXatqHONsvtkjE5FdFzL76otsuTkijnMUNTxaYjIEtypkdV2P095Q/8QqPhT2iqcIvpSAAc5mpPnyITk6ZjKL+4SPnFzhv4JODxbHySnGg0mo3Po56Og22SVmXlk8HVjr3apuNn20zHsKSyYMCx03Rk35nzrTr26uuanPaYjmJJn7/pr01HgAETJe/RSPiTinoKTUcBkGHXK85DF7uu+XUTQyOaHBq+7scY7enX9KT58p0uHp9PhaGy6/5cQahcnnzfW34sLz9fBRVlb/sxnwpC5RnLmKQLoZqmumx8omyet+SYO2CY06fpyI6Rq+N67oXn9cZAjiTKObBQ/sAv5Rt+XqPhT2i85L2m4wBYwlDnm4X6am+/IhMT8/99uPOtZXvoYnfWctnV9OTkDf8+pfL3r3hl+C3/vai6av6v84uLlF/05vCpeMHPpVHWXibLZkF/XBR0wBKcfjcdmXPildN6+VyvOM4O3FjO9KgCF/9W+QO/0MjKP2PbO5BFscI9PTGp0d6++b++2jP715GJSV3t7TeWD8l5e7mPt+wXVJQpb25qv3CCX1jx5l/HWegfjzdrqrJ2xF3imDuygyPuiWGajnj0D47ouReeV++o13QU2+CIOyQp6inUWNkHdLXyPtNRANuanpjU6FzBjk25F5Zupx0ThxkLj+fHynxefr4C4dC51bd+dH22cmR7pfB+Sd/O8ucEsAim6VjM5FREJ06f0Om2YUmUcyBROdOjKuj5V/mGn9fIyj9TxL/GdCTAUhaW79j97as9/ZqemNDE0IgmhkdMxoOLLDyev3BCX9FQf2b1rdnLke2CfkAUdMBy+gdH9NTh49raUKdN9dWm48AiunsH9OyLRzU8wT1zIFV5460qafkjXQ39PtN0uEqsgMeOnMcm3xw1h134Cgsezebny2pBD9U0tfV0HDwh6ZZsfl4AS5uciujFU83z0/RAgd90JBgyORXRiVfO6PTr/WIJHJBeBT3/Ku/Vk9xNh6PECndsAj7c2UUBhyP4S4Nj77j3q89m83Nme4IuzV6wZ4oOWFR378D8pnem6e7T3TugZ397TMPjLIEDMsU7ekolLX/EpnfYysISHpuCcwQdThdYHvp5tj8nBR3ANWLT9O7eATVub5DPa+JfFci2F0+8qldaL4kN7UDmxTa9+4ae1/DKP+PddFhC7Dj6xPCIJoaGmYTD9fKLAp/J9ufM6hb3mJ6Ogwck7cv6J4YrsMU9vXzePDVub1BtVYXpKMiQkavjevo3L6tvmA246cQWd8RrxlupodqHWCCHrIkV8au9/ZoYGtbVnj42oQNvU7Qi3L3ns/89I4+qL8bUWIyCDtjE5FREvzpyWvW1Ye3cUs803WHau3p1+KVTmowwNQdMyZ26PH/kfaz8A6bjwGGGOrso4kAS/CXFPzPxeU0W9P2SgoY+P4AENbd3q7t3QHfu2sxzbA7BkfbMqVnWYToCbKiw+3vyjp7kyDuSErsTPtrbp+HOLu6HAynw+LxRX2HBX5r43EYKeqimaWDumPvHTHx+AMkZuTquJ59+SbfdXM8CORubnIro4DMvcqQdsCDf8PMqbfl/OPKORQ11dmlieERXe/p0tafvLW82A0hdIFzZuu1DX75g4nObPKv6uCjogC29eKpZ/YMjHHm3of7BET3165c0GTGdBMCN5E5dVrDtC2x5h6Q3j6iPzpVxFrYBmbesNPj3pj63sa+sQzVNh3o6Dl6QtMpUBgDJa27vVv/giBq3N3Dk3SbOt3fr2aNnTccAEIfYlnfPeKtGw58wHQdZQhkHzPMFCiI77vvaflOf3/To63FJDxnOACBJ/YMjeurwcd25a7PCFSWm42ARb943B2Any/oOKG+8RUM1D3Ev3WEmhkY0dLGLY+qAxQSqlj9n8vNT0AGkZHIqoqcOH9e7tzdoXW3YdBxcx3Mv/lbnLo6ajgEgSd7RU9xLt7nYs2ZDF7s03NnFJnXAwvzFRV8x+fmNFvRQTVNbT8fBZyTtMZkDQOqePXpW/QOz99JhDbPL4J5X3/C06SgAUhS7lz5U8980VbjFdBwsITYdH+rs4qg6YCOFleUD77j3q8+azGB6gi7NTtEp6IADnGnp1ORURI3bG0xHcb3JqYgOHjqsvhGeUAOcImd6VMG2/6qRlX/K8jiLiR1RH+qcLeVMxwF7Kqgo/6npDFYo6LyJDjhIc3v3fElnw7sZk1MR/fw/f6W+0XzTUVwr3zNuOgIcjOVx5g11ds0fV+fuOOAMJt8+X8j4V8+8iY50oxSa197Vq6cOH9fexq38/yPL+gdH9NyRw+q9usx0FFerzL9sOgIcblnfAeVOj2h45Z+ZjuIKFHLA+Uy+fb6QVb5y3i8KOtKkvIQnv6wgtuGdkp49V/p7dPDZE5qYppwDbpA/8Et5xls1WPcIG97TjEIOuE9BeemXTWeQpJxoNGo6gySpp+Ngm3gTHWnQ3Tugpw4fNx0Dc8qCAUp6FkyND+kn//sFTUx7TUeBpN3lz+ld5UZ3zMBFIv41lPQUxe6QX2lpo5ADLuQLFER+96EfWOKLKCt9xbxf0rdNhwCQXkzSM29qfEg//8+nNTHNW/SAG+WNtyrY9gUN1/43TXuXm45jC7Et61daLrDUDYCKq1f8L9MZYqz01fLjoqADjhQr6fvu2GE6iuPMDDfr588eV894hekoWKAy/5LpCHCZvPFWlbT8kQbrHuGt9OuYnpjUUGeX+lsvaLizSxPDI6YjAbCQ/KLAZ0xniLFMQZ9bFvcDcRcdcKT+wREdPnqWJ9jSaGa4Wf9BObckf+6E6Qhwodln2L5ASZ/DsXUA8QjWrmyxwnK4GMsU9DmPi4IOOFZz++wXSJT01OWNt+o/XzisnvHVpqMAsBA3l/SFU/IrLRc4tg4gLstKg39vOsNClirooZqmQz0dBy+IZXFIAfecra25vVtlwYA21VebjmJbeeOt+s1v/reah/lGh1UVewdNR4CLuamkMyUHkApfoCCy476v7TedYyErNhmWxSElZUGeWbO6F081y+fL07rasOkotpM33qqOE9/XK4N3mo6CRQS/QwBtAAAgAElEQVQp6DDMySX9SsuF+QVv3CUHkAorLYeLsWJBf1zSw5KCZmMAyKQXTzarPBjgGyoJyBtv1dCZv9PBN+42HQWADTilpE9PTM4fW2fjOoB08fi8USsth4vJNR3g7UI1TQOSDpjOASCzJqci+tWR05qcipiOYgt5463S+a/rQMddpqNgCcXeIdMRgHmxkp433mo6SkImhkbUffwVnftfv9RL3/ufav3Fr3WllXvlANInEK5stdJyuBgrTtCl2WPuLItD0sqCAfUPcuzN6kaujutXR05rb+NW01EsLW+8Vf6Wr+qJjn2amMk3HQdLCOZxvB3WYpdJ+sTQiK60XlDPmXO62ttvOg4AhysoL/2y6QzXY8mCHqppOt7TcfCEpFtMZ4E9sSjOPrp7B3Ts1TZt21BnOooleaYuKdj2BR3svl2XJypNx0Ec8j3jpiMA14iV9IG1/6Bp73LTceZd7elTz6vnuU8OIKv8pcGx7R956AnTOa7Hyi1mv6Tvmw4BIPOOn21TVahE4YoS01EsJWd6VEXtf6FXrqzR6aHNpuMgTpX5l01HAK4r9u+UwbpHFPUUGstBKQdgWlHV8h+ZznAjOdFo1HSGG+rpODgglsUhCcdebdPxs22mYyABgQK/9t2xg9MPc2LTrv7BEf244yMcbbeR3eXP6V3lz5qOAdxQxL8m6yWdUg7AKjw+b3TvN35kuV1sMVb/Sni/pIdMhwCQeSNXx3X46FnduYtJsaT5pU5PdT9AObeZ2mXtpiMAi8obb50/7p5Js4veTlPKAVhKcFX1r01nWIzVC/rjoqAjCVWhEh0/azoFEtXe1av2rl7VVlWYjmJU0cVHlTfequf63s29cwAZkTfeqqKLj2p45Z+l9eOy6A2A1fmLi75iOsNiLF3QQzVNbT0dB38gNroDrnH46Fnd875drj3qXnTxUeUP/FKXJyr1m753mY6DJNQUMEGHPeQP/FKSUi7psXfKu4+dppQDsLRg7cqWd9z7VUvfQ7PDV8CPi4KOBLFszL4mpyKuPeruH/jF/BfMT3X/nuE0SAZvoMNu8gd+qanCLRoveW/Cvzd2p/xKq+WeEQaA61pWGvx70xmWYvmCHqppOsSTa0hGoMCvkas8d2RHbjzq7ht+XoGLfytJHG23Md5Ahx0FLv6tZjwBTRa9c8lfO9TZNV/Mpycns5AOANLDXxoc23Hf1/abzrEUyxf0OTy5hoRR0O3thZPNCleUuOKoe+wuqCQNTgU52m5jlf5LpiMASSm6+KgG6x5RxL/mmp+bGBpRz6vn1HvmPMveANiWlZ9WW8iy6+UXCtU0PS6J81NISFkwYDoCUjBydVyvNHeajpFxOdOjKm7/mnKmRyVxtN3ueAMddvX2fxdNT0yq59XzevWnP9Pxx5/QxReOUc4B2JYvUBDZ+cA3HjSdIx52Gk09Lja6IwFlJRR0uzt+tk3rVoUVKPCbjpIxwbYvKHdqttSdH1mnjrEaw4mQCo64w85ypy4r5/S31Hz5vRxhB+Aogarlz5nOEC87FfT9kj4jKWg6COyhnAm6I7xwstmxC+Niz6nFPN3zHoNpkA5scIcdTUW86uyq0+vt6zQ2XiDpvOlIAJA2Hp83uqwkaJul47Yp6KGapoGejoMHxEZ3xIkj7s7Q3tWr7t4Bx23mX7ixXZpdDDc0VWwwEVLF8XbYTd+VkDq76tTZtcp0FADImEC4snXbh75sm+vStinocx4WBR0JCFeUqLt3wHQMpOjYq23a27jVdIy0yRtvnd/YLkkTM/k6emWHwURIBwo67ODaaTkAOFthqPx+0xkSYauCHqppauvpOPikpH2ms8AeyoIBCroDdPcOOGaKHlvEtNBLV27VxEy+oURIF463w8qYlgNwo6IV4e533PvVZ03nSIQttri/jeXfroN1VIXsX+gw69irbaYjpEVxx9fml8JJPKvmJDXLKOiwlti0/Onn7tKRl/dQzgG4TmGo7K9NZ0iUrSbokhSqaTrU03HwGUl7TGeB9XEP3TmcMEUvuPxDeUdPveXHftP3bkNpkE75uRMKetngDmsYGy/UudaN6u5ZoUjEazoOABhRWFk+sOO+r9luuGu7gj7ncVHQEYdAgV+BAr9Gro6bjoI0sPNddO/oSRX0/OtbfmxwKqjTQ87cUO826wJsvYZ53T0r1NaxTn1XQqajAIBxhctD3zWdIRl2POKuUE3T45Jss4kPZtl54oq3ik3R7SZnelRFFx+95sePDrAYzim4fw5TpiJevd6xTk8/d5eOntxNOQcASb5AQeS2j/7lF03nSIZdJ+jS7Eb375sOAetbtaJCze3dpmMgTc5f6LbdN12KLj76lnvn0uzm9tODNxtKhHTj/jmyjWPsAHBjwdrqH5jOkCxbTtAlpuiIn93KHBbX3N5tqysLy/oOyDf8/DU/zuZ256jMv8z9c2RN35WQXjq5W08/t1edXaso5wDwNr5AQWTnA9940HSOZNm2oM953HQAWJ/Pm0dJd5hXmjtNR4iLZ+qSCnp+eN2fOz3E9NwpON6ObOjsqtPhF96rIy/v0aWeFabjAIBlBaqWP2c6QyrsXtD3S2JsgSXVVlWYjoA0ssuVhaL2v1DO9Og1P3566GYNTRUbSIRM2Fx8aulfBCRhKuLVudaNevq5u3TizA4NjQRNRwIAS/P4vNFlJcGPmc6RClsX9FBN04B4Fx1xWLWCgu4kk1MRnbd4SS+4/EPljbde9+e4e+4cxd4hVeZfXvoXAgkYGy/UmXO36Onn7tL51zdqbLzAdCQAsIXgqupfb/vQl219DdrOS+Ji9kv6jCS+rYwbChT4VRYMqH9wxHQUpEn7G71aVxs2HeO68sZbr3lSLWZwKqiOsZosJ0KmrAucMx0BDhJb/NbZtcp0FACwHSdMzyWbT9AlpuiIX71FyxyS097Va9llcYHrPKkWw9NqzsLxdqRD35WQTpy5dX7xGwAgcU6YnksOKOhzuIuOJXHM3XkuvNFrOsI1FjvaLnG83Uk43o5U9V0J6cjLe3Tk5T0UcwBIgVOm55JDCvrcFP2A6RywttgxdziH1ZbFLXa0XZLOj6zjaTUH4Xg7krWwmPddCZmOAwC2FwhXtjphei45pKDPedh0AFjfxvpq0xGQRv2DI5Y65l7Y/d1Ff56n1Zxle8lLpiPAZijmAJAZhaHy+01nSBfHFPRQTVObpB+YzgFrW8Vza45jlWPuy/oOyDt64/vIEzP5ah5Zl8VEyKSaZR0KerlZhfh0dtXp6efuopgDQAYEa1e2vOPerz5rOke6OKagz3nYdABYm8+bx7I4h7HCMXfP1CUV9Pxw0V9zfuSmLKVBNmwOshwOS4sV8xNndvBUGgBkiJOm55LDCjpTdMRj3SoKupNY4Zh7Ydf3lDM9uuivOc/03DHycyfY3o5F9V0J6fAL76WYA0CGOW16LjmsoM952HQAWFu4ooRlcQ7T1Ttg7HN7R0/KN/z8kr+O4+3Osb2Uu+e4voV3zIdGgqbjAIDjOW16LjmwoDNFRzxYFucs7QbvoRct8uZ5DNNzZ2F6jrdj+RsAZJ8Tp+eSAwv6nIdNB4C1rasNK1DgNx0DadJtaIJecPmHyp1a+h3sZu6fO8bm4tMsh8O8oeESijkAGOLE6bnk0II+N0X/O9M5YG0si3OOyamI+gdHsvo5c6ZHtaz/QFy/tn2sNsNpkC27yx33jXokYWy8UCfO3KrDL76HYg4ABpSuqT3uxOm55NCCPudhSYw5cEOb6qvl8+aZjoE06erJ7hQ90P3dJRfDSdLliUoNTRVnIREyjek5piJenThzq55+bq86u1aZjgMAruTxeaMF5WUfMJ0jUxxb0EM1TQOS9pvOAevyefO0cS130Z0im8fc88ZblT/wy7h+bcdVpudOwfTcvaYiXp1r3ainn7uLYg4AhgVXVf9624e+fMF0jkxxbEGfs19M0bEIpujOkc2CXtj93bh/LcfbnYHpuXvF3jI///pGRSJe03EAwNU8Pm90WUnwY6ZzZJKjCzpTdCyFKbpzZOseunf0pLyj8W/xZoLuDEzP3afvSkhPP3eXTpzZQTEHAItw+vRccnhBn8MUHYvatqGOje4O0ZeFgl7Y/b24f+3liUpNzORnMA2ygem5u4yNF85vZh8bLzAdBwAwxw3Tc8kFBZ0pOuKxdUOd6QhIg/6BzBZ0/8AvlDfeGvevvzyxPINpkA35uRO6ozK+fQOwt4UL4NjMDgDW44bpueSCgi5JoZqmhyU5/v+ZSN662rDCFSWmYyBFmT7iXnD5hwn9eo6329/20peUnzthOgYy7PWOdSyAAwAL8wUKIrs//sjtpnNkgysK+pyHTQeAtW1jim57mVwU5x/4hXKnLif0ey5PVGYoDbKh2Dukd3H33NFi98zPnLuFe+YAYGHB2uofmM6QLa4p6KGapsfFFB2LCFeUqL42bDoGUjRydTwjHzfR6blEQbe7u5b/zHQEZMjYeKFeOrmbe+YAYAO+QEFk5wPfeNB0jmxxTUGfc7/pALC2nVvqeXbN5jJR0JOZnnO83d7qA+dVU9BuOgbS7M33zPfqUs8K03EAAHEoW1v3edMZsslVBT1U03RI0jOmc8C6fN48NW5vMB0DKejqSf8xd6bn7pKfO6G7wkzPnaa7Z4UOv/BenX99o+koAIA4FVaWD+y472uuWvjtqoI+52HTAWBttVUVqq2qMB0DSZqciqT14yUzPZek8Rme7rOrveGfsRjOQWLH2Y+e3M1xdgCwmaKq5V8znSHbXFfQ56boT5rOAWtr3N7AUXebSvcm92Sm5xJH3O2qPnBe6wLnTcdAmpxr3ahfv/AejrMDgA0VrQh3u216LrmwoM/5jOkAsDaOuttXOu+gJzs9l6SJmfy05UB2cLTdOfquhOaPs7OdHQDsqaiq8h7TGUxwZUEP1TS1Sfo70zlgbbVVFWx1t6F0FvRkp+cSd9Dt6O4V/8bRdpubinh15twtOvLyHg2NBE3HAQAkqXRN7fF33PtVV7516sqCPudhSYOmQ8Dadm6pV1kwYDoGEpSOku4dPcn03EW2l77E1nab6+5Zoaefu0uvd6wzHQUAkAKPzxstKC/7gOkcpri2oIdqmgYkue5OAxITO+rOfXR7SUdBL+hJYXo+vjzlz4/sqcy/rDtCvzIdA0lauASO4+wAYH/BVdW/3vahL18wncMU1xZ0SQrVND0sybX/z0d8yoIB3bal3nQMJCDVTe6eqUvyjp5KUxpYWX7uhD6w4t9Mx0CSXu9YxxI4AHAQX6Agsvvjj9xuOodJri7oc1gYhyWtqw1zH91G+gZS2+Seyt1zifvndnL3in9T0MttJ7sZGy/UkZf36My5W5iaA4CDlKyu/RvTGUxzfUEP1TQdkPSM6RywvsbtDQpXlJiOgQzLmR5V/sAvU/oYvIFuD3vD/8G9cxuKTc37roRMRwEApFFhZfnAbR/9yy+azmGa6wv6HKboiMuduzazNM4GUnkLfVnfv6cxCaxqc/FpbS7mGoOdMDUHAGcrXln1SdMZrICCLilU03Rc0g9M54D1sTTOHlK5g+4f+EXKn58t7tZWs6xDe3nv3FaYmgOAswVrV7Zs/8hDT5jOYQUU9Dd9Rjy7hjiUBQPa27iVku5AvuHnk35abSG2uFtXZf5l3b3yp6ZjIE5TES9TcwBwOI/PGw0sD91pOodVUNDnzD279rDpHLCHsmBAd+7abDoGbqC7dyCp3+e/kvr0HNZV7B3SvTU/Un7uhOkoiEPsXXOm5gDgbKVrVj3p5mfV3o6CvkCopmm/eHYNcQpXlOjd2xtMx0CaeKYuyTf8vOkYyJD83AndveKnlHMbmIp4edccAFzCFyiI7PqDv7rbdA4r4Yzute6X9J+mQ8Ae1s09vfbs0bOGkyBV+UzPHSs/d0L31vxIlfmpX19AZvVdCenEmVs1Nl5gOgoAIAvK1tZ93nQGq2GC/jahmqZDkp40nQP2sa42zCTdghJdFJeO5XCwHsq5fZxr3agjL++hnAOASxStCHfvuO9r+03nsBoK+vWxMA4JoaRbTyJPrXlHT6ZlORyshXJuD2PjhTr8wnt1/vWNpqMAALLE4/NGi6oq7zGdw4oo6NcRqmlqk8R3c5CQdbVh3blrM9vdbYjpufNQzu2hs6tOv37hPRoaCZqOAgDIouCq6l+/496vPms6hxVR0G8gVNP0sFgYhwTVVlXwBJvN5EyPpn053GCEsmES5dz6piJenThzq06c2cEiOABwGV+gILL744/cbjqHVVHQF3e/6QCwn9g76YECv+koiEP+8G+UMz2a1o85NFWc1o+H+FXmX9Yn1vwPyrmFDQ2X6MjR29XZtcp0FACAASyGWxwFfREsjEOyyoIB7btjh8qCAdNRXGv46nhcv843xNNqTlGZf5l3zi2us6tOz7+8hyPtAOBSLIZbGgV9aSyMQ1J83jztbdyq+rmn2JBdI6NLF/RMHG+HGZuLT1POLYwj7QAAFsPFh4K+BBbGIRU+b54atzfotpvrTUfBdeQP/8Z0BKTB9tKXtDf8M8q5RXGkHQAgsRguXhT0OMwtjDthOgfsa1N9NcvjLIjj7faWnzuhveH/0B2hX5mOghvo7lnBkXYAgPylwTEWw8WHgh6/z5gOAHsLV5TonvftUriixHQUKLPH25nkZl6xd0j31vxIm4tPmY6CGzhz7hYdPbmbI+0AAJXUrvyS6Qx2QUGP09zCuL8znQP2FruXvrWhznQU18vk8XY2iGdWzbIO3b/qn/n7bFFTEa+OvLxHr3esMx0FAGABpWtqj7MYLn6ct03Mw5p9eo2zekjJtg11qgqV6FdHTmtyKmI6jistdrz9Ul9AE5PJ/+txPIXfi8XtLn9O7yrn+ppVDQ2X6KWTuzU2XmA6CgDAAjw+b7SgvOwDpnPYSU40GjWdwVZ6Og5+QNK/m84BZ5iciujw0bNq7+o1HcVxCoaHVTg8PP/fJ8fG1fdGdiauni0blRPkLfR0ys+d0N0r/k01Be2mo+AGOrvq9Mq5WzjSDgCYV3lzw7du++hfftF0DjuhoCehp+PgIUl7TOeAc7zS3KkXTzWbjuEoM+2dmrnQaeRzU9DTqz5wXnexpd3Szpy7hSPtAIC3KKwsH/gvn/9uqekcdsM5zOTcL+m4OOqONNlUX62qUIkOHz2r/sER03EAS8jPndC7yp/V9tKXTEfBDcTeN7/Us8J0FACAhXh83miwZuX7TeewI5bEJWHubfSHDceAw5QFA9rbuFUb11abjgIYV7OsQx9b9X3KuYWNjRfqyNHbKecAgGuUrln1JG+eJ4cj7ino6Th4XNItpnPAedq7enX46FkWyKWAI+42FZnWTHunqqdflSQtLx9Vvi+iYNG4SgLjChaNKxgYNxwSQ8Mlev7lPdw3BwBcw18aHHvPl/6JbaFJ4oh7au6XdMx0CDhPbVWF7nnfLv3qyGl19w6YjgNkRXRwSDPnWhQdn1C7SiRJ7d0l1/21+b6IlpeNKD8/ouVlo/Lnz/13X0TLy7kmkkmdXXU6cWaH6RgAAIsqrat5wHQGO2OCnqKejoMPS3rIdA441yvNnTp+to1peoKYoNvI3NR85mJX2j7k2wt8bAJfWT4iv48/S8k617pR51/faDoGAMCiytatfmb3xx+53XQOO6OgpwFH3ZFOXc3tGr4yqOH+QfVdvKTJsQl1d/cpd/1a5RRyWiheFHR7WDg1z6ba8ADlPUEnztyqzq5VpmMAACyKo+3pwRH39LhfHHVHAmLF+42Wdo30Lyjji5SU6ZdPKndVtXJrWSIHB8jA1DwRsaPz5y9UXPNzteEBBYsmFAyMa3n5yPx/utVUxKsjR2/X0AgPlwAAboyj7enBBD1NOOqO6+m7eGm2fL9xWX0XL2lk7q9TkRMslmf9Wik/P00pnYkJunWZmpqnqrJsdsJeWzU4P3WvrXL2jgjKOQAgHhxtTx8Kehpx1N29MlHEF5WXp9zaauWuDGfuc9gcBd2CDE/NMyU4dzx+edmooybubGoHAMSDo+3pxRH39LpfHHV3tMmxcfVdvKy+Ny6p7+JlDfcPqqulPftBIhHNtLYp2tcvz8b1Up4n+xmABNh1ah6PwRG/Bkf81xyXrywb0fLyUQUD41pVNWCrO+6UcwBAvDjanl5M0NOMo+7OEbsX3vfG5dnFbf2DGrkyaDrWtfLy5LlprXLKS00nsRQm6Bbh0Kl5soKB2Xfca6sGtbx8ZH7ibiXdPSt04sytlHMAwJI42p5+FPQM4Ki7/by9jC+1sM2KcsrL5LlpLdP0OSYLel7jLiOf12qifVc0fa5FithjamxK7Em45eWjc0flR4wdkeeNcwBAvDjanhkccc+M+8VRd8tyQhm/nmhfvyK/HWKaDvMi05o+16JoX7/pJLYwMZmn9u6S+c3yMbXhAS0vH1Vt1UBWJu2UcwBAIjjanhlM0DOEo+7WELsz/kZLu6PK+FKYpjNBN4WpeebEJu21VYNpv9P+esc6nTnHwS8AQHw42p45FPQM4qh79vVdvKSulvbZUt7cbs0749ni8rvpFPQsY2puxML77LMT98SPxp84c6s6u1ZlIB0AwIk42p5ZHHHPrPvFUfeMmRwb1xvN7fNH1Y1sU7eySETTZ15jmo6Mi17q0XTrBabmBgyO+HXqvF+nzi+f/7Ha8MCbpb1qYNEpO+UcAJAojrZnFhP0DOvpOPgZSd82ncMJYk+axY6qZ/Sdcadx4TSdCXoWTExo+rUWRQeHTCfBImLPvdVWDWhV1cD8XXbKOQAgURUN9Qd2/cFf3W06h5NR0LOgp+PgIUl7TOewm9hx9TeaZ4+su/q4epq4aZpOQc+smYvdmmnvZGpuQ8HAuKoriuVR0HQUAICNFFaWD/yXz3/XPdMeQzjinh33Szou8dXQYhYW8q7mdlcsc8u2+U3va1YpZ3nIdBzYEVNz2yv2h+SR33QMAICNeHzeaLBm5ftN53ADCnoWhGqa2no6Dt4v6d9NZ7ESCrkhkYimz7Uo51KPPOvXSvn5phPBJmbaOzVzsZupuY3VVBSpNEA5BwAkpnz92r9+x71ffdZ0DjfgiHsW9XQcPCBpn+kcpiy8Q9526hyF3Ary8pRbW63clWHTSdKOI+7pEx29qpnXWhQdHTUdBSmgnAMAklG0Ity957P/vcp0Drdggp5d92v2qLsrtvLEtqxfOH2eJ8+sKhLRTGubon39TNNxXSa/0YH0oZwDAJLhCxREileGnTV5sDgKehaFapoG5o66/6fpLJnS1dyuN1radeHUObas20h0cEiRF48pd1W1cmurTcdJD05opCQ6OKSZcy2K8vfR9ijnAIBkla2t+/y2D335gukcbsIRdwN6Og4+LOkh0znSIXZsve3UOe6RO0ROYaFy169VTmGB6SgpmT55xtgiM1sfcY9Mz9017zKdBGmwoiygiuJlpmMAAGyobN3qZ3Z//JHbTedwGwq6IT0dB49LusV0jmR0Nber7fRsIWdK7ly5q6qVu6LKtk+yUdATx9TcWUoDftVUFJmOAQCwIX9pcOw9X/one09rbIoj7uZ8QDZ5eo0puTvNXOhU9FKPcm9aq5xgsek4yKTItKbPtSja1286CdKEcg4ASJbH542WrVn1u6ZzuBUF3RCrP73Wd/GS2k6f5y65y0XHJzR98oxyl4eUu6bOttN03Fi074qmz7XwdJqDUM4BAKngSTWzOOJuWE/Hwcclfcx0DkmzE/KWdrWdOs/GdVwrL0+em9Yqp7zUdJK4cMR9CRMTmn6txdjfI2RGwO/VmnCJ6RgAAJsK1q5safz0/nrTOdyMCbp5n5G0VQbuo0+Ojavt9HneJUd8IhFNn3lNOeVl8qxdxZNsNjZzsVsz7Z1MzR1mmS9Pqyotf2sKAGBR/tLgWGB56E7TOdyOgm7YgqfXDikL99Fjpbzt1DldOH0+058ODhTt61dkcEi5tdXKXRk2HQcJiI5e1UxLG1NzB1rmy9OacIk8uTmmowAAbMjj80ZL62oe4Ek18yjoFhCqaTre03HwM5K+n4mPP9w/qAunz+nci6e4T470iEQ009qmaF+/ctfW2f5JNjeYae/UzIVO0zGQAZ7cHNVUFFHOAQBJK6tf/c/bP/LQE6ZzgDvolpLO++iUcmSTFZ9k4w76rOjoVc281qLo6KjpKMgAT26O1oZL5Pfx/XYAQHK4d24t/C+6taR0H51SDlN4ks2CItOzU/OLXaaTIINWlAUo5wCApHHv3Hr4X3ULSeY++uTYuM799hSlHMbxJJt1RAeHNHOuRVEWPzrairKASgN+0zEAADbFvXNroqBbTDz30Vn0BiubudSjmb4rtnqSzTEi05ppbdPMpR7TSZBhpQG/KoqXmY4BALAx7p1bE3fQLep699HbTp3Tud+eopTDNnKCxfKsX2vkSTa33UGP9l3R9LkWnk5zgWW+PK1bwTe/AADJ4965dTFBt67PSNra1dx+y7nfnuKdcthSdHBIkZdPKXdlWLm11abjONPEhKZbLija1286CbLAl+fRmnCJ6RgAABvj3rm1UdAtKlTTNPCz//Hnn3r1N8d+PTk+wds5sK9IZHaJXO8V5a5fy5NsaTRzsVsz7Z1MzV3Ck5ujuspinlMDACTN4/NGy9as+l3unVtXrukAuLHf+8NvPbv2HRv/2nQOIB2io6OafvmkZlovSJHpzH/CCQefOJmYXcg309pGOXcRNrYDAFJVvn7tX7/j3q8+azoHbow76Dbw469/8lDribN7TOcA0iXHn6/cNXUZXSIXOXwkYx97KZm8gz7T3qmZC50Z+/iwpuUlhVpewukTAEDyytatfmb3xx+53XQOLI4Jug3c+5Xv3l5RHR4wnQNIl+j4hKbPvKbpM+eyM013gOjgkKZfPkU5d6GA30s5BwCkpLCyfIBybg8UdJuoaViztTBYxFlWOEq0r1+R3x7TzMVu01GsKzKtmRS2tIMAAB1rSURBVNYLs1vpR0dNp0GW+fI8WlUZNB0DAGBjvkBBpGRVzVbTORAfCrpN7P3ENy+s2brhPp8/nzsJcJZIRDOtbZo+ecY598bT9H9HdHBI08dOauZiV1o+HuyHpXAAgFR4fN5o+bo197EUzj4o6Dby/k898sTqW9b/s+kcQCZEB4cUefHY7FZym4um+iRiZFoz51pmp+Y8r+haLIUDAKSqrH71P2//yENPmM6B+FHQbeaDn/vOg6s2rTtuOgeQKTMXOjX98ilFB4dMRzEi2ndl9tj/pR7TUWBQcUG+KoqXmY4BALCx0jW1x3c+8I0HTedAYijoNvT7D//jNpbGwcmio6Nzz4gl/yRbTrA4zakybGJC02fOafrMazyd5nK+PI9qKopMxwAA2FhhZfnAu/7w0W2mcyBxFHSbYmkc3GDmYpemj51UtO+K6SgZNXOxW5GXTyna1286CiyAe+cAgFSwFM7eKOg2xdI4uIUtn2TLi/Pe8MTE3EmBNqbmkMS9cwBAalgKZ38UdBtjaRzcJPYkW9QGd7NzCpd+s3qmvXN2au7Su/a4VsDv5d45ACAlLIWzPwq6zX3wc995cM0tDc+YzgFkRSSi6bnt5nZ9ki06elXTL5/SzIVOpuaY58nN4b1zAEBKytatfoalcPZHQXeAe7/y3dvDa2q6TecAsiU6OKTIy6c0c9Fe/9jPtHdq+uWTio6Omo4Ci6mpKOLeOQAgaUUrwt27P/7I7aZzIHUUdIeoWlOzK1hZNmY6B5A1kYhmWttmn2QbvWo6zVu9fbofmX5zag68TWnAr+KCfNMxAAA25S8NjhWvDO8ynQPpQUF3iL2f+OaFus03/S5L4+A20dFRTb98UjPt1im/06+cm908H5lWtO/K7CZ6pua4Dl+eRyvKAqZjAABsyuPzRsvWrPpdlsI5R040Sp9zkv/v77/wf5565sUfm84BmJBTWKjctauUEyzW9MkzLGCD5a0Nl6jQ7zUdAwBgU1XbNt/LUjhnoaA70E//5o//6bUXTv6B6RyAKbkrqxQdGGJqDUurKF7G9BwAkLTQxpseYymc81DQHerHX//kodYTZ/eYzgEAuJYvz6N1K0pZDAcASErZutXPsBTOmSjoDvYvX3mgufO119eazgEAeCuOtgMAkhWsXdnS+On99aZzIDMo6A73D3/0f1wdvNy/zHQOAMCs4oJ81VUWm44BALAhf2lw7D1f+qcC0zmQOWxxd7g1Wxo28PwaAFiDJzdHNRVFpmMAAGzIXxocK69fvcF0DmQWBd3h9n7imxdqN9Q/wPNrAGDe8pJC7p0DABLm8XmjpXU1D/CcmvNR0F3g/Z965In1O2/5sOkcAOBmAb9XFcXcOAIAJK5y0/oP85yaO1DQXWK2pG95zHQOAHArnlQDACQjtPGmxyjn7kFBd5EPfu47D1LSASD7KoqXye/LMx0DAGAzvHXuPmxxdyGeXwOA7PHk5qihupy75wCAhPCcmjsxQXehj379+/XV61e3mM4BAG6woixAOQcAJIRy7l5M0F2MN9IBILOW+fK0bkWp6RgAABvhrXN3Y4LuYryRDgCZxWI4AEAieOscFHQX2/uJb15Ys6VhA2+kA0D6BfxeFfq9pmMAAGzCFyiIlNev3sBb5+5GQXe5vZ/45oX1O2/5MCUdANKruqLIdAQAgE14fN5o+bo191HOQUHH3BvplHQASJfSgF++PI/pGAAAG/D4vNHKTes/zFvnkCjomPP+Tz3yxLpbN/+p6RwAYHee3BwtL2G3DwAgPqEN6/6Uco4YCjrm7fvjR/ev37nlMdM5AMDOKooLmJ4DAOIS2njTYzvu+9p+0zlgHRR0vMUHP/edBynpAJAcT26OKop5vRIAsLTQxpse2/nANx40nQPWQkHHNSjpAJCciuICeXJzTMcAAFgc5Rw3khONshcM1/cvX3mgufO119eazgEAduDJzVFDdTkFHQCwqGDtypbGT++vN50D1sQEHTf00a9/v756/eoW0zkAwA6YngMAlkI5x1Io6FgUJR0AlsbdcwDAUijniAcFHUuipAPA4koDfqbnAIAbopwjXhR0xIWSDgA3xvQcAHAjlHMkgoKOuIVqqu4MVpaNmc4BAFZSGvDz7jkA4Lr8pcGxwPLQnaZzwD4o6Ijb3k9888KaLQ0bKOkA8KblJQWmIwAALMhfGhwrr1+9YduHvnzBdBbYBwUdCaGkA8CbAn4v03MAwDUo50gWBR0Jo6QDwKzlJYWmIwAALIZyjlRQ0JEUSjoAt/PleVTo95qOAQCwEMo5UkVBR9Io6QDcjLvnAICFKOdIBwo6UkJJB+BGntwcFRfkm44BALAIyjnShYKOlFHSAbhNcUG+PLk5pmMAACyAco50oqAjLSjpANwkVLzMdAQAgAVQzpFuFHSkDSUdgBss8+XJ78szHQMAYBjlHJlAQUdaUdIBOF0F03MAcD3KOTKFgo60o6QDcDKWwwGAu1HOkUk50WjUdAY41FPf+9Kq1pNnXx283M+4CWbk5Sm3vFQ5wWLJ/2apig4OvflrItOKjowu+aFy/Plv+Rg5weI3P97IVWl0VDOXetKTG5ZVGvCrpqLIdAwAgCGUc2QaBR0Z9dT3vrSqq7XjSHdrR9h0FrhLjj9fni0bpfzsTTujo1c1ffKMFIlk7XMiu+oqi5mgA4BLBWtXtgSWh+6knCOTKOjIin/5ygPNna+9vtZ0DriH56a1ylkeyvrnnbnYrZnWtqx/XmSeJzdHm2orTMcAABgQrF3Z0vjp/fWmc8D5uIOOrPjo179fX71+dYvpHHAPE+VcknINfV5kHpNzAHAnyjmyiYKOrKGkI1sW3g/PujyPcgoLzX1+ZAxvnwOA+1DOkW0UdGQVJR2ukOcxnQBp5svz8PY5ALgM5RwmUNCRdR/9+vfr67dvOmA6BwDEq7jAZzoCACCLQhtveoxyDhMo6DDiQ3/+D3ev37nlMdM5ACAeAb/XdAQAQJaENt702M4HvvGg6RxwJwo6jPng577zICUdgNV5cnNYEAcALkE5h2kUdBj1wc9958ENu7d9y+fP570/AJZEOQcA5/P4vNHwLRs/SzmHaRR0GHf3Z7/9xfU7b/kwJR2AFXG8HQCczePzRis3rf/wjvu+tt90FoCCDkt4/6ceeYKSDsCKmKADgHPFyvn2jzz0hOksgERBh4W8/1OPPLHp3dtXByvLxkxnAQBpdnruyc0xHQMAkAH+0uBY+JZNqynnsBIKOixl7ye+eWHNloYNlHQAVlDo53k1AHAif2lwrLx+9YZtH/ryBdNZgIUo6LCcWEmvXr+6xXQWAO4W5P1zAHCcYO3KFso5rConGuXKL6zrX77yQHPna6+vNZ0D9pITLJZny0Zjn3/65BlFB4eMfX6khyc3R5tqK0zHAACkUbB2ZUvjp/fXm84B3AgTdFjaR7/+/fr67ZsOmM4BwH043g4AzlLRUH+Acg6ro6DD8j705/9w9/qdWx4znQOAu/C8GgA4R2jjTY/t+oO/utt0DmApFHTYwgc/950Hb95z2708wwYgW5b58kxHAACkyOPzRqu2bb535wPfeNB0FiAeFHTYRuyt9MJgUcR0FlhcZNp0AjhAIRN0ALA1f2lwjDfOYTcUdNjK+z/1yBM33XpzPc+wYTHR0VHTEWBzHG8HAHuLPaNGOYfdUNBhOzzDBiDTWBAHAPbFM2qwM55Zg639+OufPNR64uwe0zlgPXmNu4x9bp5Zs7+6ymIVF+SbjgEASFDZutXP7P74I7ebzgEkiwk6bO3er3z3dja8A0g3PwviAMB2QhtveoxyDrujoMP22PAOIJ08uTny5XlMxwAAxIlN7XASCjoc4f2feuSJDbu3/Q7L4wCkiufVAMA+/KXBseU3b/gdlsHBKSjocIzf+8NvPbtmS8OG8JqabtNZANgXC+IAwB6KVoS7y+tXb3jHvV991nQWIF1YEgdH+teH/+9jF145v9V0DpjDkjgkq6aiSKUBv+kYAIBFlK6pPf6uP3x0m+kcQLoxQYcj/f7D/7ht/c4tj3EvHUCiuH8OANbl8XmjoY03PUY5h1NR0OFYH/zcdx5cv/OWD1PSASSi0O81HQEAcB2+QEGkctP6D7MMDk5GQYejvf9Tjzyx6d3bV7M8DkA8mJ4DgDX5S4NjoQ031bMMDk7HHXS4xr985YHmztdeX2s6B7KDO+hIRsDv1ZpwiekYAIAFgrUrWxo/vb/edA4gG5igwzU++vXv16/fueUx0zkAWJefJ9YAwFJCG296jHION6Ggw1U++LnvPHjzntvuLQwWRUxnAWA9nlz+ZxEArMAXKIhUbdt8L/fN4TZ8JQLXef+nHnnipltvrq+oDg+YzgLAWpb5uIMOAKYVVpYPcN8cbsUddLga76U7F3fQkYy14RK2uAOAQbxvDrdjgg5X+/2H/3Hbht3bvsVTbAAk7qADgCkenzdaeXPDtyjncDsKOlzv7s9++4vrd97yYZ5iA+DJzTEdAQBcx18aHKvctP7Dt330L79oOgtgGgUd0Oy99DVbGjZUr1/dYjoLADMo5wCQfcHalS3l9as3cN8cmMUddOBtfvo3f/xPr5947f+aHJ/gq3Ub4w46EsUb6ACQPR6fN1pWv/qf2dIOvBUTdOBtPvi57zy4fuctH+YpNgAAgPTzBQoilZvWf5hyDlyLgg5cR+wptvCamm7TWQBkRy5voANAxhWtCHfzhBpwYxxxB5bw/37rj/69/ZXmfRx5txeOuCNRy0sKtbykwHQMAHAkj88bLV2z6sldf/BXd5vOAlgZ4wJgCR/683+4my3vAAAAyYltaaecA0ujoANxYMs7AABA4tjSDiSGI+5Agtjybg8ccUeiVpQFVFG8zHQMAHAEtrQDyWGCDiTog5/7zoMbdm/7HY68A86yzJdnOgIAOIK/NDi2/OYNv0M5BxLHBB1IwY+//slDrSfO7jGdA9digo5ErQ2XqNDvNR0DAGytbN3qZ3Z//JHbTecA7IoJOpCCe7/y3ds3NW7/LG+mAwAAN/MFCiLhWzZ+lnIOpIaCDqRo3x8/up830wEAgFvF3jbfcd/X9pvOAtgdR9yBNGKBnHVwxB2J4og7ACSGRXBA+jFBB9IotkCuojo8YDoLAABAphRWlg+wCA5IPyboQIawQM4sJuhIFBP0/7+9e4uN4zoPOH5mdnZn9sLV7molMgwl6m4aMq06gp3WZWUXfUhQxzcogdQUSNrAQBNDUOhSlijZios2rpFagQtKBk2HMFIHRlq0qsGqgh6CorUTNHXQAEkMw5Zhm7JEWpQoSiR3l9wbZ/IQrEMrupC7s3Pm8v892gL1QW9/fmfOAYCl4SI4oHnYoANNsvvJF+7tvueu3TzHBgAA/MBIr5j/1B237SbOgeZhgw44gG2689igY7nYoAPA9bE1B5zBBh1wQG2bznNsAADAS3g+DXAWgQ445P49//AvW+7s3tS5dfMvZM8CAABwM+kNa3/B82mAszjiDkgwMtDXe+ZX7z5bmMlpsmfxK464Y7k44g4AvxFJxKqZjeseJ8wB57FBByR4cO93/5FtOgAAcBu25oBcbNAByUYG+nrHTo/+/czFy1HZs/gJG3Qs15psi0gnDNljAIAUbM0BdyDQAZfgpnd7EehYrtZUXLSmYrLHAADHcUM74B4ccQdcgnfTAQCAk3jXHHAfNuiAC/3zt7/+P2OnR3eUiyVF9ixexQYdy8UGHUBQhCJha0Vnx+uEOeA+bNABF9r95Av33nr3HTuyHW3TsmcBgmLBNGWPAABNF1+9crq1+9YdxDngTmzQAZc7fmTv8OgvT3+NbfrysEHHciWMsNjQlpI9BgA0RSgStjKb1r/02b98+hHZswC4PjbogMvt3DfwyNae7es7bln/vuxZAACA96xY++n327ZtXU+cA+7HBh3wkJGBvt4zv3r32cJMTpM9i9uxQcdyRSOa2Nyelj0GANiGp9MA7yHQAQ/iErmbI9BRj9vXrZI9AgDYgqfTAG/iiDvgQVwiBwAAriW+euV0+/bb/4g4B7yJDTrgca8+99gzZ996bx/H3j+JDTrqsbEtJeJGWPYYALBskUSsmlq/9shdX/m7g7JnAVA/NuiAxz382HMHt9zZvWnDtq7XZM8CAACcl9m8/rVVt27ZRJwD3scGHfCRk4P9PePvnjlxaWwi8G9FsUFHPdozCZFNRmWPAQBLosZic223bvrcZ3Yf/onsWQDYg0AHfIjb3gl01Kc1FRetqZjsMQDghqqmJZRU6t8fPDy8U/YsAOxFoAM+FuTb3gl01CNhhMWGtsAfQAHgUqZliQU9+uHDT/9gnexZADQH36ADPrb7yRfu3dqzfX3HLevflz0L4AULJr+0BuBOZVXLhVa3fok4B/yNDToQECMDfb0XRsefCsr36WzQUS/eQgfgJmVLqWrp1NADT7y4R/YsAJqPQAcC5viRvcNj74x+1e/fpxPoqFdXR0ZEtJDsMQAEXNW0hEgmX3/oqZfukT0LAOcQ6EBA+f37dAId9Vq3OimSMV32GAACqvaduZ5O3f+n+46+KXseAM4i0IEAOzV0qHPy3Pn/Gjs9ulH2LHYj0FEvbnIHIEtZ1XLGquwfEuZAcBHoAMTJwf6eC2fG/3Xig3NtsmexC4GOeiVjuli3Oil7DAABUraUqr561Z/dt//5f5M9CwC5CHQAH/PTRXIEOuoV0UKiqyMjewwAAcAFcACuRqAD+B2vPvfYM2ffem+fly+SI9DRCG5yB9BMXAAH4HoIdADX5eUb3wl0NGJjW0rEjbDsMQD4jGlZwmwhzAFcnyp7AADutXPfwCNb7uzetGFb12sRQ+e3eQiMfLEiewQAPmJalqhEjA+1tk/dTpwDuBE26ACW5NTQoc6Zycv/5JWn2digoxFcFAfADjyZBmC5CHQAy1IL9Q9++Y6rNwAEOhrBRXEAGlXWIpPGysyfEOYAloNAB1CXk4P9PVPjF77v1jfUCXQ0qqsjIyJaSPYYADymrGo5fWXmazyZBqAeBDqAhrg11Al0NGpNtkWkE4bsMQB4BGEOwA4EOgBbuC3UCXQ0Kp0wxJpsi+wxALgcYQ7ATgQ6AFu5JdQJdDSK79AB3AhhDqAZCHQATSE71Al02IHv0AFcjTAH0EwEOoCmOjnY35Obmv6208+zEeiwA9+hAxDiN8+lVcP6pJ5OPUqYA2gmAh2AI5x+R51Ahx14Dx0INt4xB+A0Ah2Ao5wKdQIddgipiti6Nit7DAAOI8wByEKgA5Dm+JG9w2PvjH61MJPT7P7ZBDrssrEtJeJGWPYYABxQNS0hksnXH3rqpXtkzwIgmAh0ANIdP7J3eGr84s5LYxMpu34mgQ67ZJNR0Z5JyB4DQBNVTMtUksmfEOYAZCPQAbjGyEBf74XR8afsCHUCHXaJRjSxuT0tewwATVC2lKqWTg098MSLe2TPAgBCEOgAXMiOJ9oIdNiJ59YAf+GpNABuRaADcK1GLpQj0GGn9kxCZJNR2WMAaAAXvwHwAgIdgCccP7J3eGJ07MszFy8vqZIIdNiJY+6Ad3HxGwAvIdABeMrIQF/v1PjFAxMfnGu70Z8j0GE3jrkD3lJW1JK2YsUw35cD8BICHYAnnRzs75m+MHX0/Ptnt13r+DuBDrtxzB1wP9OyRDWsT+rp1KN8Xw7Aiwh0AJ53rePvBDrsxjF3wL1qz6RF4vE9fF8OwMsIdAC+ceLY/l1XJiafHjs9upFARzNwzB1wl7Kq5bRky8scYwfgFwQ6AN85NXSo82y+eGLWUrqtSNjxv59A969sMiraMwnZYwCBVjUtYcXjb+rJ5J+zLQfgNwQ6AF/7/sDjx2ZLla8UdaPFqb+TQPeviBYSXR0Z2WMAgcS2HEAQEOgAAuGHgwe7Z+dKrzixVSfQ/W3d6qRIxnTZYwCBwLYcQNAQ6AAC5+WjBw5MF0tPFLVwiwjZ/z0xge5v6YQh1mQdO5ABBI5pWaIaCrMtBxBIBDqAwPrh4MHuQrF8bLaycHfVMDS7fi6B7n9b12ZFSP2d1/0ANICb2AGAQAcAIYQQrzzf/8XZ+dKRvFA7Gz0CX/3p/wtRrdo0GdyIN9EBe1RNS5gR3i0HgBoCHQCu8vHFcnUega/++P+aMBXchMvigPrVjrCHEvEfPXh4eKfseQDATQh0ALiO2hH4fGXhs2XDWPKtYAR6MGxsS4m44fwzfoBXlRW1pMbjb3CEHQCuj0AHgCWo3QKfM62tpq6rN/qzBHowJGO6WLc6KXsMwNUqpmWKePytSCLxtxxhB4CbI9ABYJleeb7/i/li+VvXe7KNQA+Oro6MiGj2vwQAeFnVtIRlRD+MrEjuI8oBYHkIdABowMtHDxyYLZb75hV1VS3WCfTgyCajoj2TkD0GIF3tsrdwMvnd+w8Ofkf2PADgVQQ6ANikFusLp99LF2Zytj3bBvcKqYro6ljJk2sIJKIcAOxHoANAE5w4tn/X7KUr/ZfGJm4j1v2tNRUXramY7DEARxDlANBcBDoANNmJY/t3FaZnvzF1/uJdMxcv83i2z/DkGvyuYlqmMKLntERikCgHgOYi0AHAQScH+3sKM7m+yXPnP0es+8eabItIJwzZYwC24fZ1AJCDQAcASU4NHeqcy+UPz0xeue/yRxdby8USHzJ7FFt0eJ1pWaKqhninHAAkI9ABwCVefe6xZ+Zm8p/nu3VvYosOr6l9Tx6KRX/84OHhnbLnAQAQ6ADgSieO7d81ny/snr4wde+lsYmU7Hlwc2zR4QVlS6kqsejbWjT2Ct+TA4D7EOgA4HKnhg51Fufmv56bmv7SlYlLnWzX3YstOtymalrC1MK5UCL+o3A0+jccXQcAdyPQAcBjatv1/JXZ35/44Fyb7HnwW2zRIVvtW3LFMN7lgjcA8B4CHQA8bmSgr3d+tvAQz7i5A1t0OK1sKVVF18dDseh/PvDEi3tkzwMAqB+BDgA+UjsOPzeT//z05NQtBLvz2KKj2SqmZVoRfYrL3QDAfwh0APAxgl0Otuiw0+Ig5ztyAPA3Ah0AAqQW7KXC/B/MTk1v44b45gipiujqWClCKk/bY/kWH1nXdH2IIAeA4CDQASDgat+wz+UKt1z+6GJruViiKm3QmoqL1lRM9hhwucWXuoV0/XW+IQeAYCPQAQCfcHKwv6dYmPuLYn5+O8fi6xdSFbG5PS0iWkj2KHCRsqVURTh8RTX0t8PR6FFuWQcALEagAwBuamSgr7c0V7ynmJ/r5i32pUsnDLEm2yJ7DEhSMS3T0sIFRY+cYTsOAFgKAh0AsGynhg51lkulh2tH43NT01mi/do2tqVE3AjLHgNN9nGMa9plnjsDANSLQAcA2Gbxpr1YmF/JJXRCJIyw2NAW+H8GXylbSlWEQvNsxgEAdiPQAQBNdeLY/l3VSuX3ajfHz+cKiaBt23l2zZuqpiXMUKikhCMTqqH/XNXCP7v/4OB3ZM8FAPAvAh0AIMXIQF9vtVy5baGY78pf+uiOheKsMTkVUWXP1Qw8u+ZuFbMihKKaihEdF2F9VNW0N9mKAwBkINABAK7yxvfuO1AuVe7Kz5S2zxUWMoW8GR07H/H8xj2bjIr2TEL2GIFlmpYwRdlSNLOqha05I668HdbVn+346//4puzZAACoIdABAJ7w85cf6i7Nlf6qNF/pLs5VOmvxPjkV0kplbzxltqU9LQzv/67Bta4V4aqmTPzx4ycelj0bAABLQaADAHzhje/dd2BhwVxTyBV3VMtmcma60lYuidBsXtFmc+64RT0a0cTm9rTsMTyrai4IIaqWUC0rrJu5kCbm9Lj6RiiknGUTDgDwAwIdABAItQ28EELMTM19QQghalt4IYRw6hh9eyYhssmoE3+Vp1TNkiWEELXttxBCxFao/y2EEHpce/buR1/9X5nzAQDgBAIdAIBFFod87Ti9EEJUKmZs+vLCx+vveoM+pCpic3taRDRvHMuvVy24hfhkdId1ZSJsKG8LQXgDAHA1Ah0AgAYtjvqa2pZ+sckLlU8LIURY1ZVoqGXRjfWaoqlyg732/fa1/l84ujB79X+rbbdriG0AABr3a5oV2Fa/gHPmAAAAAElFTkSuQmCC" alt="Logo" style="width: 100px; height: auto;">
    	</div>
		<h2>Crop Type: ${fieldEntries[0].crop_type}</h2>
	</div>
	<div class="chart-container">
		<h3>Health Index Chart</h3>
		<img src="${chartImage8}" alt="Health Index Chart" style="width: 100%; max-width: 800px;">
	</div>
	<div class="chart-container">
		<h3>Yield Chart</h3>
		<img src="${chartImage9}" alt="Yield Chart" style="width: 100%; max-width: 800px;">
		</div><div class="chart-container">
		<h3>Sprayability Chart</h3>
		<img src="${chartImage10}" alt="Sprayability Chart" style="width: 100%; max-width: 800px;">
	</div>
	<div class="chart-container">
		<h3>Temperature Chart</h3>
		<img src="${chartImage}" alt="Temperature Chart" style="width: 100%; max-width: 800px;">
	</div>
	<div class="chart-container">
		<h3>Pressure Chart</h3>
		<img src="${chartImage1}" alt="Pressure Chart" style="width: 100%; max-width: 800px;">
	</div>
	<div class="chart-container">
		<h3>Humidity Chart</h3>
		<img src="${chartImage2}" alt="Humidity Chart" style="width: 100%; max-width: 800px;">
	</div>
	<div class="chart-container">
		<h3>Dew Point Chart</h3>
		<img src="${chartImage3}" alt="Dew Point Chart" style="width: 100%; max-width: 800px;">
	</div>
	<div class="chart-container">
		<h3>Rainfall Chart</h3>
		<img src="${chartImage4}" alt="Rainfall Chart" style="width: 100%; max-width: 800px;">
	</div>
	<div class="chart-container">
		<h3>UV Index Chart</h3>
		<img src="${chartImage5}" alt="UV Index Chart" style="width: 100%; max-width: 800px;">
	</div>
	<div class="chart-container">
		<h3>Soil Moisture Chart</h3>
		<img src="${chartImage6}" alt="Soil Moisture Chart" style="width: 100%; max-width: 800px;">
	</div>
	<div class="chart-container">
		<h3>Soil Temperature Chart</h3>
		<img src="${chartImage7}" alt="Soil Temperature Chart" style="width: 100%; max-width: 800px;">
	</div>
  `
	return true
}

// const triggerPrint = async () => {
// 	if (!(await preparePrintContent())) return

// 	const printSection = document.createElement('div')
// 	printSection.id = 'printSection'
// 	printSection.innerHTML = printContent.value
// 	document.body.appendChild(printSection)

// 	const style = document.createElement('style')
// 	style.textContent = `
// 		@media print {
// 			body * {
// 				visibility: hidden;
// 			}
// 			#printSection, #printSection * {
// 				visibility: visible;
// 			}
// 			#printSection {
// 				position: absolute;
// 				left: 0;
// 				top: 0;
// 				width: 100%;
// 			}
// 			.chart-container {
// 				page-break-inside: avoid; /* Prevent splitting graphs */
// 				break-inside: avoid;
// 				margin-bottom: 20px;
// 			}
// 			.headings {
// 				display: flex;
// 				flex-direction: row;
// 				justify-content: space-between;
// 				margin-bottom: 20px;
// 			}
// 			canvas {
// 				width: 100% !important; /* Ensure charts fit within the page width */
// 				height: auto !important;
// 			}
// 			@page {
// 				size: auto;
// 				margin: 20mm; /* Adjust margins to fit content */
// 			}
// 			h2 {
// 				font-size: 18pt;
// 				font-weight: bold;
// 				padding-bottom: 10px;
// 			}
// 		}

// 	`
// 	document.head.appendChild(style)

// 	window.print()

// 	window.onafterprint = () => {
// 		document.body.removeChild(printSection)
// 		document.head.removeChild(style)
// 	}
// }

const triggerPrint = async () => {
	if (!(await preparePrintContent())) return
	const printIframe = document.createElement('iframe')
	printIframe.style.position = 'absolute'
	printIframe.style.width = '0'
	printIframe.style.height = '0'
	printIframe.style.border = 'none'
	document.body.appendChild(printIframe)
	const printDoc = printIframe.contentWindow?.document
	if (!printDoc) {
		console.error('Failed to access print iframe document.')
		return
	}
	printDoc.open()
	printDoc.write(`
        <html>
        <head>
            <title>Print ${selectedField.value}</title>
            <style>
                @media print {
                    body * {
                        visibility: hidden;
						font-family: Open sans, sans-serif;
                    }
                    #printSection, #printSection * {
                        visibility: visible;
                    }
                    #printSection {
                        position: absolute;
                        left: 0;
                        top: 0;
                        width: 100%;
                    }
                    .chart-container {
                        page-break-inside: avoid; /* Prevent splitting graphs */
                        break-inside: avoid;
                        margin-bottom: 20px;
                    }
                    .headings {
                        display: flex;
                        flex-direction: row;
                        justify-content: space-between;
                        margin-bottom: 20px;
						align-items: center;
                    }
                    canvas {
                        width: 100% !important; /* Ensure charts fit within the page width */
                        height: auto !important;
                    }
                    @page {
                        size: auto;
                        margin: 20mm; /* Adjust margins to fit content */
                    }
                    h1 {
                        font-size: 24pt;
                        font-weight: bold;
                        margin-bottom: 10px;
                    }
                    h2 {
                        font-size: 18pt;
                        font-weight: bold;
                        padding-bottom: 10px;
                        margin-bottom: 8px;
                    }
                    h3 {
                        font-size: 14pt;
                        font-weight: normal;
                        margin-bottom: 5px;
                    }
                }
            </style>
        </head>
        <body>
            <div id="printSection">
                ${printContent.value}
            </div>
        </body>
        </html>
    `)
	printDoc.close()
	printIframe.onload = () => {
		if (printIframe.contentWindow) {
			printIframe.contentWindow.focus()
			printIframe.contentWindow.print()
		}
	}
	printIframe.contentWindow.onafterprint = () => {
		document.body.removeChild(printIframe)
	}
}

const convertToCSV = (objArray: any[], headers: string[]) => {
	const array = Array.isArray(objArray) ? objArray : JSON.parse(objArray)
	let str = '\ufeff'

	str += headers.join(';') + '\r\n'

	for (let i = 0; i < array.length; i++) {
		let line = ''
		for (const column of columns) {
			const value = array[i][column.field]
			if (value !== undefined && value !== null) {
				line += String(value).replace(/;/g, ',') + ';'
			} else {
				line += ';'
			}
		}
		str += line.slice(0, -1) + '\r\n'
	}
	return str
}

const exportSelectedCSV = () => {
	const rawSelectedData = selectedDataEntries.value.map((item) => toRaw(item))
	if (rawSelectedData.length === 0) {
		toast.add({
			severity: 'error',
			summary: 'No Rows Selected',
			detail: 'Please select at least one row to export.',
			life: 3000,
		})
		return
	}
	const headerLabels = columns.map((column) => column.header)
	const csvData = convertToCSV(rawSelectedData, headerLabels)

	const blob = new Blob([csvData], { type: 'text/csv;charset=utf-8;' })
	const url = URL.createObjectURL(blob)

	const downloadLink = document.createElement('a')
	const fileName = 'Exported_DataEntries.csv'

	downloadLink.href = url
	downloadLink.setAttribute('download', fileName)
	downloadLink.style.display = 'none'
	document.body.appendChild(downloadLink)
	downloadLink.click()
	document.body.removeChild(downloadLink)
	URL.revokeObjectURL(url)
}

const selectedField = ref(null)
const uniqueFieldNames = computed(() => {
	const fieldNames = entries.value.map((entry) => entry.field_name)
	return [...new Set(fieldNames)]
})

const onCellEditInit = (event) => {
	if (userRole.value === 'data_analyst') {
		showWrongRoleError()
		return
	}
	event.data._originalValue = event.data[event.field]
}

const updateDatabase = async (data) => {
	try {
		const updateData = await $fetch('/api/updateEntry', {
			method: 'PUT',
			body: {
				field_id: data.field_id,
				date: data.date,
				soil_moisture: data.soil_moisture,
				tempmax: data.tempmax,
				tempmin: data.tempmin,
				tempmean: data.tempmean,
				pressure: data.pressure,
				humidity: data.humidity,
				dew_point: data.dew_point,
				rain: data.rain,
				uvi: data.uvi,
				soil_temperature: data.soil_temperature,
			},
		})
		if (updateData.status === 'success') {
			toast.add({ severity: 'success', summary: 'Data updated succesfully', life: 3000 })
		} else {
			throw new Error('Failed to update database')
		}
	} catch (error) {
		console.error('Error updating database:', error)
	}
}

const onCellEditComplete = async (event) => {
	let { data, newValue, field, originalEvent } = event

	if (originalEvent.type === 'keydown' && originalEvent.key === 'Enter') {
		if (data[field] !== data._originalValue) {
			data[field] = newValue
			console.log('Data updated:', data)
			await updateDatabase(data)
			delete data._originalValue
		}
	} else if (originalEvent.type === 'focusout') {
		data[field] = data._originalValue
		delete data._originalValue
	}
}

function showWrongRoleError() {
	if (userRole.value === 'data_analyst') {
		toast.add({
			severity: 'warn',
			summary: 'Access Denied',
			detail: "You don't have the required permissions to perform this action.",
			life: 3000,
		})
	}
}
const onCellEditCancel = (event) => {
	let { data, field } = event
	data[field] = data._originalValue
	delete data._originalValue
}
</script>
