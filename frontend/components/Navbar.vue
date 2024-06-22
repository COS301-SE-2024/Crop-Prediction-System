<template>
	<nav class="p-2 px-5 z-50 w-full sm:w-full md:w-full shadow-md dark:bg-surface-400/10 sticky top-0 left-0">
		<div class="flex justify-between xl:justify-normal xl:grid xl:grid-cols-3 h-full w-full">
			<Sidebar class="justify-self-start" />
			<NuxtLink to="/" class="text-2xl font-[500] text-primary-500 justify-self-center self-center h-full">
				<img src="../assets/logo.png" alt="Logo" class="w-36 xl:h-14 xl:w-auto object-cover dark:hidden block" />
				<img src="../assets/logo-alt.png" alt="Logo" class="w-36 xl:h-14 xl:w-auto object-cover hidden dark:block" />
			</NuxtLink>
			<OverlayPanel ref="op" class="flex flex-col justify-center items-center mt-2">
				<div class="flex flex-col items-center justify-center gap-5">
					<Menu :model="items" />
				</div>
			</OverlayPanel>
			<OverlayPanel ref="settingsPanel" class="flex flex-col justify-center items-center p-2">
				<!-- system status showing operation -->
				<div class="w-full grid gap-2">
					<Menu :model="status">
						<template #item="{ item }">
							<div class="flex items-center gap-2 p-2">
								<i :class="`${item.icon} text-${item.status === 'good' ? 'green' : 'red'}-400`" class="text-xs" />
								<span>{{ item.label }}</span>
							</div>
						</template>
					</Menu>
				</div>
			</OverlayPanel>
			<div class="flex flex-row items-center justify-end gap-4 justify-self-end dark:text-white cursor-pointer opacity-60">
				<!-- System Status -->
				<div class="hidden sm:block">
					<!-- green dot if good -->
					<div class="flex items-center gap-1 text-xs border p-2 rounded-lg" @click="toggleStatus">
						<i class="pi pi-circle-on text-xs text-green-400" />
						<span>System Status</span>
					</div>
				</div>
				<div class="p-5 sm:p-0">
					<i class="pi pi-bell" style="font-size: 1.5rem" />
				</div>
				<div>
					<i class="pi pi-user" @click="toggleProfile" style="font-size: 1.5rem" />
				</div>
				<!-- <div class="hidden sm:block">
			<i class="pi pi-cog" @click="toggleSettings" style="font-size: 1.5rem" />
		  </div> -->
			</div>
		</div>
	</nav>
</template>

<script setup lang="ts">
import Sidebar from '../components/Sidebar.vue'
import { ref } from 'vue'
import Button from 'primevue/button'
import OverlayPanel from 'primevue/overlaypanel'
import ToggleButton from 'primevue/togglebutton'
import { useColorMode } from '@vueuse/core'

const user = useSupabaseUser()
const client = useSupabaseClient()

const settingsSwitch = ref(false)

const op = ref<OverlayPanel | null>(null)
const settingsPanel = ref<OverlayPanel | null>(null)

const items = ref([
	{
		label: user.value?.email,
		icon: 'pi pi-user',
		command: () => {
			window.location.href = '/settings'
		},
	},
	{
		label: 'Manage Teams',
		icon: 'pi pi-users',
		command: () => {
			window.location.href = '/teams'
		},
	},
	{
		label: 'IoT Devices',
		icon: 'pi pi-globe',
		command: () => {
			window.location.href = '/devices'
		},
	},
	{
		label: 'Toggle Theme',
		icon: useColorMode().preference == 'dark' ? 'pi pi-sun' : 'pi pi-moon',
		command: () => {
			setColorTheme(useColorMode().preference == 'dark' ? 'light' : 'dark')
		},
	},
	{
		label: 'Settings',
		icon: 'pi pi-cog',
		command: () => {
			window.location.href = '/settings'
		},
	},
	{
		label: 'Logout',
		icon: 'pi pi-sign-out',
		command: () => {
			signOut()
		},
	},
])

// the whole system status thing
const status = ref([
	{ label: 'API', icon: 'pi pi-circle-on', status: 'good' },
	{ label: 'Storage', icon: 'pi pi-circle-on', status: 'good' },
	{ label: 'Database', icon: 'pi pi-circle-on', status: 'error' },
	{ label: 'Analytics', icon: 'pi pi-circle-on', status: 'good' },
	{ label: 'ML Model', icon: 'pi pi-circle-on', status: 'error' },
])

const toggleProfile = (event: Event) => {
	if (op.value) {
		op.value.toggle(event)
	}
}

const toggleStatus = (event: Event) => {
	if (settingsPanel.value) {
		settingsPanel.value.toggle(event)
	}
}

const signOut = async () => {
	try {
		const { error } = await client.auth.signOut()
		if (!error) {
			navigateTo('/login')
		} else {
			throw error
		}
	} catch (error) {
		console.log(error)
	}
}

type Theme = 'light' | 'dark'

const setColorTheme = (newTheme: Theme) => {
	useColorMode().preference = newTheme
}
</script>
