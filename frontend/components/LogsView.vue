<template>
	<DataTable
		v-model:value="entries"
		ref="dataEntries"
		scrollable
		scrollHeight="450px"
		size="small"
		class="bg-surface-100 dark:bg-surface-800 rounded-md"
		paginator
		:rows="5"
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
						<Button icon="pi pi-print" severity="secondary" label="Print" @click="triggerPrint" />
						<Button icon="pi pi-upload" severity="secondary" label="Upload" />
						<Button icon="pi pi-refresh" rounded raised @click="fetchEntryData" />
					</div>
				</div>
				<div class="flex justify-content-center text-xs gap-2">
					<IconField iconPosition="left">
						<InputIcon>
							<i class="pi pi-search" />
						</InputIcon>
						<InputText v-model="filters['global'].value" placeholder="Keyword Search" />
					</IconField>
				</div>
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
		<Column selectionMode="multiple" headerStyle="width: 3rem"></Column>
		<Column v-for="col of columns" :key="col.field" :field="col.field" :header="col.header" sortable></Column>
	</DataTable>
	<Dialog header="Selected Rows" v-model:visible="dialogVisible" :modal="true" :closable="true">
		<Button label="Print" icon="pi pi-print" @click="triggerPrint" />
		<pre>{{ printableContent }}</pre>
	</Dialog>
</template>

<script setup lang="ts">
import { ref, toRaw, onMounted } from 'vue'
import { FilterMatchMode } from 'primevue/api'

const selectedDataEntries = ref([])
const dialogVisible = ref(false)
const printableContent = ref('')
const dataEntries = ref()
const selectAll = ref<boolean>()

// Define your columns
const columns = [
	{ field: 'date', header: 'Date' },
	{ field: 'field_name', header: 'Field Name' },
	{ field: 'crop_type', header: 'Crop Type' },
	{ field: 'tempmax', header: 'Max Temperature (°C)' },
	{ field: 'tempmin', header: 'Min Temperature (°C)' },
	{ field: 'tempmean', header: 'Mean Temperature (°C)' },
	{ field: 'pressure', header: 'Pressure (hPa)' },
	{ field: 'humidity', header: 'Humidity (%)' },
	{ field: 'dew_point', header: 'Dew Point (°C)' },
	{ field: 'rain', header: 'Rainfall (mm)' },
	{ field: 'uvi', header: 'UV Index' },
	{ field: 'soil_moisture', header: 'Soil Moisture' },
	{ field: 'soil_temperature', header: 'Soil Temperature (°C)' },
	{ field: 'pred_health', header: 'Health Index' },
	{ field: 'pred_yield', header: 'Yield' },
	{ field: 'pred_sprayability', header: 'Sprayability' },
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

	console.log(entryData)

	entries.value = entryData.map((entry: any) => ({
		...entry,
		yield: entry.pred_yield === null ? 'N/A' : entry.pred_yield.toFixed(2),
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

const exportSelectedCSV = () => {
	const rawSelectedData = selectedDataEntries.value.map((item) => toRaw(item))
	if (rawSelectedData.length === 0) {
		return
	}
	const headerLabels = columns.map((column) => column.header)
	const csvData = convertToCSV(rawSelectedData, headerLabels)

	const downloadLink = document.createElement('a')
	const fileName = 'Exported_DataEntries.csv'

	downloadLink.setAttribute('href', `data:text/csv;charset=utf-8,${encodeURIComponent(csvData)}`)
	downloadLink.setAttribute('download', fileName)
	downloadLink.style.display = 'none'

	document.body.appendChild(downloadLink)
	downloadLink.click()
	document.body.removeChild(downloadLink)
}

const triggerPrint = () => {
	const rawSelectedData = selectedDataEntries.value.map((item) => toRaw(item))
	if (rawSelectedData.length === 0) {
		return
	}
	const printContents = JSON.stringify(rawSelectedData, null, 2)
	const printWindow = window.open('', '', 'height=600,width=800')
	if (!printWindow) {
		return
	}
	printWindow.document.write('<html><head><title>Print</title></head><body>')
	printWindow.document.write('<pre>' + printContents + '</pre>')
	printWindow.document.write('</body></html>')
	printWindow.onbeforeunload = function () {
		printWindow.close()
	}
	printWindow.document.close()
	printWindow.print()
	printWindow.close()
}

const convertToCSV = (objArray: any[], headers: string[]) => {
	const array = Array.isArray(objArray) ? objArray : JSON.parse(objArray)
	let str = ''

	// Add headers as the first row
	str += headers.map((header) => `"${header}"`).join(',') + '\r\n'

	for (let i = 0; i < array.length; i++) {
		let line = ''
		for (const key in array[i]) {
			// eslint-disable-next-line no-prototype-builtins
			if (array[i].hasOwnProperty(key)) {
				line += `"${array[i][key]}",`
			}
		}
		str += line.slice(0, -1) + '\r\n'
	}
	return str
}
</script>
