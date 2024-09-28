export function useDummyChartData() {
	const dummyChartData = {
		title: 'Soil Moisture',
		chartData: {
			labels: ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7', 'Day 8'],
			datasets: [
				{
					label: 'Soil Moisture',
					data: [20, 25, 22, 30, 28, 35, 32, 40],
					fill: false,
					borderWidth: 3,
					backgroundColor: 'rgba(6, 182, 212, 0.2)',
					borderColor: 'rgba(6, 182, 212, 1)',
					tension: 0.4,
					pointRadius: 3,
				},
			],
		},
	}

	return {
		dummyChartData,
	}
}
