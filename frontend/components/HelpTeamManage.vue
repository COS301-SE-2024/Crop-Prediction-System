<template>
	<Card v-if="activeIndex === 5" class="mt-6 p-5">
		<template #content>
			<div class="w-full flex flex-col justify-between items-start gap-4">
				<h1 class="text-2xl font-semibold">Team Management Help</h1>
				<p>
					Welcome to the Team Management page! This page allows you to manage your team members, including viewing
					member details, editing roles, inviting new members, and removing members from your team.
				</p>
				<h2 class="text-xl font-semibold">Viewing Team Members</h2>
				<p>The table below displays all the members of your team:</p>
				<DataTable
					:value="team"
					responsiveLayout="scroll"
					tableStyle="min-width: 50rem"
					columnResizeMode="expand"
					class="w-full mt-4"
				>
					<Column field="full_name" header="Name"></Column>
					<Column field="email" header="Email Address"></Column>
					<Column field="role" header="Role"></Column>
					<Column header="Actions">
						<template #body>
							<Button outlined rounded icon="pi pi-pencil" severity="info" size="small" class="mr-2" />
							<Button outlined rounded icon="pi pi-trash" severity="danger" size="small" />
						</template>
					</Column>
				</DataTable>
				<p>You can see each member's name, email address, and role within your team.</p>

				<h2 class="text-xl font-semibold">Editing Member Roles</h2>
				<p>To edit a member's role:</p>
				<ul class="list-disc ml-6">
					<li>
						Click the <Button outlined rounded icon="pi pi-pencil" severity="info" size="small" class="mr-2" /> button
						next to the member's name.
					</li>
					<li>A dropdown will appear in the Role column, allowing you to select a new role.</li>
					<li>
						After selecting the new role, click the
						<Button icon="pi pi-check" outlined rounded severity="info" size="small" /> button to save the changes.
					</li>
				</ul>
				<p>Roles available:</p>
				<ul class="list-disc ml-6">
					<li><strong>Farm Manager:</strong> Has full access to manage the team and fields.</li>
					<li><strong>Farmer:</strong> Can view and update field data.</li>
					<li><strong>Data Analyst:</strong> Can analyze field data but cannot make changes.</li>
				</ul>

				<h2 class="text-xl font-semibold">Inviting New Members</h2>
				<p>To invite a new member to your team:</p>
				<ul class="list-disc ml-6">
					<li>
						Click the
						<Button
							label="Invite Member"
							icon="pi pi-plus"
							size="small"
							class="p-button-sm"
							@click="inviteActive = true"
						/>
						button at the bottom of the table.
					</li>
					<li>A dialog will appear where you can enter the new member's email and select their role.</li>
					<li>
						Click the <Button label="Send Invite" icon="pi pi-send" class="p-button-sm" /> button to send the
						invitation.
					</li>
				</ul>
				<Dialog header="Add Member" modal v-model:visible="inviteActive" :style="{ width: '25rem' }">
					<div class="flex flex-col items-start justify-between gap-4">
						<div class="flex flex-col gap-2 w-full">
							<label for="newUserEmail">User Email</label>
							<InputText id="newUserEmail" placeholder="Enter email address" class="w-full" />
							<small>We will send an invite to this email to join your team.</small>
						</div>
						<Dropdown :options="roles" optionLabel="name" placeholder="Select Member Role" class="w-full" />
						<Button label="Send Invite" icon="pi pi-send" class="w-full" />
					</div>
				</Dialog>

				<h2 class="text-xl font-semibold">Removing Members</h2>
				<p>To remove a member from your team:</p>
				<ul class="list-disc ml-6">
					<li>
						Click the
						<Button outlined rounded icon="pi pi-trash" severity="danger" size="small" @click="deleteActive = true" />
						button next to the member's name.
					</li>
					<li>A confirmation dialog will appear asking if you're sure you want to remove the member.</li>
					<li>
						Click the <Button label="Delete" severity="danger" class="p-button-sm" /> button to confirm the removal.
					</li>
				</ul>
				<Dialog header="Confirm" modal v-model:visible="deleteActive" :style="{ width: '25rem' }">
					<p>Are you sure you want to remove this user from the team?</p>
					<div class="flex gap-3 justify-end">
						<Button label="Cancel" severity="secondary" outlined class="p-button-sm" />
						<Button label="Delete" severity="danger" class="p-button-sm" />
					</div>
				</Dialog>

				<h2 class="text-xl font-semibold">Permissions</h2>
				<p>Only users with the <strong>Farm Manager</strong> role can perform the following actions:</p>
				<ul class="list-disc ml-6">
					<li>Edit member roles.</li>
					<li>Invite new members.</li>
					<li>Remove members from the team.</li>
				</ul>
				<p>If you do not have the required permissions, these actions will be disabled.</p>

				<h2 class="text-xl font-semibold">Success Message</h2>
				<p>After performing an action, a success message will appear confirming that the action has been completed.</p>
				<p>Example:</p>
				<div class="flex items-center gap-2">
					<i class="pi pi-check-circle text-green-500"></i>
					<span class="text-green-500">Action completed successfully!</span>
				</div>
			</div>
		</template>
	</Card>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
	activeIndex: {
		type: Number,
		default: 0,
	},
})

const inviteActive = ref(false)
const deleteActive = ref(false)

// Sample team data
const team = ref([
	{
		id: 'xxxx-xxxx-xxxx-xxxx',
		full_name: 'John Doe',
		email: 'email@example.com',
		role: 'Farm Manager',
	},

	{
		id: 'xxxx-xxxx-xxxx-xxxx',
		full_name: 'Jack Smith',
		email: 'email@example.com',
		role: 'Farmer',
	},
])

// Roles for dropdown
const roles = ref([
	{ name: 'Farm Manager', value: 'farm_manager' },
	{ name: 'Farmer', value: 'farmer' },
	{ name: 'Data Analyst', value: 'data_analyst' },
])
</script>
