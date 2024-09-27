import { ref } from 'vue'
import { getTeamId } from '~/utils/apiUtils'
import { getWheatMarketData, getTeamYield, getMaizeMarketData } from '~/utils/marketUtils'

export function useMarketData() {
	const currentUser = useSupabaseUser()
	const teamYield = ref()
	const wheatMarketData = ref()
	const maizeMarketData = ref()
	const loading = ref(false)

	async function fetchMarketData() {
		loading.value = true
		const teamID = await getTeamId(currentUser.value.id)
		const teamYieldData = await getTeamYield(teamID.team_id)
		// const wheatData = await getWheatMarketData()
		// const maizeData = await getMaizeMarketData()

		teamYield.value = teamYieldData
		// wheatMarketData.value = wheatData
		// maizeMarketData.value = maizeData

		loading.value = false
	}

	fetchMarketData()

	return {
		teamYield,
		// TODO: Make this exportable
		// wheatMarketData,
		// maizeMarketData,
		// loading,
	}
}
