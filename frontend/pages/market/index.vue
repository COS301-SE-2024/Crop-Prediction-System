<template>
	<Dropdown v-model="selectedCrop" :options="cropOptions" optionLabel="label" class="mb-4 w-full md:w-64" />
	<h2
		v-show="selectedCrop.value === 'Wheat' && noFieldsMessages.wheat !== ''"
		class="mb-4 text-surface-900 dark:text-surface-0 font-bold text-lg"
	>
		You have no registered Wheat fields.
	</h2>
	<h2
		v-show="selectedCrop.value === 'Maize' && noFieldsMessages.wheat !== ''"
		class="mb-4 text-surface-900 dark:text-surface-0 font-bold text-lg"
	>
		You have no registered Maize fields.
	</h2>
	<h2
		v-show="selectedCrop.value === 'Soybeans' && noFieldsMessages.soybeans !== ''"
		class="mb-4 text-surface-900 dark:text-surface-0 font-bold text-lg"
	>
		You have no registered Soybean fields.
	</h2>
	<h2
		v-show="selectedCrop.value === 'Sunflower' && noFieldsMessages.sunflower !== ''"
		class="mb-4 text-surface-900 dark:text-surface-0 font-bold text-lg"
	>
		You have no registered Sunflower fields.
	</h2>
	<h2
		v-show="selectedCrop.value === 'Oats' && noFieldsMessages.oats !== ''"
		class="mb-4 text-surface-900 dark:text-surface-0 font-bold text-lg"
	>
		You have no registered Oats fields.
	</h2>
	<h2
		v-show="selectedCrop.value === 'Sorghum' && noFieldsMessages.sorghum !== ''"
		class="mb-4 text-surface-900 dark:text-surface-0 font-bold text-lg"
	>
		You have no registered Sorghum fields.
	</h2>
	<h2
		v-show="selectedCrop.value === 'Barley' && noFieldsMessages.barley !== ''"
		class="mb-4 text-surface-900 dark:text-surface-0 font-bold text-lg"
	>
		You have no registered Barley fields.
	</h2>
	<h2
		v-show="selectedCrop.value === 'Canola' && noFieldsMessages.canola !== ''"
		class="mb-4 text-surface-900 dark:text-surface-0 font-bold text-lg"
	>
		You have no registered Canola fields.
	</h2>
	<h2
		v-show="selectedCrop.value === 'Groundnuts' && noFieldsMessages.groundnuts !== ''"
		class="mb-4 text-surface-900 dark:text-surface-0 font-bold text-lg"
	>
		You have no registered Groundnuts fields.
	</h2>
	<div class="grid gap-4 grid-cols-1 sm:grid-cols-2">
		<MarketHectareCard
			v-show="selectedCrop.value === 'Wheat'"
			title="Wheat Hectare"
			:hectare="teamWheatHectare"
			footer="Total hectare of team wheat fields"
		/>
		<MarketDataCard
			v-show="selectedCrop.value === 'Wheat'"
			title="Wheat t/ha"
			:tph="teamWheatYield"
			footer="Combined t/ha of team wheat fields"
		/>
		<MarketHectareCard
			v-show="selectedCrop.value === 'Maize'"
			title="Maize Hectare"
			:hectare="teamMaizeHectare"
			footer="Total hectare of team maize fields"
		/>
		<MarketDataCard
			v-show="selectedCrop.value === 'Maize'"
			title="Maize t/ha"
			:tph="teamMaizeYield"
			footer="Combined t/ha of team maize fields"
		/>
		<MarketHectareCard
			v-show="selectedCrop.value === 'Soybeans'"
			title="Soybeans Hectare"
			:hectare="teamSoyHectare"
			footer="Total hectare of team soybean fields"
		/>
		<MarketDataCard
			v-show="selectedCrop.value === 'Soybeans'"
			title="Soybeans t/ha"
			:tph="teamSoyYield"
			footer="Combined t/ha of team soybean fields"
		/>
		<MarketHectareCard
			v-show="selectedCrop.value === 'Sunflower'"
			title="Sunflower Hectare"
			:hectare="teamSunflowerHectare"
			footer="Total hectare of team Sunflower fields"
		/>
		<MarketDataCard
			v-show="selectedCrop.value === 'Sunflower'"
			title="Sunflower t/ha"
			:tph="teamSunflowerYield"
			footer="Combined t/ha of team sunflower fields"
		/>
		<MarketDataCard
			v-show="selectedCrop.value === 'Oats'"
			title="Oats t/ha"
			:tph="teamOatsYield"
			footer="Combined t/ha of team oats fields"
		/>
		<MarketHectareCard
			v-show="selectedCrop.value === 'Oats'"
			title="Oats Hectare"
			:hectare="teamOatsHectare"
			footer="Total hectare of team oats fields"
		/>
		<MarketDataCard
			v-show="selectedCrop.value === 'Sorghum'"
			title="Sorghum t/ha"
			:tph="teamSorghumYield"
			footer="Combined t/ha of team sorghum fields"
		/>
		<MarketHectareCard
			v-show="selectedCrop.value === 'Sorghum'"
			title="Sorghum Hectare"
			:hectare="teamSorghumHectare"
			footer="Total hectare of team sorghum fields"
		/>
		<MarketDataCard
			v-show="selectedCrop.value === 'Barley'"
			title="Barley t/ha"
			:tph="teamBarleyYield"
			footer="Combined t/ha of team barley fields"
		/>
		<MarketHectareCard
			v-show="selectedCrop.value === 'Barley'"
			title="Barley Hectare"
			:hectare="teamBarleyHectare"
			footer="Total hectare of team barley fields"
		/>
		<MarketDataCard
			v-show="selectedCrop.value === 'Canola'"
			title="Canola t/ha"
			:tph="teamCanolaYield"
			footer="Combined t/ha of team canola fields"
		/>
		<MarketHectareCard
			v-show="selectedCrop.value === 'Canola'"
			title="Canola Hectare"
			:hectare="teamCanolaHectare"
			footer="Total hectare of team canola fields"
		/>
		<MarketDataCard
			v-show="selectedCrop.value === 'Groundnuts'"
			title="Groundnuts t/ha"
			:tph="teamGroundnutsYield"
			footer="Combined t/ha of team groundnuts fields"
		/>
		<MarketHectareCard
			v-show="selectedCrop.value === 'Groundnuts'"
			title="Groundnuts Hectare"
			:hectare="teamGroundnutsHectare"
			footer="Total hectare of team groundnuts fields"
		/>
	</div>
	<div
		class="gap-4 bg-surface-100 dark:bg-surface-800 p-5 rounded-md shadow-md w-full flex flex-col justify-between items-center mt-4"
	>
		<Chart type="bar" :data="chartData" :options="chartOptions" class="w-full h-[500px] lg:h-[650px]" />
	</div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { getTeamId } from '~/utils/apiUtils'
