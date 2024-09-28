<template>
	<div v-if="loading" class="w-full h-full mt-48 gap-5 flex flex-col items-center justify-center">
		<ProgressSpinner />
		<h2 class="dark:text-white font-bold">Fetching Market Data...</h2>
	</div>

	<div v-else class="w-full">
		<Dropdown v-model="selectedCrop" :options="cropOptions" optionLabel="label" class="mb-4 w-full md:w-64" />

		<h2 v-if="noFieldsMessage" class="mb-4 text-surface-900 dark:text-surface-0 font-bold text-lg">
			{{ noFieldsMessage }}
		</h2>

		<div class="grid gap-4 grid-cols-1 sm:grid-cols-2">
			<MarketHectareCard
				:title="`${selectedCrop.label} Hectare`"
				:hectare="cropData.hectare"
				:footer="`Total hectare of team ${selectedCrop.label.toLowerCase()} fields`"
			/>
			<MarketDataCard
				:title="`${selectedCrop.label} t/ha`"
				:tph="cropData.yield"
				:footer="`Combined t/ha of team ${selectedCrop.label.toLowerCase()} fields`"
			/>
		</div>

		<div
			v-if="chartData"
			class="gap-4 bg-surface-100 dark:bg-surface-800 p-5 rounded-md shadow-md w-full flex flex-col justify-between items-center mt-4"
		>
			<Chart type="bar" :data="chartData" :options="chartOptions" class="w-full h-[500px] lg:h-[650px]" />
		</div>
	</div>
</template>

<script setup>
import { onMounted, watch } from 'vue'
import { useMarketData } from '~/composables/useMarketData'
import { useCropData } from '~/composables/useCropData'
import MarketHectareCard from '~/components/MarketHectareCard.vue'
import MarketDataCard from '~/components/MarketDataCard.vue'
import Chart from 'primevue/chart'

const marketData = useMarketData()
const { loading, cropOptions, selectedCrop, chartData, chartOptions } = marketData
const { cropData, noFieldsMessage, fetchCropData } = useCropData(selectedCrop)

onMounted(async () => {
	await Promise.all([marketData.fetchMarketData(), fetchCropData()])
	updateChartData()
})

watch(selectedCrop, updateChartData)

function updateChartData() {
	marketData.generateChartData(cropData.value)
}
</script>
