<template>
	<div class="border border-surface-border dark:border-surface-600 p-2 xl:p-6 rounded-lg shadow-lg text-sm">
		<DataTable :value="fields" paginator :rows="5" :rowsPerPageOptions="[5, 10, 20, 50]">
			<Column field="name" header="Name" style="width: 25%">
				<template #body="slotProps">
					<!-- 0.0 to 0.3, 0.3 to 0.6, 0.6 to 1.0 -->
					<Tag
						:severity="slotProps.data.health < 0.3 ? 'danger' : slotProps.data.health < 0.6 ? 'warning' : 'success'"
						rounded
					>
						<span class="text-red-200 mr-2" v-if="slotProps.data.health < 0.3">S</span>
						<span class="text-yellow-500 mr-2" v-else-if="slotProps.data.health < 0.6">M</span>
						<span class="text-green-900 mr-2" v-else>H</span>
						{{ slotProps.data.name }}
					</Tag>
				</template>
			</Column>
			<Column field="yield" header="T/H" style="width: 25%"></Column>
			<Column field="cropType" header="Crop Type" style="width: 25%"></Column>
		</DataTable>
	</div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const fields = ref([
	{ name: 'Field 1', health: 0.34, yield: 12, cropType: 'Wheat' },
	{ name: 'Field 2', health: 0.56, yield: 15, cropType: 'Rice' },
	{ name: 'Field 3', health: 0.78, yield: 18, cropType: 'Corn' },
	{ name: 'Field 4', health: 0.45, yield: 14, cropType: 'Soybean' },
	{ name: 'Field 5', health: 0.67, yield: 17, cropType: 'Barley' },
	{ name: 'Field 6', health: 0.89, yield: 20, cropType: 'Oats' },
	{ name: 'Field 7', health: 0.23, yield: 10, cropType: 'Rye' },
	{ name: 'Field 8', health: 0.45, yield: 14, cropType: 'Wheat' },
])
</script>