import {
	getMaizeMarketData,
	getWheatMarketData,
	getSoyMarketData,
	getSunflowerMarketData,
	getCropPastAverage,
	getCropMarketData,
} from '~/utils/marketUtils'
import MarketHectareCard from '~/components/MarketHectareCard.vue'
import MarketDataCard from '~/components/MarketDataCard.vue'
import Chart from 'primevue/chart'
import Dropdown from 'primevue/dropdown'

const teamYield = ref(0)
const teamWheatHectare = ref(0)
const teamWheatYield = ref(0)
const teamWheatProduction = ref(0)
const teamMaizeHectare = ref(0)
const teamMaizeYield = ref(0)
const teamMaizeProduction = ref(0)
const teamSoyHectare = ref(0)
const teamSoyYield = ref(0)
const teamSoyProduction = ref(0)
const teamSunflowerHectare = ref(0)
const teamSunflowerYield = ref(0)
const teamSunflowerProduction = ref(0)
const teamSorghumHectare = ref(0)
const teamSorghumYield = ref(0)
const teamSorghumProduction = ref(0)
const teamCanolaHectare = ref(0)
const teamCanolaYield = ref(0)
const teamCanolaProduction = ref(0)
const teamOatsHectare = ref(0)
const teamOatsYield = ref(0)
const teamOatsProduction = ref(0)
const teamBarleyHectare = ref(0)
const teamBarleyYield = ref(0)
const teamBarleyProduction = ref(0)
const teamGroundnutsHectare = ref(0)
const teamGroundnutsYield = ref(0)
const teamGroundnutsProduction = ref(0)
const wheatPastAverage = ref(0)
const maizePastAverage = ref(0)
const soyPastAverage = ref(0)
const sunflowerPastAverage = ref(0)
const oatsPastAverage = ref(0)
const canolaPastAverage = ref(0)
const barleyPastAverage = ref(0)
const sorghumPastAverage = ref(0)
const groundnutsPastAverage = ref(0)
const chartData = ref(0) // Initialize as 0
const chartOptions = ref(0)
const selectedCrop = ref({ label: 'Wheat', value: 'Wheat' }) // Default selected crop
const loading = ref(false)

