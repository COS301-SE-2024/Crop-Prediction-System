export async function getTeamYield(team_id) {
	return await $fetch('/api/getTeamYield', {
		params: { team_id: team_id },
	})
}

export async function getWheatMarketData() {
	return await $fetch('/api/getMarketData', {
		params: { crop: 'wheat' },
	})
}

export async function getMaizeMarketData() {
	return await $fetch('/api/getMarketData', {
		params: { crop: 'maize' },
	})
}

export async function getSoyMarketData() {
	return await $fetch('/api/getMarketData', {
		params: { crop: 'soybeans' },
	})
}

export async function getSunflowerMarketData() {
	return await $fetch('/api/getMarketData', {
		params: { crop: 'sunflowerseed' },
	})
}

export async function getWheatPastAverage() {
	return await $fetch('/api/getPastYieldAvg', {
		params: { crop: 'wheat' },
	})
}

export async function getMaizePastAverage() {
	return await $fetch('/api/getPastYieldAvg', {
		params: { crop: 'maize' },
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
