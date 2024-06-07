<template>
	<DataTable
		v-model:value="entries"
		ref="dataEntries"
		paginator
		:rows="5"
		:rowsPerPageOptions="[5, 10, 20, 50, 100]"
		tableStyle="min-width: 50rem"
		paginatorTemplate="FirstPageLink PrevPageLink CurrentPageReport NextPageLink LastPageLink RowsPerPageDropdown"
		currentPageReportTemplate="{first} to {last} of {totalRecords}"
		v-model:selection="selectedDataEntries"
		:selectAll="selectAll"
		@select-all-change="onSelectAllChange"
		@row-select="onRowSelect"
		@row-unselect="onRowUnselect"
		v-model:filters="filters"
		:globalFilterFields="[
			'entry_id',
			'created_at',
			'weather_temperature',
			'weather_humidity',
			'weather_uv',
			'weather_rainfall',
			'soil_moisture',
			'soil_ph',
			'soil_conductivity',
			'is_manual',
			'field_id',
		]"
	>
		<template #header>
			<div class="grid gap-2">
				<div class="flex flex-wrap items-center justify-between gap-2 sticky">
					<p class="text-xl text-900 font-bold">Data Entry Logs</p>
					<div class="flex text-xs gap-2">
						<!-- <Button label="Delete" icon="pi pi-trash" severity="danger" @click="confirmDeleteSelected" :disabled="!selectedProducts || !selectedProducts.length" /> -->
						<Button icon="pi pi-external-link" severity="secondary" label="Export" @click="exportSelectedCSV" />
						<Button icon="pi pi-print" severity="secondary" label="Print" @click="triggerPrint" />
						<NuxtLink to="/inputs/add-field-data">
							<Button icon="pi pi-upload" severity="secondary" label="Upload" />
						</NuxtLink>
						<Button icon="pi pi-refresh" rounded raised />
					</div>
				</div>
				<div class="flex justify-content-center text-xs gap-2">
					<!-- <Button type="button" icon="pi pi-filter-slash" label="Clear" outlined @click="clearFilter()" /> -->
					<IconField iconPosition="left">
						<InputIcon>
							<i class="pi pi-search" />
						</InputIcon>
						<InputText v-model="filters['global'].value" placeholder="Keyword Search" />
					</IconField>
				</div>
			</div>
		</template>
		<template #empty> <p class="text-red-500">No data entries found.</p> </template>
		<template #loading> Loading data entries. Please wait.</template>
		<Column selectionMode="multiple" headerStyle="width: 3rem"></Column>
		<!-- <Column v-for="col of columns" :key="col.field" :field="col.field" :header="col.header" sortable></Column> -->
		<Column
			v-for="col of columns.filter((c) => c.field !== 'is_manual')"
			:key="col.field"
			:field="col.field"
			:header="col.header"
			sortable
		></Column>
		<Column field="is_manual" header="Manual Entry" dataType="boolean" sortable>
			<template #body="{ data }">
				<i
					class="pi"
					:class="{ 'pi-check-circle text-green-500': data.is_manual, 'pi-times-circle text-red-400': !data.is_manual }"
				></i>
			</template>
			<template #filter="{ filterModel, filterCallback }">
				<TriStateCheckbox v-model="filterModel.value" @change="filterCallback()" />
			</template>
		</Column>
	</DataTable>
	<Dialog header="Selected Rows" v-model:visible="dialogVisible" :modal="true" :closable="true">
		<Button label="Print" icon="pi pi-print" @click="triggerPrint" />
		<pre>{{ printableContent }}</pre>
	</Dialog>
	<Toast />
</template>

<script setup lang="ts">
import { ref, toRaw } from 'vue'
import { FilterMatchMode } from 'primevue/api'
import { useToast } from 'primevue/usetoast'

const selectedDataEntries = ref([])
const dialogVisible = ref(false)
const printableContent = ref('')
const dataEntries = ref()
const toast = useToast()

class Entry {
	entry_id: number = 0
	created_at: Date = new Date()
	weather_temperature: number = 0
	weather_humidity: number = 0
	weather_uv: number = 0
	weather_rainfall: number = 0
	soil_moisture: number = 0
	soil_ph: number = 0
	soil_conductivity: number = 0
	is_manual: boolean = false
	field_id: number = 0
}