// Options for the SelectButton
const cropOptions = [
	{ label: 'Wheat', value: 'Wheat' },
	{ label: 'Maize', value: 'Maize' },
	{ label: 'Soybeans', value: 'Soybeans' },
	{ label: 'Sunflower', value: 'Sunflower' },
	{ label: 'Sorghum', value: 'Sorghum' },
	{ label: 'Barley', value: 'Barley' },
	{ label: 'Canola', value: 'Canola' },
	{ label: 'Oats', value: 'Oats' },
	{ label: 'Groundnuts', value: 'Groundnuts' },
]

const wheatPriceData = ref(null)
const maizePriceData = ref(null)
const soyPriceData = ref(null)
const sunflowerPriceData = ref(null)
const oatsPriceData = ref(null)
const sorghumPriceData = ref(null)
const barleyPriceData = ref(null)
const canolaPriceData = ref(null)
const groundnutsPriceData = ref(null)

async function getTeamYield() {
	const currentUserID = useSupabaseUser().value.id
	const team_id = await getTeamId(currentUserID)
	return await $fetch('/api/getTeamYield', {
		params: { team_id: team_id.team_id },
	})
}

const getCropData = (cropType) => {
	return teamYield.value.find((crop) => crop.crop_type === cropType)
}

const noFieldsMessages = ref({
	wheat: null,
	maize: null,
	soybeans: null,
	sunflower: null,
	oats: null,
	sorghum: null,
	barley: null,
	canola: null,
	groundnuts: null,
})

