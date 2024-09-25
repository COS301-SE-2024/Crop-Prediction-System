export interface Field {
	id: number
	created_at: string
	field_area: [number, number][]
	field_name: string
	field_tph: number
	field_health: number
	crop_type: string
	team_id: string
	updated_at: string
	hectare: number
	data?: FieldData
	pastYieldAvg: number
}

export interface FieldData {
	date: string[]
	pred_health: number[]
	pred_yield: number[]
	pred_sprayability: number[]
	rain: number[]
	summary: string[]
}

export interface ChartData {
	labels: string[]
	datasets: {
		label: string
		data: number[]
		fill: boolean
		backgroundColor: string
		borderColor: string
		borderWidth: number
		tension: number
		pointRadius: number
	}[]
}

export interface ChartOptions {
	responsive: boolean
	maintainAspectRatio: boolean
	plugins: {
		legend: {
			display: boolean
		}
		tooltip: {
			enabled: boolean
		}
	}
	scales: {
		x: {
			display: boolean
		}
		y: {
			display: boolean
		}
	}
	interaction: {
		mode: string
	}
	hover: {
		mode: null
	}
}

export interface Status {
	value: string
	severity: string
	score: number
	percentageDifference?: string
}
