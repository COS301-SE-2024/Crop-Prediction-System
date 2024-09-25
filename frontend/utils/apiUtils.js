export async function getTeamId(userId) {
	return await $fetch('/api/getTeamID', {
		params: { userid: userId },
	})
}

export async function getTeamFields(teamId) {
	const response = await $fetch('/api/getTeamFields', {
		params: { team_id: teamId },
	})

	if (Array.isArray(response)) {
		return response
	} else {
		console.error('Error fetching user fields:', response.error || response)
		return []
	}
}

export async function getFieldData(fieldId) {
	return await $fetch('/api/getFieldData', {
		params: { fieldid: fieldId },
	})
}

export function transformData(data) {
	const result = {}

	data.forEach((item) => {
		Object.keys(item).forEach((key) => {
			if (key === 'field_id') {
				if (!result[key]) {
					result[key] = item[key]
				}
			} else {
				if (!result[key]) {
					result[key] = []
				}

				if (key === 'date') {
					const formattedDate = item[key].slice(5)
					result[key].push(formattedDate)
				} else {
					result[key].push(item[key])
				}
			}
		})
	})

	Object.keys(result).forEach((key) => {
		if (Array.isArray(result[key]) && result[key].length > 30) {
			result[key] = result[key].slice(-30)
		}
	})

	return result
}

export async function getPastYieldAvg(crop) {
	return await $fetch('/api/getPastYieldAvg', {
		params: { crop: crop },
	})
}
