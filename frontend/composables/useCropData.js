import { ref, computed } from 'vue'
import { getTeamId } from '~/utils/apiUtils'
import { getCropPastAverage } from '~/utils/marketUtils'

export function useCropData(selectedCrop) {
	const teamYield = ref([])
	const pastAverages = ref({})
	const noFieldsMessage = computed(() => {
		const crop = selectedCrop.value.value.toLowerCase()
		return teamYield.value.find((c) => c.crop_type === crop)
			? ''
			: `You have no registered ${selectedCrop.value.label} fields.`
	})

	const cropData = computed(() => {
		const crop = selectedCrop.value.value.toLowerCase()
		const data = teamYield.value.find((c) => c.crop_type === crop) || {}
		const pastAverage = pastAverages.value[crop] || 0
		return {
			hectare: Number(data.total_hectare?.toFixed(2)) || 0,
			yield: Number(data.pred_tph?.toFixed(2)) || 0,
			production: Number(data.pred_production?.toFixed(2)) || 0,
			realProduction: (data.total_hectare || 0) * pastAverage,
		}
	})

	async function fetchCropData() {
		const currentUserID = useSupabaseUser().value.id
		const team_id = await getTeamId(currentUserID)
		teamYield.value = await $fetch('/api/getTeamYield', { params: { team_id: team_id.team_id } })

		const crops = ['wheat', 'maize', 'soybeans', 'sunflowerseed', 'oats', 'sorghum', 'barley', 'groundnuts', 'canola']
		for (const crop of crops) {
			pastAverages.value[crop] = await getCropPastAverage(crop)
		}
	}

	return {
		cropData,
		noFieldsMessage,
		fetchCropData,
	}
}
