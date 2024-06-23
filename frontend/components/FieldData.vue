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

const fields = ref([])

const userID = useSupabaseUser().value?.id

const userFields = await $fetch('/api/getUserFields', {
	params: { userid: userID },
})

console.log('User Fields', userFields)

const recentEntries = await $fetch('/api/getRecentEntries')

console.log('Recent Entries', recentEntries)

for (let i = 0; i < userFields.length; i++) {
	const health = await $fetch('/api/getHealth', {
		params: { crop: userFields[i].crop_type },
	})

	fields.value.push({
		name: userFields[i].field_name,
		health: health,
		yield: userFields[i].field_tph,
		cropType: userFields[i].crop_type,
	})
}
</script>
