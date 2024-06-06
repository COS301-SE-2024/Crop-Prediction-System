<template>
	<div class="card">
		<TreeTable :value="teams">
			<template #header>
				<div class="text-xl font-bold">File Viewer</div>
			</template>
			<Column field="team" header="Team" :expander="true"></Column>
			<Column field="name" header="Name"></Column>
			<Column field="id" header="ID"></Column>
			<!-- <Column header="Role" v-if="not at first level"> -->
			<Column header="Role">
				<template #body>
					<!-- <p>{{ teams[slotProps.data.key].data.role }}</p> -->
					<Dropdown :options="roles" class="w-full" v-model="teams[0].data.role" />
				</template>
			</Column>
			<Column headerStyle="width: 10rem">
				<template #body>
					<div class="flex flex-wrap gap-2">
						<Button type="button" icon="pi pi-trash" rounded severity="danger" />
						<Button type="button" icon="pi pi-pencil" rounded severity="success" />
					</div>
				</template>
			</Column>
			<template #footer>
				<div class="flex justify-between">
					<div class="flex justify-content-start">
						<Button icon="pi pi-plus" label="Add Team" />
					</div>
					<div class="flex justify-content-end gap-3">
						<Button icon="pi pi-times" label="Cancel" severity="secondary" />
						<Button icon="pi pi-save" label="Save" />
					</div>
				</div>
			</template>
		</TreeTable>
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

const teams = ref([
	{
		key: 0,
		data: {
			team: 'Team 1',
			role: 'Farm Manager', // Make sure role is defined here
		},
		label: 'Team 1',
		children: [
			{
				key: 1,
				data: {
					id: '1',
					name: 'John Doe',
					role: 'Data Analyst',
				},
				label: 'John Doe',
			},
			{
				key: 2,
				data: {
					id: '2',
					name: 'Jane Doe',
					role: 'Farmer',
				},
				label: 'Jane Doe',
			},
		],
	},
])

// function addUser(teamIndex) {
// 	if (newUser.value) {
// 		teams.value[teamIndex].users.push(newUser.value)
// 		newUser.value = ''
// 	}
// }

// function removeUser(teamIndex, userIndex) {
// 	teams.value[teamIndex].users.splice(userIndex, 1)
// }
</script>
