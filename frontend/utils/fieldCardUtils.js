export function capitalizeFirstCharacter(str) {
	return str ? str.charAt(0).toUpperCase() + str.slice(1) : 'Select a Field'
}

export function getCurrentDateFormatted() {
	const date = new Date()
	return `${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

export function getChartData(fieldData, dataKey, status) {
	return {
		labels: fieldData.date,
		datasets: [
			{
				label: dataKey === 'pred_yield' ? 'Yield' : 'Health',
				data: fieldData[dataKey],
				fill: true,
				backgroundColor: getColor(status.score, 0.2),
				borderColor: getColor(status.score, 1),
				borderWidth: 2,
				tension: 0.4,
				pointRadius: 0,
			},
		],
	}
}

export function getChartOptions() {
	return {
		responsive: true,
		maintainAspectRatio: false,
		plugins: {
			legend: { display: false },
			tooltip: { enabled: false },
		},
		scales: {
			x: { display: false },
			y: { display: false },
		},
		interaction: { mode: 'none' },
		hover: { mode: null },
	}
}

export function getSprayabilityFactor(field) {
	if (!field || !field.data) return 0
	const currentDate = getCurrentDateFormatted()
	const index = field.data.date.indexOf(currentDate)
	if (index === -1) return 0
	return Math.round(field.data.pred_sprayability[index] * 100) / 100 || 0
}

export function getPrecipitation(field) {
	if (!field || !field.data) return 0
	const currentDate = getCurrentDateFormatted()
	const index = field.data.date.indexOf(currentDate)
	if (index === -1) return 0
	return Math.round(field.data.rain[index] * 100) / 100 || 0
}

export function getHealthStatus(field) {
	if (!field || !field.data) return { value: 'Select Field', severity: 'contrast', score: 0 }
	const currentDate = getCurrentDateFormatted()
	const index = field.data.date.indexOf(currentDate)
	if (index === -1) return { value: 'Unknown', severity: 'secondary', score: 0 }
	const currentHealth = Math.round(field.data.pred_health[index])
	if (currentHealth >= 70) return { value: 'Healthy', severity: 'primary', score: currentHealth }
	if (currentHealth >= 40) return { value: 'Moderate', severity: 'warning', score: currentHealth }
	return { value: 'Severe', severity: 'danger', score: currentHealth }
}

export function getYieldStatus(field) {
	if (!field || !field.data) return { value: 'Select Field', severity: 'contrast', score: 0 }
	const currentDate = getCurrentDateFormatted()
	const index = field.data.date.indexOf(currentDate)
	if (index === -1) return { value: 'Unknown', severity: 'secondary', score: 0 }
	const currentYield = Math.round(field.data.pred_yield[index] * 100) / 100
	const percentageDifference = calculatePercentageDifference(currentYield, field.pastYieldAvg)
	if (percentageDifference >= 0)
		return { value: 'Healthy', severity: 'primary', score: currentYield, percentageDifference: `${percentageDifference}%` }
	if (percentageDifference >= -9.99)
		return { value: 'Moderate', severity: 'warning', score: currentYield, percentageDifference: `${percentageDifference}%` }
	return { value: 'Severe', severity: 'danger', score: currentYield, percentageDifference: `${percentageDifference}%` }
}

export function getCurrentSummary(field) {
	if (!field || !field.data) return 'Please select a field to view the AI summary.'
	const currentDate = getCurrentDateFormatted()
	const index = field.data.date.indexOf(currentDate)
	if (index === -1) return 'No summary available for the current date.'
	return field.data.summary[index] || 'Summary not available.'
}

function getColor(value, opacity) {
	if (value >= 70) return `rgba(17, 185, 29, ${opacity})`
	if (value >= 40) return `rgba(248, 114, 22, ${opacity})`
	return `rgba(255, 99, 132, ${opacity})`
}

function calculatePercentageDifference(currentValue, pastValue) {
	if (pastValue === 0) return currentValue > 0 ? 100 : currentValue < 0 ? -100 : 0
	const difference = currentValue - pastValue
	return Math.round((difference / Math.abs(pastValue)) * 10000) / 100
}
