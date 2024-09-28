<template>
	<Card v-if="activeIndex === 1" class="mt-6 p-5">
		<template #content>
			<div class="w-full flex flex-col justify-between items-start gap-4">
				<h1 class="text-2xl font-semibold">Revenue Dashboard Help</h1>
				<p>
					Welcome to the Revenue Dashboard! This dashboard allows you to view and analyze market data for various crops.
					Here's how to use it:
				</p>

				<h2 class="text-xl font-semibold">1. Selecting a Crop</h2>
				<p>
					Use the dropdown at the top of the dashboard to select the crop you're interested in. The dashboard will
					update automatically to display data related to the selected crop.
				</p>
				<Dropdown
					v-model="selectedCrop"
					:options="cropOptions"
					optionLabel="label"
					placeholder="Select a Crop"
					class="mb-4 w-full md:w-64"
				/>

				<h2 class="text-xl font-semibold">2. Viewing Hectare and Yield Data</h2>
				<p>After selecting a crop, two cards will display key information:</p>
				<ul class="list-disc ml-6">
					<li>
						<strong>{{ selectedCrop.label }} Hectare:</strong> Shows the total hectare of your team's fields for the
						selected crop.
					</li>
					<li>
						<strong>{{ selectedCrop.label }} t/ha:</strong> Displays the combined tons per hectare (t/ha) yield for
						your team's fields of the selected crop.
					</li>
				</ul>
				<div class="grid gap-4 grid-cols-1 sm:grid-cols-2">
					<MarketHectareCard
						:title="`${selectedCrop.label} Hectare`"
						:hectare="hectare"
						class="border-2 border-surface-500"
						:footer="`Total hectare of team ${selectedCrop.label.toLowerCase()} fields`"
					/>
					<MarketDataCard
						:title="`${selectedCrop.label} t/ha`"
						:tph="tph"
						class="border-2 border-surface-500"
						:footer="`Combined t/ha of team ${selectedCrop.label.toLowerCase()} fields`"
					/>
				</div>

				<h2 class="text-xl font-semibold">3. Revenue Chart</h2>
				<p>
					If data is available, a chart will display the predicted revenue and past average predicted revenue for the
					selected crop over the last 12 terms. This helps you compare current predictions with historical data.
				</p>
				<Chart type="bar" :data="chartData" :options="chartOptions" class="w-full h-[300px]" />

				<h2 class="text-xl font-semibold">4. Interacting with the Chart</h2>
				<p>
					You can interact with the chart by toggling datasets in the legend or hovering over data points for more
					details. Click on the dataset labels in the legend to show or hide specific data.
				</p>

				<h2 class="text-xl font-semibold">5. No Fields Message</h2>
				<p>If you have no registered fields for the selected crop, a message will inform you:</p>
				<blockquote class="mb-4 text-surface-900 dark:text-surface-0 font-bold text-lg">
					"You have no registered {{ selectedCrop.label }} fields."
				</blockquote>

				<h2 class="text-xl font-semibold">6. Loading Indicator</h2>
				<p>
					While the market data is being fetched, a loading spinner and message will appear. Please wait until the data
					is fully loaded.
				</p>
				<div class="w-full h-full mt-4 gap-5 flex flex-col items-center justify-center">
					<ProgressSpinner />
					<h2 class="dark:text-white font-bold">Fetching Market Data...</h2>
				</div>
			</div>
		</template>
	</Card>
</template>

<script setup>
import { defineProps, ref, onMounted } from 'vue'
import Card from 'primevue/card'
import Dropdown from 'primevue/dropdown'
import Chart from 'primevue/chart'
import ProgressSpinner from 'primevue/progressspinner'
import MarketHectareCard from '~/components/MarketHectareCard.vue'
import MarketDataCard from '~/components/MarketDataCard.vue'

const props = defineProps({
	activeIndex: {
		type: Number,
		default: 0,
	},
})

const cropOptions = [
	{ label: 'Wheat', value: 'Wheat' },
	{ label: 'Maize', value: 'Maize' },
	{ label: 'Soybeans', value: 'Soybeans' },
	{ label: 'Sunflower', value: 'sunflowerseed' },
	{ label: 'Sorghum', value: 'Sorghum' },
	{ label: 'Barley', value: 'Barley' },
	{ label: 'Canola', value: 'Canola' },
	{ label: 'Oats', value: 'Oats' },
	{ label: 'Groundnuts', value: 'Groundnuts' },
]

const selectedCrop = ref(cropOptions[0])

const hectare = ref(100) // Sample data
const tph = ref(5.5) // Sample data

const chartData = ref(null)
const chartOptions = ref(null)

onMounted(() => {
	chartData.value = getSampleChartData()
	chartOptions.value = getSampleChartOptions()
})

function getSampleChartData() {
	const labels = [
		'Term 1',
		'Term 2',
		'Term 3',
		'Term 4',
		'Term 5',
		'Term 6',
		'Term 7',
		'Term 8',
		'Term 9',
		'Term 10',
		'Term 11',
		'Term 12',
	]
	const predictedRevenueData = [1000, 1200, 1100, 1300, 1250, 1400, 1350, 1500, 1450, 1600, 1550, 1700]
	const realRevenueData = [950, 1150, 1050, 1250, 1200, 1350, 1300, 1450, 1400, 1550, 1500, 1650]

	return {
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

function getSampleChartOptions() {
	return {
		maintainAspectRatio: false,
		responsive: true,
		plugins: { legend: { display: true } },
		scales: {
			x: {
				ticks: { autoSkip: false },
				grid: { color: 'rgba(192, 192, 192, 0.5)', display: true },
				title: { display: true, text: 'Term', font: { size: 12, weight: 'bold' } },
				stacked: false,
			},
			y: {
				beginAtZero: true,
				grid: { color: 'rgba(192, 192, 192, 0.5)', display: true },
				title: { display: true, text: 'Revenue in ZAR', font: { size: 12, weight: 'bold' } },
				stacked: false,
			},
		},
	}
}
</script>

<style scoped>
blockquote {
	border-left: 4px solid #ccc;
	padding-left: 1em;
	color: #555;
}
</style>
