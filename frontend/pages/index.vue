<template>
	<div class="space-y-5 w-full px-4 sm:px-6 md:px-8 lg:px-0 py-4 sm:py-6 md:py-8 lg:py-0">
		<div class="flex space-x-5 w-full overflow-x-auto whitespace-nowrap">
			<StatPanel
				v-for="stat in stats"
				:key="stat.title"
				:title="stat.title"
				:chart-input="stat.chartData"
				:chart-type="stat.chartType"
			/>
		</div>
		<div class="grid xl:grid-cols-5 xl:grid-rows-2 w-full h-full gap-5 pb-5">
			<div
				class="xl:col-span-3 xl:row-span-2 border border-surface-border dark:border-surface-600 md:p-6 rounded-lg shadow-lg md:h-full h-96 _h-full flex flex-col md:gap-2"
			>
				<div class="flex justify-between items-center p-2 pl-4">
					<p class="text-xl font-[500] dark:text-white">Farm Map</p>
					<NuxtLink to="/inputs/manage-fields" class="text-sm text-primary-500">
						<Button label="Edit" icon="pi pi-pencil" severity="secondary" text />
					</NuxtLink>
				</div>
				<GoogleMap class="w-full h-full" />
			</div>
			<div class="xl:col-span-2 xl:row-span-2 grid gap-5 h-full">
				<FieldData />
				<div
					class="grid xl:grid-cols-2 gap-5 items-center border border-surface-border dark:border-surface-600 p-6 rounded-lg shadow-lg"
				>
					<div class="flex flex-col gap-2">
						<span class="text-lg font-[500] dark:text-surface-0">Polar Stats</span>
						<!-- actionable results -->
						<p class="text-sm text-surface-500 dark:text-surface-100">Actionable results based on the data</p>
						<p class="dark:text-surface-400">
							We'd suggest increasing the moisture levels in the soil to improve the overall crop health. This will
							also help with the current temperature and humidity levels.
						</p>
						<div class="grid gap-3">
							<div v-for="(value, i) in polarSupportingStat" :key="value">
								<span class="text-sm font-[500] dark:text-surface-300"
									>{{ polarstat[0].labels[i] }}: {{ value * 100 }}%</span
								>
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
import { ref } from 'vue'

definePageMeta({
	middleware: 'auth',
})

const visible = ref(false)

function changeVisible() {
	visible.value = !visible.value
}

const recentEntries = await $fetch('/api/getRecentEntries')

let recentWeather = []
for (let i = 0; i < recentEntries.length; i++) {
	recentWeather.push(recentEntries[i]['mean_temperature'])
}

console.log('Recent Weather', recentWeather)

const userID = useSupabaseUser().value?.id

const userFields = await $fetch('/api/getUserFields', {
	params: { userid: userID },
})

let healts = []

for (let i = 0; i < userFields.length; i++) {
	const health = await $fetch('/api/getHealth', {
		params: { crop: userFields[i].crop_type },
	})
	healts.push(health['health_score'][1])
}

console.log('Health', healts)

let soilMoisture = []
for (let i = 0; i < recentEntries.length; i++) {
	soilMoisture.push(recentEntries[i]['soil_moisture'])
}

let precipitation = []
for (let i = 0; i < recentEntries.length; i++) {
	precipitation.push(recentEntries[i]['precipitation'])
}

const stats = [
	{
		title: 'Overall Crop Health',
		chartData: healts.length ? healts : [88, 80, 99, 92],
		chartType: 'line',
	},
	{
		title: 'Current Temperature',
		chartData: recentWeather.length ? recentWeather : [25, 27, 29, 30, 31],
		chartType: 'line',
	},
	{
		title: 'Soil Moisture',
		chartData: soilMoisture.length ? soilMoisture : [0.5, 0.7, 0.2, 0.7, 0.9],
		chartType: 'line',
	},
	{
		title: 'Rainfall',
		chartData: precipitation.length ? precipitation : [51, 0, 67, 89, 45, 23, 78],
		chartType: 'bar',
	},
	{
		title: 'Humidity',
		chartData: [45, 67, 89, 34, 56, 78, 23],
		chartType: 'line',
	},
]

let polarStatData = []
if (recentEntries.length > 0) {
	polarStatData = [
		recentEntries[0]['soil_moisture'],
		recentEntries[0]['mean_temperature'] / 100,
		0.7,
		recentEntries[0]['soil_seed_nitrogen_per_unit_area'],
		recentEntries[0]['precipitation'],
	]
} else {
	polarStatData = [0.5, 0.7, 0.2, 0.7, 0.9]
}

const polarstat = [
	{
		title: 'Polar Stat',
		chartData: polarStatData,
		labels: ['Moisture', 'Temperature', 'Humidity', 'Soil', 'Rainfall'],
		chartType: 'polarArea',
	},
]

const polarSupportingStat: number[] = []
for (let i = 0; i < polarstat[0].chartData.length; i++) {
	polarSupportingStat.push(polarstat[0].chartData[i])
}
</script>
