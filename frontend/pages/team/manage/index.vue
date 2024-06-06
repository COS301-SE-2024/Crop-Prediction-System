<template>
	<div>
		<div class="justify-between flex items-center">
			<div class="flex gap-5">
				<h1 class="text-2xl font-semibold dark:text-white">Manage Team</h1>
				<div class="flex items-center gap-2">
					<Dropdown
						v-model="selectedCity"
						:options="cities"
						optionLabel="name"
						placeholder="Switch Team"
						checkmark
						:highlightOnSelect="true"
						class="w-full text-xs"
						filter
					>
					</Dropdown>
				</div>
			</div>
			<div class="flex gap-5">
				<Button label="Add Team Member" icon="pi pi-plus" class="text-sm" />
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import TreeTable from 'primevue/treeTable'
import Column from 'primevue/column'
import Dropdown from 'primevue/dropdown'
import Button from 'primevue/button'

definePageMeta({
	middleware: 'auth',
})

const roles = ref(['Farm Manager', 'Farmer', 'Data Analyst', 'Unassigned'])

const cities = ref([
	{ name: 'Buffelsfontein', alerts: 2 },
	{ name: 'Plaas ander kant die dam', alerts: 4 },
])
const selectedCity = ref(cities.value[0])
</script>
