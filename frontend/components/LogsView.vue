<template>
	<Toast />
	<DataTable
		v-model:value="entries"
		ref="dataEntries"
		scrollable
		scrollHeight="450px"
		size="small"
		paginator
		@cell-edit-complete="onCellEditComplete"
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
						<Button icon="pi pi-print" severity="secondary" label="Print" @click="visible = true" />
					</div>
				</div>
				<Dialog v-model:visible="visible" modal header="Print" :style="{ width: '25rem' }">
					<span class="text-surface-500 dark:text-surface-400 block mb-8"
						>Which farms data would you like to Print?</span
					>

					<div class="flex items-center gap-4 mb-8">
						<div class="card flex justify-content-center">
							<Dropdown
								v-model="selectedField"
								:options="uniqueFieldNames"
								placeholder="Select a Field"
								class="w-full md:w-14rem"
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
				<p class="text-xs text-surface-600 dark:text-surface-0/60">
					(To change table values, select the value you wish to change, then enter the correct value and hit 'Enter'.
					You will receive a prompt if the new value was saved successfully. (Note: You cannot change the Date, Field
					Name, Crop Type, Health, Yield or Sprayability values))
				</p>
			</div>
		</template>
		<template #empty>
			<Skeleton height="20px"></Skeleton>
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
					<InputNumber v-model="data[field]" autofocus size="small" :minFractionDigits="0" :maxFractionDigits="10" />
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
	{ field: 'uvi', header: 'UV Index' },
	{ field: 'soil_moisture', header: 'Soil Moisture' },
	{ field: 'soil_temperature', header: 'Soil Temp (°C)' },
	{ field: 'health', header: 'Health Index' },
	{ field: 'yield', header: 'Yield' },
	{ field: 'sprayability', header: 'Sprayability' },
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

const fetchEntryData = async () => {
	const user = useSupabaseUser()

	const teamID = await $fetch('/api/getTeamID', {
		params: { userid: user?.value?.id },
	})

	const entryData = await $fetch('/api/getTeamFieldData', {
		params: { team_id: teamID.team_id },
	})

	entries.value = entryData.map((entry: any) => ({
		...entry,
		yield: entry.yield === null ? 'N/A' : entry.yield.toFixed(2),
	}))
}

