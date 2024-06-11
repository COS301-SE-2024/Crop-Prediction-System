<template>
	<div class="flex justify-center px-4 sm:px-6 lg:px-8 mt-3">
		<TabView :activeIndex="activeTabIndex" @onTabChange="handleTabChange" class="w-full sm:w-10/12 lg:w-5/12">
			<TabPanel v-for="(tab, index) in settings" :key="index">
				<template #header>
					<i :class="tab.icon" class="pr-2"></i>
					{{ tab.label }}
				</template>
				<div class="p-4">
					<div v-if="tab.label === 'Account'" class="space-y-6">
						<div>
							<h1 class="text-xl sm:text-2xl">Account</h1>
							<p class="text-sm sm:text-base text-surface-400">Manage your account settings and other preferences</p>
						</div>
						<div class="w-full flex flex-col gap-4 sm:gap-6">
							<div class="flex flex-col gap-2 sm:gap-4">
								<label for="first_name" class="block text-sm sm:text-base">First Name</label>
								<InputText id="first_name" v-model="first_name" class="w-full text-sm sm:text-base" />
							</div>
							<div class="flex flex-col gap-2 sm:gap-4">
								<label for="last_name" class="block text-sm sm:text-base">Last Name</label>
								<InputText id="last_name" v-model="last_name" class="w-full text-sm sm:text-base" />
							</div>
							<div class="flex flex-col gap-2 sm:gap-4">
								<label for="email" class="block text-sm sm:text-base">Email</label>
								<InputText id="email" v-model="email" class="w-full text-sm sm:text-base" />
							</div>
							<div class="flex flex-col gap-2 sm:gap-4">
								<p class="text-sm sm:text-base">Password: <a href="#" class="text-primary-500 underline">Email Reset Link</a></p>
							</div>
						</div>
						<div>
							<div class="field flex items-center gap-2 sm:gap-4">
								<p class="text-sm sm:text-base">Dark Mode</p>
								<InputSwitch v-model="checked" @change="setColorTheme(checked ? 'dark' : 'light')" />
							</div>
						</div>
						<div>
							<div class="flex flex-row justify-end gap-2 sm:gap-4">
								<Button label="Cancel" severity="secondary" class="text-sm sm:text-base" />
								<Button label="Save" class="text-sm sm:text-base" />
							</div>
						</div>
					</div>
					<div v-else-if="tab.label === 'Teams'" class="space-y-6">
						<div class="flex flex-col sm:flex-row sm:justify-between sm:items-center">
							<div>
								<h1 class="text-xl sm:text-2xl">Teams</h1>
								<p class="text-sm sm:text-base text-surface-400">Manage your teams and team members</p>
							</div>
							<Button label="Add Team" icon="pi pi-plus" class="p-button-success text-sm sm:text-base mt-4 sm:mt-0" />
						</div>
						<div class="treetable-container text-xs sm:text-sm">
							<TreeTable :value="teams">
								<Column expander style="width: 3em"></Column>
								<Column field="team" header="Team"></Column>
								<Column field="id" header="User ID"></Column>
								<Column field="name" header="Name"></Column>
								<Column field="role" header="Role"></Column>
								<Column field="actions" header="Actions">
									<template #body="slotProps">
										<div class="flex gap-2">
											<Button
												icon="pi pi-pencil"
												class="p-button-rounded p-button-text"
												@click="editProduct(slotProps.data)"
												severity="info"
											></Button>
											<Button
												icon="pi pi-trash"
												class="p-button-rounded p-button-text"
												@click="deleteProduct(slotProps.data)"
												severity="danger"
											></Button>
										</div>
									</template>
								</Column>
							</TreeTable>
						</div>
					</div>
					<div v-else-if="tab.label === 'Devices'">
						<h1 class="text-xl sm:text-2xl">Devices</h1>
						<DataTable :value="devices">
							<Column field="name" header="Device Name"></Column>
							<Column field="status" header="Status"></Column>
						</DataTable>
					</div>
				</div>
			</TabPanel>
		</TabView>
	</div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import TabView from 'primevue/tabview'
import TabPanel from 'primevue/tabpanel'
import InputText from 'primevue/inputtext'
import Password from 'primevue/password'
import Button from 'primevue/button'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Dropdown from 'primevue/dropdown'
import MultiSelect from 'primevue/multiselect'

const settings = ref([
	{ label: 'Account', icon: 'pi pi-user' },
	{ label: 'Teams', icon: 'pi pi-users' },
	{ label: 'Devices', icon: 'pi pi-globe' },
])

const activeTabIndex = ref(0)

const account = ref({
	name: '',
	email: '',
	password: '',
})

const checked = ref(useColorMode().preference === 'dark')

type Theme = 'light' | 'dark'

function setColorTheme(theme: Theme) {
	useColorMode().preference = theme
}

const teams = ref([
	{
		key: 0,
		data: {
			team: 'Team 1',
			id: '1',
		},
		label: 'Team 1',
		children: [
			{
				key: 1,
				data: {
					id: '1',
					name: 'John Doe',
					role: 'Admin',
				},
				label: 'John Doe',
			},
			{
				key: 2,
				data: {
					id: '2',
					name: 'Jane Doe',
					role: 'User',
				},
				label: 'Jane Doe',
			},
		],
	},
])

const newUser = ref('')

const devices = ref([
	{ name: 'Device 1', status: 'Online' },
	{ name: 'Device 2', status: 'Offline' },
])

const themes = ref([
	{ label: 'Light', value: 'light' },
	{ label: 'Dark', value: 'dark' },
])

const items = ref([
	{ label: 'Item 1', value: 'item1' },
	{ label: 'Item 2', value: 'item2' },
	{ label: 'Item 3', value: 'item3' },
])

const settingsData = ref({
	theme: null,
	preferredItems: [],
})

function handleTabChange(event) {
	activeTabIndex.value = event.index
}

function addUser(teamIndex) {
	if (newUser.value) {
		teams.value[teamIndex].users.push(newUser.value)
		newUser.value = ''
	}
}

function removeUser(teamIndex, userIndex) {
	teams.value[teamIndex].users.splice(userIndex, 1)
}
</script>

<style>
.card {
	max-width: 800px;
	margin: 0 auto;
}

.treetable-container {
	width: 100%;
	overflow-x: auto; /* Enable horizontal scrolling */
}
</style>
