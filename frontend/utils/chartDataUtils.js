export function updateChartData(field, filterValue, chartDataList) {
	if (field && field.data) {
		const slicedData = sliceData(field.data, filterValue)
		const formattedToday = formatToday()

		Object.keys(chartDataList).forEach((key) => {
			if (chartDataList[key]) {
				chartDataList[key].chartData = createChartData(slicedData, key, formattedToday)
			} else {
				console.warn(`Chart data for key "${key}" is not defined in chartDataList`)
			}
		})
	}
}

function sliceData(data, filterValue) {
	const slicedData = {}
	const dataLength = data.date ? data.date.length : 0
	const entriesToUse = Math.min(dataLength, filterValue)

	Object.keys(data).forEach((key) => {
		if (Array.isArray(data[key])) {
			slicedData[key] = data[key].slice(-entriesToUse)
		} else {
			slicedData[key] = data[key]
		}
	})

	return slicedData
}

function formatToday() {
	const today = new Date()
	return `${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`
}

function createChartData(slicedData, key, formattedToday) {
	const chartConfigs = {
		soilMoisture: { label: 'Soil Moisture', dataKey: 'soil_moisture', color: 'rgba(6, 182, 212, 1)' },
		soilTemperature: { label: 'Soil Temperature', dataKey: 'soil_temperature', color: 'rgba(248, 114, 22, 1)' },
		temperature: {
			datasets: [
				{ label: 'Temp Max', dataKey: 'tempmax', color: 'rgba(76, 175, 80, 1)' },
				{ label: 'Temp Mean', dataKey: 'tempmean', color: 'rgba(255, 205, 86, 1)' },
				{ label: 'Temp Min', dataKey: 'tempmin', color: 'rgba(255, 99, 132, 1)' },
			],
		},
		dewPoint: { label: 'Dew Point', dataKey: 'dew_point', color: 'rgba(115, 155, 208, 1)' },
		humidity: { label: 'Humidity', dataKey: 'humidity', color: 'rgba(168, 84, 246, 1)' },
		pressure: { label: 'Pressure', dataKey: 'pressure', color: 'rgba(255, 99, 132, 1)' },
		uv: { label: 'UV Index', dataKey: 'uvi', color: 'rgba(255, 205, 86, 1)' },
		sprayability: { label: 'Sprayability', dataKey: 'pred_sprayability', color: 'rgba(255, 205, 86, 1)' },
		precipitation: { label: 'Precipitation', dataKey: 'rain', color: 'rgba(6, 182, 212, 1)' },
	}

	const config = chartConfigs[key]

	if (!config) {
		console.error(`No chart configuration found for key: ${key}`)
		return { labels: [], datasets: [] }
	}

	if (config.datasets) {
		return {
			labels: slicedData.date || [],
			datasets: config.datasets.map((dataset) => createDataset(dataset, slicedData, formattedToday)),
		}
	} else {
		return {
			labels: slicedData.date || [],
			datasets: [createDataset(config, slicedData, formattedToday)],
		}
	}
}

function createDataset(config, slicedData, formattedToday) {
	return {
		label: config.label,
		data: slicedData[config.dataKey] || [],
		fill: false,
		borderWidth: 3,
		backgroundColor: config.color.replace('1)', '0.2)'),
		borderColor: config.color,
		tension: 0.4,
		pointRadius: (slicedData.date || []).map(() => 3),
		borderDash: (slicedData.date || []).map((date) => (date > formattedToday ? [6, 6] : [])),
		segment: {
			borderDash: (ctx) => {
				const index = ctx.p0DataIndex
				const currentDate = (slicedData.date || [])[index]
				return currentDate >= formattedToday ? [6, 6] : undefined
			},
		},
	}
}

export function getGridClass(filterValue) {
	switch (filterValue) {
		case 8:
			return 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3'
		case 14:
			return 'grid-cols-1 md:grid-cols-2'
		default:
			return 'grid-cols-1'
	}
}
