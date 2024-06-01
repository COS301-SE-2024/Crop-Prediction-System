<template>
	<div class="flex flex-col gap-5 h-full">
		<div class="flex space-x-5 w-full">
			<StatPanel
				v-for="stat in stats"
				:key="stat.title"
				:title="stat.title"
				:chart-input="stat.chartData"
				:chart-type="stat.chartType"
				class="w-full"
			/>
		</div>
		<div class="grid grid-cols-5 grid-rows-2 w-full h-full gap-5 pb-5">
			<div class="col-span-3 row-span-2 border border-surface-border p-6 rounded-lg shadow-lg h-full flex flex-col gap-2">
				<div class="flex justify-between items-center">
					<p class="text-xl font-[500]">Farm Map</p>
					<NuxtLink to="/inputs/manage-fields" class="text-sm text-primary-500">
						<Button label="Edit" icon="pi pi-pencil" severity="secondary" text />
					</NuxtLink>
				</div>
				<GoogleMap class="w-full h-full" />
			</div>
			<div class="col-span-2 row-span-2 grid gap-5 h-full">
				<FieldData />
				<div class="grid grid-cols-2 gap-5 items-center border border-surface-border p-6 rounded-lg shadow-lg">
					<div class="flex flex-col gap-2">
						<span class="text-lg font-[500]">Polar Stats</span>
						<!-- actionable results -->
						<p class="text-sm text-surface-500">Actionable results based on the data</p>
						<p>
							We'd suggest increasing the moisture levels in the soil to improve the overall crop health. This will
							also help with the current temperature and humidity levels.
						</p>
						<div class="grid gap-3">
							<div v-for="(value, i) in polarSupportingStat" :key="value">
								<span class="text-sm font-[500]">{{ polarstat[0].labels[i] }}: {{ value * 100 }}%</span>
								<ProgressBar :value="value * 100" :showValue="false" style="height: 12px" />
							</div>
						</div>
					</div>
					<PolarStat
						v-for="stat in polarstat"
						:key="stat.title"
						:title="stat.title"
						:chart-input="stat.chartData"
						:chart-type="stat.chartType"
						class="w-full"
					/>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import StatPanel from '~/components/StatPanel.vue'
import GoogleMap from '~/components/GoogleMap.vue'
import Button from 'primevue/button'
import ProgressBar from 'primevue/progressbar'
import FieldData from '~/components/FieldData.vue'
import PolarStat from '~/components/PolarStat.vue'

const stats = [
	{
		title: 'Overall Crop Health',
		chartData: [65, 59, 80, 81, 56, 55, 40],
		chartType: 'line',
	},
	{
		title: 'Current Temperature',
		chartData: [24, 45, 67, 89, 34, 56, 78],
		chartType: 'line',
	},
	{
		title: 'Soil Moisture',
		chartData: [41, 56, 67, 24, 78, 45, 47],
		chartType: 'line',
	},
	{
		title: 'Rainfall',
		chartData: [51, 0, 67, 89, 45, 23, 78],
		chartType: 'bar',
	},
	{
		title: 'Humidity',
		chartData: [45, 67, 89, 34, 56, 78, 23],
		chartType: 'line',
	},
]

const polarstat = [
	{
		title: 'Polar Stat',
		chartData: [0.5, 0.7, 0.2, 0.7, 0.9],
		labels: ['Moisture', 'Temperature', 'Humidity', 'Soil', 'Rainfall'],
		chartType: 'polarArea',
	},
]

const polarSupportingStat: number[] = []
for (let i = 0; i < polarstat[0].chartData.length; i++) {
	polarSupportingStat.push(polarstat[0].chartData[i])
}
</script>
