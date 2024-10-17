import { ref, reactive } from 'vue'
import { getTeamId, getTeamFields, getFieldData, transformData, getPastYieldAvg } from '~/utils/apiUtils'

export function useFieldData() {
	const currentUser = useSupabaseUser()
	const userFieldsWithData = ref([])
	const filterOptions = ref([])
	const loading = ref(false)

	// soilMoisture: 'The amount of water in the soil as a percentage',
	// soilTemperature: 'The temperature of the soil in degrees Celsius',
	// temperature: 'The temperature in degrees Celsius',
	// dewPoint: 'The temperature at which air becomes saturated with water vapor',
	// humidity: 'The amount of water vapor in the air as a percentage',
	// pressure: 'The force exerted by the atmosphere on a surface',
	// uv: 'The strength of ultraviolet radiation from the sun',
	// sprayability: 'The suitability to spray chemicals on crops',
	// precipitation: 'The amount of rain that has fallen in millimeters',

	const chartDataList = reactive({
		soilMoisture: {
			title: 'Soil Moisture',
			chartData: {},
			subtitle: 'The amount of water in the soil as a percentage',
			unit: '%',
		},
		soilTemperature: {
			title: 'Soil Temperature (°C)',
			chartData: {},
			subtitle: 'The temperature of the soil in degrees Celsius',
			unit: '°C',
		},
		sprayability: {
			title: 'Sprayability',
			chartData: {},
			subtitle: 'The suitability to spray chemicals on crops',
			unit: '%',
		},
		precipitation: {
			title: 'Precipitation (mm)',
			chartData: {},
			subtitle: 'The amount of rain that has fallen in millimeters',
			unit: 'mm',
		},
		temperature: { title: 'Temperature (°C)', chartData: {}, subtitle: 'The temperature in degrees Celsius', unit: '°C' },
		dewPoint: {
			title: 'Dew Point (°C)',
			chartData: {},
			subtitle: 'The temperature at which air becomes saturated with water vapor',
			unit: '°C',
		},
		humidity: {
			title: 'Humidity',
			chartData: {},
			subtitle: 'The amount of water vapor in the air as a percentage',
			unit: '%',
		},
		pressure: { title: 'Pressure', chartData: {}, subtitle: 'The force exerted by the atmosphere on a surface', unit: 'hPa' },
		uv: { title: 'UV Index', chartData: {}, subtitle: 'The strength of ultraviolet radiation from the sun', unit: '' },
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