onMounted(async () => {
	loading.value = true
	// Fetch team yield data
	teamYield.value = await getTeamYield()
	wheatPriceData.value = await getWheatMarketData()
	maizePriceData.value = await getMaizeMarketData()
	soyPriceData.value = await getSoyMarketData()
	sunflowerPriceData.value = await getSunflowerMarketData()
	oatsPriceData.value = await getCropMarketData('oats')
	sorghumPriceData.value = await getCropMarketData('sorghum')
	barleyPriceData.value = await getCropMarketData('barley')
	canolaPriceData.value = await getCropMarketData('canola')
	groundnutsPriceData.value = await getCropMarketData('groundnuts')

	// Assume teamYield.value is an array with wheat data at index 1
	// and maize data at index 0 (adjust as necessary)
	const wheatData = getCropData('wheat')
	const maizeData = getCropData('maize')
	const soyData = getCropData('soybeans')
	const sunflowerData = getCropData('sunflowerseed')
	const oatsData = getCropData('oats')
	const sorghumData = getCropData('sorghum')
	const barleyData = getCropData('barley')
	const groundnutsData = getCropData('groundnuts')
	const canolaData = getCropData('canola')

	if (wheatData) {
		teamWheatHectare.value = Number(wheatData.total_hectare.toFixed(2))
		teamWheatYield.value = wheatData.pred_tph === null ? 0 : Number(wheatData.pred_tph.toFixed(2))
		teamWheatProduction.value = wheatData.pred_production === null ? 0 : Number(wheatData.pred_production.toFixed(2))
		noFieldsMessages.value.wheat = ''
	} else {
		noFieldsMessages.value.wheat = 'You have no registered Wheat fields.'
	}

	if (maizeData) {
		teamMaizeHectare.value = Number(maizeData.total_hectare.toFixed(2))
		teamMaizeYield.value = maizeData.pred_tph === null ? 0 : Number(maizeData.pred_tph.toFixed(2))
		teamMaizeProduction.value = maizeData.pred_production === null ? 0 : Number(maizeData.pred_production.toFixed(2))
		noFieldsMessages.value.maize = ''
	} else {
		noFieldsMessages.value.maize = 'You have no registered Maize fields.'
	}

	if (soyData) {
		teamSoyHectare.value = Number(soyData.total_hectare.toFixed(2))
		teamSoyYield.value = soyData.pred_tph === null ? 0 : Number(soyData.pred_tph.toFixed(2))
		teamSoyProduction.value = soyData.pred_production === null ? 0 : Number(soyData.pred_production.toFixed(2))
		noFieldsMessages.value.soybeans = ''
	} else {
		noFieldsMessages.value.soybeans = 'You have no registered Soybean fields.'
	}

	if (sunflowerData) {
		teamSunflowerHectare.value = Number(sunflowerData.total_hectare.toFixed(2))
		teamSunflowerYield.value = sunflowerData.pred_tph === null ? 0 : Number(sunflowerData.pred_tph.toFixed(2))
		teamSunflowerProduction.value =
			sunflowerData.pred_production === null ? 0 : Number(sunflowerData.pred_production.toFixed(2))
		noFieldsMessages.value.sunflower = ''
	} else {
		noFieldsMessages.value.sunflower = ''
	}

	if (oatsData) {
		teamOatsHectare.value = Number(oatsData.total_hectare.toFixed(2))
		teamOatsYield.value = oatsData.pred_tph === null ? 0 : Number(oatsData.pred_tph.toFixed(2))
		teamOatsProduction.value = oatsData.pred_production === null ? 0 : Number(oatsData.pred_production.toFixed(2))
		noFieldsMessages.value.oats = ''
	} else {
		noFieldsMessages.value.oats = 'You have no registered Oats fields.'
	}

	if (sorghumData) {
		teamSorghumHectare.value = Number(sorghumData.total_hectare.toFixed(2))
		teamSorghumYield.value = sorghumData.pred_tph === null ? 0 : Number(sorghumData.pred_tph.toFixed(2))
		teamSorghumProduction.value = sorghumData.pred_production === null ? 0 : Number(sorghumData.pred_production.toFixed(2))
		noFieldsMessages.value.sorghum = ''
	} else {
		noFieldsMessages.value.sorghum = 'You have no registered Sorghum fields.'
	}

	if (barleyData) {
		teamBarleyHectare.value = Number(barleyData.total_hectare.toFixed(2))
		teamBarleyYield.value = barleyData.pred_tph === null ? 0 : Number(barleyData.pred_tph.toFixed(2))
		teamBarleyProduction.value = barleyData.pred_production === null ? 0 : Number(barleyData.pred_production.toFixed(2))
		noFieldsMessages.value.barley = ''
	} else {
		noFieldsMessages.value.barley = 'You have no registered Barley fields.'
	}

	if (groundnutsData) {
		teamGroundnutsHectare.value = Number(groundnutsData.total_hectare.toFixed(2))
		teamGroundnutsYield.value = groundnutsData.pred_tph === null ? 0 : Number(groundnutsData.pred_tph.toFixed(2))
		teamGroundnutsProduction.value =
			groundnutsData.pred_production === null ? 0 : Number(groundnutsData.pred_production.toFixed(2))
		noFieldsMessages.value.groundnuts = ''
	} else {
		noFieldsMessages.value.groundnuts = 'You have no registered Groundnuts fields.'
	}

	if (canolaData) {
		teamCanolaHectare.value = Number(canolaData.total_hectare.toFixed(2))
		teamCanolaYield.value = canolaData.pred_tph === null ? 0 : Number(canolaData.pred_tph.toFixed(2))
		teamCanolaProduction.value = canolaData.pred_production === null ? 0 : Number(canolaData.pred_production.toFixed(2))
		noFieldsMessages.value.canola = ''
	} else {
		noFieldsMessages.value.canola = 'You have no registered Canola fields.'
	}

	// Fetch past average TPH values
	wheatPastAverage.value = await getCropPastAverage('wheat')
	maizePastAverage.value = await getCropPastAverage('maize')
	soyPastAverage.value = await getCropPastAverage('soybeans')
	sunflowerPastAverage.value = await getCropPastAverage('sunflowerseed')
	oatsPastAverage.value = await getCropPastAverage('oats')
	sorghumPastAverage.value = await getCropPastAverage('sorghum')
	barleyPastAverage.value = await getCropPastAverage('barley')
	groundnutsPastAverage.value = await getCropPastAverage('groundnuts')
	canolaPastAverage.value = await getCropPastAverage('canola')

	// Set initial chart options
	chartOptions.value = setChartOptions()

	// Generate chart data based on the selected crop
	generateChartData()
	loading.value = false
})

