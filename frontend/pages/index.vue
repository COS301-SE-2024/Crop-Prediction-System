<template>
	<div class="flex w-full justify-center items-start p-4">
		<div class="flex flex-col justify-start items-start gap-4 w-full">
			<div class="flex flex-col md:flex-row w-full gap-5">
				<div class="w-full md:w-1/3">
					<FieldCard v-model="selectedField" :fields="fields" />
				</div>
				<div class="w-full md:w-2/3 h-96 md:h-auto rounded overflow-hidden border-surface-600 shadow-md">
					<GoogleMapsField :selectedField="selectedField" :fields="fields" />
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref } from 'vue'
import FieldCard from '~/components/FieldCard.vue'
import GoogleMapsField from '~/components/GoogleMapsField.vue'

const selectedField = ref(null)

// Define the fields here
const fields = ref([
	{
		id: 10,
		created_at: '2024-06-23T19:11:49.43101+00:00',
		field_area: [
			[-25.8707939665029, 28.1601760921001],
			[-25.8714238619316, 28.160146587801],
			[-25.8713321532275, 28.1593794760227],
			[-25.8708446478686, 28.1595377263546],
		],
		field_name: 'Maize Down',
		field_tph: 0.7,
		field_health: 0.7,
		crop_type: 'Maize',
		team_id: '17383e3d-f211-4724-8515-8c4cb836c812',
		updated_at: '2024-06-23T19:11:49.43101+00:00',
		hectare: 0.644354929407972,
	},
	{
		id: 8,
		created_at: '2024-06-23T13:52:42.724541+00:00',
		field_area: [
			[-25.8703366265299, 28.1593566772461],
			[-25.8703317997134, 28.160236441803],
			[-25.8706431289766, 28.1602659461021],
			[-25.8707975866012, 28.1594344613075],
		],
		field_name: 'First Field',
		field_tph: 0.8,
		field_health: 0.85,
		crop_type: 'Wheat',
		team_id: '17383e3d-f211-4724-8515-8c4cb836c812',
		updated_at: '2024-06-23T13:52:42.724541+00:00',
		hectare: 0.546557915300319,
	},
	{
		id: 28,
		created_at: '2024-06-24T09:36:02.484727+00:00',
		field_area: [
			[-25.755436539304, 28.2323061052948],
			[-25.7558472161549, 28.232161266008],
			[-25.7559535087556, 28.2324724022537],
			[-25.7554993487967, 28.2326038304954],
		],
		field_name: 'Up 1',
		field_tph: 1.2,
		field_health: 0.95,
		crop_type: 'Barley',
		team_id: '17383e3d-f211-4724-8515-8c4cb836c812',
		updated_at: '2024-06-24T09:36:02.484727+00:00',
		hectare: 0.233207014962497,
	},
	{
		id: 13,
		created_at: '2024-06-24T05:58:25.142173+00:00',
		field_area: [
			[-25.8495617478938, 28.1452494848141],
			[-25.8494893328991, 28.145600854195],
			[-25.8497234745553, 28.1456813204655],
			[-25.849793475579, 28.1453272688755],
		],
		field_name: 'Field 4',
		field_tph: 2.5,
		field_health: 0.82,
		crop_type: 'Oats',
		team_id: '17383e3d-f211-4724-8515-8c4cb836c812',
		updated_at: '2024-06-24T05:58:25.142173+00:00',
		hectare: 0.143355503464841,
	},
])

definePageMeta({
	middleware: 'auth',
})
</script>
