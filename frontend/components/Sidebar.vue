<template>
	<Sidebar v-model:visible="visible">
		<template #container="{ closeCallback }">
			<div class="flex flex-col justify-between h-full items-center p-4">
				<div class="flex flex-col gap-3 items-center w-full">
					<div class="flex flex-row justify-between items-center w-full">
						<img src="../assets/logo.png" alt="Logo" class="object-fill w-1/2 h-full dark:hidden block" />
						<img src="../assets/logo-alt.png" alt="Logo" class="object-fill w-1/2 h-full hidden dark:block" />
						<Button icon="pi pi-times" @click="closeCallback" rounded text severity="secondary" aria-label="Filter" />
					</div>
					<div class="w-full max-h-[calc(100vh-200px)] overflow-y-auto">
						<Menu />
					</div>
				</div>
				<div class="space-y-2 w-full">
					<div
						class="w-full flex flex-row gap-3 items-center dark:hover:bg-surface-400/10 hover:bg-surface-100 cursor-pointer p-2 rounded-lg"
					>
						<Avatar icon="pi pi-user" size="large" shape="circle" />
						<h1>{{ user?.email }}</h1>
					</div>
					<Dropdown
						v-model="selectedCity"
						:options="cities"
						optionLabel="name"
						placeholder="Switch Team"
						checkmark
						:highlightOnSelect="true"
						class="w-full text-xs"
					/>
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

const user = useSupabaseUser()

const visible = ref(false)

const selectedCity = ref()
const cities = ref([
	{ name: 'Buffelsfontein', code: 'NY' },
	{ name: 'Plaas ander kant die dam', code: 'RM' },
])
</script>