onMounted(() => {
	fetchEntryData()
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
					borderColor: 'red',
					fill: false,
				},
				{
					label: 'Mean Temperature',
					data: tempMeanData,
					borderColor: 'orange',
					fill: false,
				},
				{
					label: 'Min Temperature',
					data: tempMinData,
					borderColor: 'blue',
					fill: false,
				},
			],
		},
		options: {
			responsive: false,
			animation: false,
			title: {
				display: true,
				text: `Temperature Data for ${selectedField.value}`,
			},
		},
	})
	const chart1 = new Chart(canvas1, {
		type: 'line',
		data: {
			labels: labels,
			datasets: [
				{
					label: 'Max Temperature',
					data: tempMaxData,
					borderColor: 'red',
					fill: false,
				},
				{
					label: 'Mean Temperature',
					data: tempMeanData,
					borderColor: 'orange',
					fill: false,
				},
				{
					label: 'Min Temperature',
					data: tempMinData,
					borderColor: 'blue',
					fill: false,
				},
			],
		},
		options: {
			responsive: false,
			animation: false,
			title: {
				display: true,
				text: `Temperature Data for ${selectedField.value}`,
			},
		},
	})
	const chart2 = new Chart(canvas2, {
		type: 'line',
		data: {
			labels: labels,
			datasets: [
				{
					label: 'Max Temperature',
					data: tempMaxData,
					borderColor: 'red',
					fill: false,
				},
				{
					label: 'Mean Temperature',
					data: tempMeanData,
					borderColor: 'orange',
					fill: false,
				},
				{
					label: 'Min Temperature',
					data: tempMinData,
					borderColor: 'blue',
					fill: false,
				},
			],
		},
		options: {
			responsive: false,
			animation: false,
			title: {
				display: true,
				text: `Temperature Data for ${selectedField.value}`,
			},
		},
	})
	const chart3 = new Chart(canvas3, {
		type: 'line',
		data: {
			labels: labels,
			datasets: [
				{
					label: 'Max Temperature',
					data: tempMaxData,
					borderColor: 'red',
					fill: false,
				},
				{
					label: 'Mean Temperature',
					data: tempMeanData,
					borderColor: 'orange',
					fill: false,
				},
				{
					label: 'Min Temperature',
					data: tempMinData,
					borderColor: 'blue',
					fill: false,
				},
			],
		},
		options: {
			responsive: false,
			animation: false,
			title: {
				display: true,
				text: `Temperature Data for ${selectedField.value}`,
			},
		},
	})
	const chart4 = new Chart(canvas4, {
		type: 'line',
		data: {
			labels: labels,
			datasets: [
				{
					label: 'Max Temperature',
					data: tempMaxData,
					borderColor: 'red',
					fill: false,
				},
				{
					label: 'Mean Temperature',
					data: tempMeanData,
					borderColor: 'orange',
					fill: false,
				},
				{
					label: 'Min Temperature',
					data: tempMinData,
					borderColor: 'blue',
					fill: false,
				},
			],
		},
		options: {
			responsive: false,
			animation: false,
			title: {
				display: true,
				text: `Temperature Data for ${selectedField.value}`,
			},
		},
	})
	const chart5 = new Chart(canvas5, {
		type: 'line',
		data: {
			labels: labels,
			datasets: [
				{
					label: 'Max Temperature',
					data: tempMaxData,
					borderColor: 'red',
					fill: false,
				},
				{
					label: 'Mean Temperature',
					data: tempMeanData,
					borderColor: 'orange',
					fill: false,
				},
				{
					label: 'Min Temperature',
					data: tempMinData,
					borderColor: 'blue',
					fill: false,
				},
			],
		},
		options: {
			responsive: false,
			animation: false,
			title: {
				display: true,
				text: `Temperature Data for ${selectedField.value}`,
			},
		},
	})
	const chart6 = new Chart(canvas6, {
		type: 'line',
		data: {
			labels: labels,
			datasets: [
				{
					label: 'Max Temperature',
					data: tempMaxData,
					borderColor: 'red',
					fill: false,
				},
				{
					label: 'Mean Temperature',
					data: tempMeanData,
					borderColor: 'orange',
					fill: false,
				},
				{
					label: 'Min Temperature',
					data: tempMinData,
					borderColor: 'blue',
					fill: false,
				},
			],
		},
		options: {
			responsive: false,
			animation: false,
			title: {
				display: true,
				text: `Temperature Data for ${selectedField.value}`,
			},
		},
	})
	const chart7 = new Chart(canvas7, {
		type: 'line',
		data: {
			labels: labels,
			datasets: [
				{
					label: 'Max Temperature',
					data: tempMaxData,
					borderColor: 'red',
					fill: false,
				},
				{
					label: 'Mean Temperature',
					data: tempMeanData,
					borderColor: 'orange',
					fill: false,
				},
				{
					label: 'Min Temperature',
					data: tempMinData,
					borderColor: 'blue',
					fill: false,
				},
			],
		},
		options: {
			responsive: false,
			animation: false,
			title: {
				display: true,
				text: `Temperature Data for ${selectedField.value}`,
			},
		},
	})
	const chart8 = new Chart(canvas8, {
		type: 'line',
		data: {
			labels: labels,
			datasets: [
				{
					label: 'Max Temperature',
					data: tempMaxData,
					borderColor: 'red',
					fill: false,
				},
				{
					label: 'Mean Temperature',
					data: tempMeanData,
					borderColor: 'orange',
					fill: false,
				},
				{
					label: 'Min Temperature',
					data: tempMinData,
					borderColor: 'blue',
					fill: false,
				},
			],
		},
		options: {
			responsive: false,
			animation: false,
			title: {
				display: true,
				text: `Temperature Data for ${selectedField.value}`,
			},
		},
	})
	const chart9 = new Chart(canvas9, {
		type: 'line',
		data: {
			labels: labels,
			datasets: [
				{
					label: 'Max Temperature',
					data: tempMaxData,
					borderColor: 'red',
					fill: false,
				},
				{
					label: 'Mean Temperature',
					data: tempMeanData,
					borderColor: 'orange',
					fill: false,
				},
				{
					label: 'Min Temperature',
					data: tempMinData,
					borderColor: 'blue',
					fill: false,
				},
			],
		},
		options: {
			responsive: false,
			animation: false,
			title: {
				display: true,
				text: `Temperature Data for ${selectedField.value}`,
			},
		},
	})
	const chart10 = new Chart(canvas10, {
		type: 'line',
		data: {
			labels: labels,
			datasets: [
				{
					label: 'Max Temperature',
					data: tempMaxData,
					borderColor: 'red',
					fill: false,
				},
				{
					label: 'Mean Temperature',
					data: tempMeanData,
					borderColor: 'orange',
					fill: false,
				},
				{
					label: 'Min Temperature',
					data: tempMinData,
					borderColor: 'blue',
					fill: false,
				},
			],
		},
		options: {
			responsive: false,
			animation: false,
			title: {
				display: true,
				text: `Temperature Data for ${selectedField.value}`,
			},
		},
	})

	// Wait for the chart to render
	await new Promise((resolve) => setTimeout(resolve, 100))

	// Convert the chart to an image
	const chartImage = canvas.toDataURL('image/png')
	const chartImage1 = canvas.toDataURL('image1/png')
	const chartImage2 = canvas.toDataURL('image2/png')
	const chartImage3 = canvas.toDataURL('image3/png')
	const chartImage4 = canvas.toDataURL('image4/png')
	const chartImage5 = canvas.toDataURL('image5/png')
	const chartImage6 = canvas.toDataURL('image6/png')
	const chartImage7 = canvas.toDataURL('image7/png')
	const chartImage8 = canvas.toDataURL('image8/png')
	const chartImage9 = canvas.toDataURL('image9/png')
	const chartImage10 = canvas.toDataURL('image10/png')

	// Remove the canvas from the DOM
	document.body.removeChild(canvas)

	// Prepare the print content
	printContent.value = `
    <h1>Field: ${selectedField.value}</h1>
    <h2>Crop Type: ${fieldEntries[0].crop_type}</h2>
	<div>
		<h3>Temperature Chart</h3>
		<img src="${chartImage}" alt="Temperature Chart" style="width: 100%; max-width: 800px;"></div>
		<div>
		<h3>Pressure Chart</h3>
		<img src="${chartImage1}" alt="Pressure Chart" style="width: 100%; max-width: 800px;"></div><div>
		<h3>Humidity Chart</h3>
		<img src="${chartImage2}" alt="Humidity Chart" style="width: 100%; max-width: 800px;"></div><div>
		<h3>Dew Point Chart</h3>
		<img src="${chartImage3}" alt="Dew Point Chart" style="width: 100%; max-width: 800px;"></div><div>
		<h3>Rainfall Chart</h3>
		<img src="${chartImage4}" alt="Rainfall Chart" style="width: 100%; max-width: 800px;"></div><div>
		<h3>UV Index Chart</h3>
		<img src="${chartImage5}" alt="UV Index Chart" style="width: 100%; max-width: 800px;"></div><div>
		<h3>Soil Moisture Chart</h3>
		<img src="${chartImage6}" alt="Soil Moisture Chart" style="width: 100%; max-width: 800px;"></div><div>
		<h3>Soil Temperature Chart</h3>
		<img src="${chartImage7}" alt="Soil Temperature Chart" style="width: 100%; max-width: 800px;"></div><div>
		<h3>Health Index Chart</h3>
		<img src="${chartImage8}" alt="Health Index Chart" style="width: 100%; max-width: 800px;"></div><div>
		<h3>Yield Chart</h3>
		<img src="${chartImage9}" alt="Yield Chart" style="width: 100%; max-width: 800px;"></div><div>
		<h3>Sprayability Chart</h3>
		<img src="${chartImage10}" alt="Sprayability Chart" style="width: 100%; max-width: 800px;"></div>
  `
	return true
}

const triggerPrint = async () => {
	if (!(await preparePrintContent())) return
	const printWindow = window.open('', '_blank')
	if (!printWindow) {
		alert('Please allow pop-ups for this website to enable printing.')
		return
	}
	printWindow.document.write(`
    <html>
      <head>
        <title>Print ${selectedField.value}</title>
      </head>
      <body>
        ${printContent.value}
      </body>
    </html>
  `)
	printWindow.document.close()
	printWindow.focus()
	setTimeout(() => {
		printWindow.print()
		printWindow.close()
	}, 500)
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
			summary: 'No fields selected',
			detail: 'Please select atleast one field to export',
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

const onCellEditComplete = (event) => {
	let { data, newValue, field } = event

	data[field] = newValue
	toast.add({ severity: 'success', summary: 'Data changed successfully', life: 3000 })
}

const selectedField = ref()
const uniqueFieldNames = computed(() => {
	const fieldNames = entries.value.map((entry) => entry.field_name)
	return [...new Set(fieldNames)]
})
</script>