// Watch for changes in the selected crop and regenerate the chart data
watch(selectedCrop, () => {
	generateChartData()
})

function generateChartData() {
	const labels = []
	const predictedRevenueData = []
	const realRevenueData = []
	let priceData = []
	let predictedProduction = 0
	let realProduction = 0

	if (selectedCrop.value.label === 'Wheat') {
		priceData = wheatPriceData.value
		predictedProduction = teamWheatProduction.value
		realProduction = teamWheatHectare.value * wheatPastAverage.value
	} else if (selectedCrop.value.label === 'Maize') {
		priceData = maizePriceData.value
		predictedProduction = teamMaizeProduction.value
		realProduction = teamMaizeHectare.value * maizePastAverage.value
	} else if (selectedCrop.value.label === 'Soybeans') {
		priceData = soyPriceData.value
		predictedProduction = teamSoyProduction.value
		realProduction = teamSoyHectare.value * soyPastAverage.value
	} else if (selectedCrop.value.label === 'Sunflower') {
		priceData = sunflowerPriceData.value
		predictedProduction = teamSunflowerProduction.value
		realProduction = teamSunflowerHectare.value * sunflowerPastAverage.value
	} else if (selectedCrop.value.label === 'Sorghum') {
		priceData = sorghumPriceData.value
		predictedProduction = teamSorghumProduction.value
		realProduction = teamSorghumHectare.value * sorghumPastAverage.value
	} else if (selectedCrop.value.label === 'Barley') {
		priceData = barleyPriceData.value
		predictedProduction = teamBarleyProduction.value
		realProduction = teamBarleyHectare.value * barleyPastAverage.value
	} else if (selectedCrop.value.label === 'Canola') {
		priceData = canolaPriceData.value
		predictedProduction = teamCanolaProduction.value
		realProduction = teamCanolaHectare.value * canolaPastAverage.value
	} else if (selectedCrop.value.label === 'Oats') {
		priceData = oatsPriceData.value
		predictedProduction = teamOatsProduction.value
		realProduction = teamOatsHectare.value * oatsPastAverage.value
	} else if (selectedCrop.value.label === 'Groundnuts') {
		priceData = groundnutsPriceData.value
		predictedProduction = teamGroundnutsProduction.value
		realProduction = teamGroundnutsHectare.value * groundnutsPastAverage.value
	}

	const last12PriceData = priceData.slice(-12)

	last12PriceData.forEach((item) => {
		labels.push(item.date)

		const price = parseFloat(item.market_value)

		// Calculate predicted revenue
		const predictedRevenue = price * predictedProduction
		predictedRevenueData.push(predictedRevenue.toFixed(2))

		// Calculate real revenue
		const realRevenue = price * realProduction
		realRevenueData.push(realRevenue.toFixed(2))
	})

	// Update the chartData object
	chartData.value = {
		labels: labels,
		datasets: [
			{
				label: 'Predicted Revenue',
				data: predictedRevenueData,
				backgroundColor: 'rgba(40, 137, 75, 1)',
			},
			{
				label: 'Past Average Predicted Revenue',
				type: 'line',
				data: realRevenueData,
				backgroundColor: 'rgba(100, 117, 138, 1)',
				borderColor: 'rgba(100, 117, 138, 1)',
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
					color: 'rgba(192, 192, 192, 0.5)',
					display: true,
				},
				title: {
					display: true,
					text: 'Term',
					font: {
						size: 12,
						weight: 'bold',
					},
				},
				stacked: false,
			},
			y: {
				beginAtZero: true,
				grid: {
					color: 'rgba(192, 192, 192, 0.5)',
					display: true,
				},
				title: {
					display: true,
					text: 'Revenue in ZAR',
					font: {
						size: 12,
						weight: 'bold',
					},
				},
				stacked: false,
			},
		},
	}
}
</script>
