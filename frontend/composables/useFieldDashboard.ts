import { ref, computed } from 'vue'
import {
	getChartData,
	getChartOptions,
	getSprayabilityFactor,
	getPrecipitation,
	getHealthStatus,
	getYieldStatus,
	getCurrentSummary,
} from '../utils/fieldCardUtils'
import type { Field, ChartData, ChartOptions, Status } from '../types'

export function useFieldDashboard(initialField: Field | null) {
	const selectedField = ref<Field | null>(initialField)
	const yieldData = ref<ChartData>({} as ChartData)
	const healthData = ref<ChartData>({} as ChartData)

	const chartOptions = computed<ChartOptions>(() => getChartOptions())

	const sprayabilityFactor = computed(() => getSprayabilityFactor(selectedField.value))
	const precipitation = computed(() => getPrecipitation(selectedField.value))

	const healthStatus = computed<Status>(() => getHealthStatus(selectedField.value))
	const yieldStatus = computed<Status>(() => getYieldStatus(selectedField.value))

	const currentSummary = computed(() => getCurrentSummary(selectedField.value))

	function updateChartData() {
		if (!selectedField.value?.data) return

		yieldData.value = getChartData(selectedField.value.data, 'pred_yield', yieldStatus.value)
		healthData.value = getChartData(selectedField.value.data, 'pred_health', healthStatus.value)
	}

	return {
		selectedField,
		yieldData,
		healthData,
		chartOptions,
		sprayabilityFactor,
		precipitation,
		healthStatus,
		yieldStatus,
		currentSummary,
		updateChartData,
	}
}
