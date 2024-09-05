<template>
	<div class="flex flex-col gap-5 px-4 sm:px-6 md:px-8 lg:px-0 py-4 sm:py-6 md:py-8 lg:py-0">
		<DataTable :value="team" responsiveLayout="scroll" tableStyle="min-width: 50rem" columnResizeMode="expand">
			<template #header>
				<h1 class="text-lg font-bold dark:text-white">
					{{ teamOwner.valueOf() === '' ? 'Fetching Team Details...' : `${teamOwner} Team` }}
				</h1>
			</template>

			<!-- Name Column -->
			<Column field="full_name" header="Name"></Column>

			<!-- Email Column -->
			<Column field="email" header="Email Address"></Column>

			<!-- Role Column with Conditional Dropdown -->
			<Column field="role" header="Role">
				<template #body="slotProps">
					<Dropdown
						v-model="slotProps.data.role"
						:options="roles"
						optionLabel="name"
						optionValue="value"
						class="w-full sm:w-[250px]"
						:disabled="editingRoleId !== slotProps.data.id"
					/>
				</template>
			</Column>

			<!-- Actions Column with Trash Button -->
			<Column header="Actions">
				<template #body="slotProps">
					<Button
						outlined
						rounded
						:icon="editingRoleId === slotProps.data.id ? 'pi pi-check' : 'pi pi-pencil'"
						severity="info"
						size="small"
						class="mr-2"
						@click="editRole(slotProps.data.id)"
					/>
					<Button
						outlined
						rounded
						icon="pi pi-trash"
						severity="danger"
						size="small"
						@click="confirmRemove(slotProps.data.id)"
					/>
				</template>
			</Column>

			<template #footer>
				<div class="flex flex-row justify-end w-full">
					<Button label="Invite Member" icon="pi pi-plus" size="small" @click="visible = true" />
				</div>
			</template>
		</DataTable>

		<!-- Dialog for Adding New Member -->
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

		<!-- Confirmation Dialog -->
		<Dialog v-model:visible="confirmVisible" modal header="Confirm" :style="{ width: '25rem' }">
			<p>Are you sure you want to remove this user from the team?</p>
			<div class="flex gap-3 justify-end">
				<Button label="Cancel" severity="secondary" outlined @click="confirmVisible = false" />
				<Button label="Delete" severity="danger" @click="removeFromTeam(selectedUserId)" />
			</div>
		</Dialog>

		<Toast />
	</div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useToast } from 'primevue/usetoast'

// State for the team and editing
const team = ref([])
const teamOwner = ref('')
const editingRoleId = ref(null) // State for row being edited
const visible = ref(false) // State for invite member dialog
const confirmVisible = ref(false) // State for confirmation dialog
const selectedUserId = ref('') // State for the user being removed
const toast = useToast()

onMounted(async () => {
	await getTeamDetails()
})

async function getTeamDetails() {
	try {
		const currentUser = useSupabaseUser()
		const teamID = await $fetch('/api/getTeamID', {
			params: { userid: currentUser?.value?.id },
		})
		const data = await $fetch('/api/getTeamDetails', {
			params: { team_id: teamID.team_id },
		})

		// Check for current user in team and don't show them in the table
		data.forEach((member: any) => {
			if (member.id === currentUser?.value?.id) {
				teamOwner.value = member.full_name
				data.splice(data.indexOf(member), 1)
			}
		})
		team.value = data
	} catch (error) {
		console.error('Error fetching team details:', error)
	}
}

// Dropdown options for role
const role = ref()
const roles = ref([
	{ name: 'Farm Manager', value: 'farm_manager' },
	{ name: 'Farmer', value: 'farmer' },
	{ name: 'Data Analyst', value: 'data_analyst' },
])

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
			params: { to: newUserEmail.value, team_id: teamID.team_id, role: role.value.value },
		})
		toast.add({ severity: 'success', summary: 'Invite Sent', detail: 'Invite sent successfully', life: 3000 })
	} catch (error) {
		console.error('Error sending invite:', error)
		toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to send invite', life: 3000 })
	} finally {
		loading.value = false
		visible.value = false
	}
}

const editRole = async (id: string) => {
	// If the row is being edited (check mark is clicked)
	if (editingRoleId.value === id) {
		const updatedRow = team.value.find((member: any) => member.id === id)

		// Send a request to update the role
		try {
			const response = await $fetch('/api/updateRoles', {
				method: 'POST',
				body: {
					user_id: updatedRow.id,
					role: updatedRow.role, // Use the updated role from the dropdown
				},
			})

			toast.add({ severity: 'success', summary: 'Role Updated', detail: 'User role updated successfully', life: 3000 })
			console.log('Role update response:', response)
		} catch (error) {
			console.error('Error updating role:', error)
			toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to update role', life: 3000 })
		} finally {
			// Stop editing after the role is updated
			editingRoleId.value = null
		}
	} else {
		// Enable editing for the selected row
		editingRoleId.value = id
	}
}
// Function to open the confirmation dialog
const confirmRemove = (id: string) => {
	selectedUserId.value = id
	confirmVisible.value = true
}

// Function to remove user from the team
const removeFromTeam = async (id: string) => {
	confirmVisible.value = false // Close the confirmation dialog

	try {
		await $fetch('/api/removeFromTeam', {
			method: 'PUT',
			params: { user_id: id },
		})

		// Remove the user from the team array
		team.value = team.value.filter((member: any) => member.id !== id)

		toast.add({ severity: 'success', summary: 'User Removed', detail: 'User removed from team successfully', life: 3000 })
	} catch (error) {
		console.error('Error removing user from team:', error)
		toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to remove user from team', life: 3000 })
	}
}
</script>