const entries = ref<Entry[]>([])
const columns = [
	{ field: 'entry_id', header: 'Entry ID' },
	{ field: 'created_at', header: 'Created At' },
	{ field: 'weather_temperature', header: 'Temperature' },
	{ field: 'weather_humidity', header: 'Humidity' },
	{ field: 'weather_uv', header: 'UV Index' },
	{ field: 'weather_rainfall', header: 'Rainfall' },
	{ field: 'soil_moisture', header: 'Moisture' },
	{ field: 'soil_ph', header: 'pH' },
	{ field: 'soil_conductivity', header: 'Conductivity' },
	{ field: 'is_manual', header: 'Manual Entry' },
	{ field: 'field_id', header: 'Field ID' },
]

for (let i = 0; i < 100; i++) {
	entries.value.push({
		entry_id: i,
		created_at: new Date(),
		weather_temperature: parseFloat((Math.random() * 100).toFixed(2)),
		weather_humidity: parseFloat((Math.random() * 100).toFixed(2)),
		weather_uv: parseFloat((Math.random() * 10).toFixed(2)),
		weather_rainfall: parseFloat((Math.random() * 100).toFixed(2)),
		soil_moisture: parseFloat((Math.random() * 100).toFixed(2)),
		soil_ph: parseFloat((Math.random() * 14).toFixed(2)),
		soil_conductivity: parseFloat((Math.random() * 100).toFixed(2)),
		is_manual: Math.random() > 0.5,
		field_id: Math.floor(Math.random() * 10),
	})
}

const filters = ref({
	global: { value: null, matchMode: FilterMatchMode.CONTAINS },
	entry_id: { value: null, matchMode: FilterMatchMode.EQUALS },
	created_at: { value: null, matchMode: FilterMatchMode.DATE_IS },
	weather_temperature: { value: null, matchMode: FilterMatchMode.EQUALS },
	weather_humidity: { value: null, matchMode: FilterMatchMode.EQUALS },
	weather_uv: { value: null, matchMode: FilterMatchMode.EQUALS },
	weather_rainfall: { value: null, matchMode: FilterMatchMode.EQUALS },
	soil_moisture: { value: null, matchMode: FilterMatchMode.EQUALS },
	soil_ph: { value: null, matchMode: FilterMatchMode.EQUALS },
	soil_conductivity: { value: null, matchMode: FilterMatchMode.EQUALS },
	is_manual: { value: null, matchMode: FilterMatchMode.EQUALS },
	field_id: { value: null, matchMode: FilterMatchMode.EQUALS },
})

const onSort = (event) => {
	lazyParams.value = event
	loadLazyData(event)
}

const selectAll = ref(false)

const onSelectAllChange = (event) => {
	selectAll.value = event.checked

	if (selectAll.value) {
		CustomerService.getCustomers().then((data) => {
			selectAll.value = true
			selectedDataEntries.value = data.customers
		})
	} else {
		selectAll.value = false
		selectedDataEntries.value = []
	}
}

const onRowSelect = () => {
	const rawSelectedData = selectedDataEntries.value.map((item) => toRaw(item))
	selectAll.value = selectedDataEntries.value.length === totalRecords.value
}

const onRowUnselect = () => {
	selectAll.value = false
}

const exportSelectedCSV = () => {
	const rawSelectedData = selectedDataEntries.value.map((item) => toRaw(item))
	if (rawSelectedData.length === 0) {
		toast.add({
			severity: 'warn',
			summary: 'No Entries Selected',
			detail: 'Please select at least one entry to export.',
			life: 3000,
		})
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

const convertToCSV = (objArray, headers) => {
	const array = typeof objArray !== 'object' ? JSON.parse(objArray) : objArray
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

const triggerPrint = () => {
	const rawSelectedData = selectedDataEntries.value.map((item) => toRaw(item))
	if (rawSelectedData.length === 0) {
		toast.add({
			severity: 'warn',
			summary: 'No Entries Selected',
			detail: 'Please select at least one entry to print.',
			life: 3000,
		})
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
</script>
