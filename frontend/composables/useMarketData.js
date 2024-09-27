import { ref } from 'vue'
import { getCropMarketData } from '~/utils/marketUtils'

export function useMarketData() {
	const loading = ref(true)
	const selectedCrop = ref({ label: 'Wheat', value: 'Wheat' })
	const chartData = ref(null)
	const chartOptions = ref(null)
	const marketData = ref({})

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

	async function fetchMarketData() {
		marketData.value = {
			wheat: await getCropMarketData('wheat'),
			maize: await getCropMarketData('maize'),
			soybeans: await getCropMarketData('soybeans'),
			sunflowerseed: await getCropMarketData('sunflowerseed'),
			oats: await getCropMarketData('oats'),
			sorghum: await getCropMarketData('sorghum'),
			barley: await getCropMarketData('barley'),
			canola: await getCropMarketData('canola'),
			groundnuts: await getCropMarketData('groundnuts'),
		}
		loading.value = false
	}

	function generateChartData(cropData) {
		const priceData = marketData.value[selectedCrop.value.value.toLowerCase()].slice(-12)
		const labels = priceData.map((item) => item.date)
		const predictedRevenueData = priceData.map((item) => (parseFloat(item.market_value) * cropData.production).toFixed(2))
		const realRevenueData = priceData.map((item) => (parseFloat(item.market_value) * cropData.realProduction).toFixed(2))

		chartData.value = {
			labels,
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

		chartOptions.value = {
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

	return {
		loading,
		cropOptions,
		selectedCrop,
		chartData,
		chartOptions,
		fetchMarketData,
		generateChartData,
	}
}
