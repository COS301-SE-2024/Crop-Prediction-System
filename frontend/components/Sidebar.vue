<template>
	<Sidebar v-model:visible="visible">
		<template #container="{ closeCallback }">
			<div class="flex flex-col justify-between h-full items-center p-4">
				<div class="flex flex-col gap-3 items-center w-full">
					<div class="flex flex-row justify-between items-center w-full">
						<img src="../assets/logo.png" alt="Logo" class="object-fill w-1/2 h-full dark:hidden block" />
						<img src="../assets/logo-alt.png" alt="Logo" class="object-fill w-1/2 h-full hidden dark:block" />
						<Button icon="pi pi-times" @click="closeCallback" text severity="secondary" aria-label="Filter" />
					</div>
					<div class="w-full max-h-[calc(100vh-200px)] overflow-y-auto">
						<Menu />
					</div>
				</div>
				<div class="space-y-2 w-full">
					<AccountManage :email="user?.email" />
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
							<template #option="{ option }">
								<div class="flex flex-row justify-between items-center w-full">
									<span>{{ option.name }}</span>
									<Badge :value="option.alerts" severity="danger" />
								</div>
							</template>
						</Dropdown>
						<!-- Sum of all option alerts minus the selected city alerts -->
						<Badge
							:value="cities.reduce((acc, city) => acc + city.alerts, 0) - selectedCity?.alerts"
							severity="danger"
						/>
					</div>
				</div>
			</div>
		</template>
	</Sidebar>
	<Button icon="pi pi-bars" @click="visible = true" text severity="secondary" aria-label="Filter" />
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Sidebar from 'primevue/sidebar'
import Menu from '../components/NavigationMenu.vue'
import Avatar from 'primevue/avatar'
import Button from 'primevue/button'
import Dropdown from 'primevue/dropdown'
import AccountManage from '~/components/AccountManage.vue'

const user = useSupabaseUser()

const visible = ref(false)

const op = ref()

const cities = ref([
	{ name: 'Buffelsfontein', alerts: 2 },
	{ name: 'Plaas ander kant die dam', alerts: 4 },
])
const selectedCity = ref(cities.value[0])
</script>
