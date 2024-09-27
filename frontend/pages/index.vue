<template>
	<div class="flex w-full justify-center items-center">
		<div v-if="loading" class="flex flex-col items-center justify-center gap-4 mt-20">
			<ProgressSpinner />
			<h2 class="dark:text-white font-bold">Fetching your data...</h2>
		</div>
		<div v-else class="flex flex-col justify-start items-start gap-4 w-full">
			<div v-if="userFieldsWithData.length === 0">
				<p class="text-surface-700 dark:text-surface-0">
					You have no fields available. Start adding fields on the
					<NuxtLink to="/inputs/add-field" class="underline">Add Field Page.</NuxtLink>
				</p>
			</div>
			<div class="flex flex-col md:flex-row w-full gap-5">
				<div class="w-full lg:w-1/3">
					<FieldCard v-model="selectedField" :fields="userFieldsWithData" />
				</div>
				<div class="w-full lg:w-2/3 h-96 md:h-auto rounded-md shadow-md overflow-hidden">
					<GoogleMapsField
						:selectedField="selectedField"
						:fields="userFieldsWithData"
						@update:selectedField="updateSelectedField"
					/>
				</div>
			</div>
			<div class="w-full">
				<Panel
					:header="!selectedField ? 'Select a field to view stats' : 'More Field Stats'"
					:toggleable="!selectedField ? false : true"
					collapsed
				>
					<div class="w-full flex flex-col justify-center items-center gap-4 relative">
						<div class="flex w-full gap-4 mol:flex-row mos:flex-col justify-between items-center">
							<SelectButton
								v-model="selectedFilterOption"
								:options="filterOptions"
								optionLabel="name"
								optionDisabled="constant"
								@change="handleFilterChange"
							/>
							<Button icon="pi pi-question-circle" outlined severity="secondary" size="small" class="h-full" />
						</div>
						<div v-if="selectedField" class="grid gap-4 w-full" :class="getGridClass(filter.value)">
							<StatsCard
								v-for="(chartData, key) in chartDataList"
								:key="key"
								:title="chartData.title"
								:chartData="chartData.chartData"
							/>
						</div>
					</div>
				</Panel>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import FieldCard from '~/components/FieldCard.vue'
import GoogleMapsField from '~/components/GoogleMapsField.vue'
import StatsCard from '~/components/StatsCard.vue'
import { useFieldData } from '~/composables/useFieldData'
import { updateChartData, getGridClass } from '~/utils/chartDataUtils'

const { userFieldsWithData, filterOptions, chartDataList, loading } = useFieldData()

const selectedField = ref(null)
const filter = ref({ name: '8 Days', value: 8, constant: false })
const selectedFilterOption = ref(filter.value)
const screenWidth = ref(0)

watch(filter, (newFilter) => {
	if (selectedField.value) {
		if (filter.value === null) {
			filter.value = {}
		}
		updateChartData(selectedField.value, newFilter.value, chartDataList)
	}
})

const handleFilterChange = (e) => {
	if (e.value !== null) {
		filter.value = e.value
		selectedFilterOption.value = e.value
	} else {
		// If e.value is null, it means the same option was selected again
		// So we force the SelectButton to keep the current selection
		selectedFilterOption.value = filter.value
	}
}

watch(selectedField, async (newField) => {
	if (newField && newField.data) {
		filter.value = { name: '8 Days', value: 8, constant: false }
		selectedFilterOption.value = filter.value
		updateChartData(newField, filter.value.value, chartDataList)
		await nextTick()
		updateFilterOptions()
	} else {
		Object.keys(chartDataList).forEach((key) => {
			if (chartDataList[key]) {
				chartDataList[key].chartData = {}
			}
		})
	}
})

function updateSelectedField(newField) {
	selectedField.value = newField
}

function checkLargeDateValues() {
	return !(selectedField.value?.data?.['date']?.length >= 30 && screenWidth.value >= 650)
}

function checkMediumDateValues() {
	return !(selectedField.value?.data?.['date']?.length >= 14 && screenWidth.value >= 650)
}

function updateFilterOptions() {
	filterOptions.value = [
		{ name: '8 Days', value: 8, constant: false },
		{ name: '14 Days', value: 14, constant: checkMediumDateValues() },
		{ name: '30 Days', value: 30, constant: checkLargeDateValues() },
	]
}

onMounted(() => {
	updateFilterOptions()

	screenWidth.value = window.innerWidth
	window.addEventListener('resize', () => {
		screenWidth.value = window.innerWidth
		filterOptions.value[2].constant = window.innerWidth < 650
	})
})

definePageMeta({
	middleware: 'auth',
})
</script>
