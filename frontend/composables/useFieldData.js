import { ref, reactive } from 'vue'
import { getTeamId, getTeamFields, getFieldData, transformData, getPastYieldAvg } from '~/utils/apiUtils'

export function useFieldData() {
	const currentUser = useSupabaseUser()
	const userFieldsWithData = ref([])
	const filterOptions = ref([])
	const loading = ref(false)

	const chartDataList = reactive({
		soilMoisture: { title: 'Soil Moisture', chartData: {} },
		soilTemperature: { title: 'Soil Temperature (°C)', chartData: {} },
		sprayability: { title: 'Sprayability', chartData: {} },
		precipitation: { title: 'Precipitation (mm)', chartData: {} },
		temperature: { title: 'Temperature (°C)', chartData: {} },
		dewPoint: { title: 'Dew Point (°C)', chartData: {} },
		humidity: { title: 'Humidity', chartData: {} },
		pressure: { title: 'Pressure', chartData: {} },
		uv: { title: 'UV Index', chartData: {} },
	})

	async function fetchFieldData() {
		loading.value = true
		const teamId = await getTeamId(currentUser.value.id)
		const userFields = await getTeamFields(teamId.team_id)

		userFieldsWithData.value = await Promise.all(
			userFields.map(async (field) => {
				const fieldData = await getFieldData(field.id)
				const pastYieldAvg = await getPastYieldAvg(field.crop_type)
				const transformedFieldData = transformData(fieldData)
				return {
					...field,
					data: transformedFieldData,
					pastYieldAvg,
				}
			}),
		)
		loading.value = false
	}

	fetchFieldData()

	return {
		userFieldsWithData,
		filterOptions,
		chartDataList,
		loading,
	}
}
