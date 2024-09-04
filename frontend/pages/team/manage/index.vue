<template>
	<div class="flex flex-col gap-5 px-4 sm:px-6 md:px-8 lg:px-0 py-4 sm:py-6 md:py-8 lg:py-0">
		<DataTable :value="users" responsiveLayout="scroll" tableStyle="min-width: 35rem" columnResizeMode="expand">
			<template #header>
				<h1 class="text-lg font-bold dark:text-white">Team Members</h1>
			</template>
			<Column field="name" header="Name"></Column>
			<Column field="email" header="Email Address"></Column>
			<Column field="role" header="Role"></Column>
			<template #footer>
				<div class="flex flex-row justify-end w-full">
					<Button label="Invite Member" icon="pi pi-plus" size="small" @click="visible = true" />
				</div>
			</template>
		</DataTable>

		<Dialog v-model:visible="visible" modal header="Add Member" :style="{ width: '25rem' }">
			<div class="flex flex-col items-start justify-between gap-4">
				<div class="flex flex-col gap-2 w-full">
					<label for="newUserEmail">User Email</label>
					<InputText id="newUserEmail" v-model="newUserEmail" type="email" aria-describedby="username-help" />
					<small>We will send an invite to this email to join your team.</small>
				</div>
				<Dropdown v-model="role" :options="roles" optionLabel="name" placeholder="Select Member Role" class="w-full" />
				<Button label="Send Invite" icon="pi pi-send" class="w-full" @click="send" :loading="loading" />
			</div>
		</Dialog>
	</div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// TODO: Fill table with data from new api call that needs to be implemented
definePageMeta({
	middleware: 'auth',
})

const role = ref()
const roles = ref([
	{ name: 'Farmer', value: 'farmer' },
	{ name: 'Data Analyst', value: 'data_analyst' },
])

const users = ref([
	{ name: 'John Doe', email: 'john.doe@example.com', role: 'Farm Manager' },
	{ name: 'Jane Smith', email: 'jane.smith@example.com', role: 'Farmer' },
	{ name: 'James Brown', email: 'james.brown@example.com', role: 'Data Analyst' },
])

const visible = ref(false)
const newUserEmail = ref('')
const loading = ref(false)

const send = async () => {
	loading.value = true
	const currentUser = useSupabaseUser()
	const teamID = await $fetch('/api/getTeamID', {
		params: { userid: currentUser?.value?.id },
	})

	try {
		await $fetch('/api/send', {
			params: { to: newUserEmail.value, team_id: teamID.team_id },
		})
	} catch (error) {
		console.error('Error sending invite:', error)
	} finally {
		loading.value = false
	}
}
</script>
