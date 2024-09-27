export async function getTeamYield(team_id) {
	return await $fetch('/api/getTeamYield', {
		params: { team_id: team_id },
	})
}

export async function getCropMarketData(crop) {
	return await $fetch('/api/getMarketData', {
		params: { crop: crop },
	})
}

export async function getCropPastAverage(crop) {
	return await $fetch('/api/getPastYieldAvg', {
		params: { crop: crop },
	})
}
