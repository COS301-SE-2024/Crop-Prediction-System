<template>
	<nav class="p-2 px-5 z-50 w-full sm:w-full md:w-full shadow-md dark:bg-surface-400/10 sticky top-0 left-0">
		<div class="flex justify-between xl:justify-normal xl:grid xl:grid-cols-3 h-full w-full">
			<Sidebar />
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
				<!-- <div class="p-5 sm:p-0">
					<i class="pi pi-bell" style="font-size: 1.5rem" />
				</div> -->
				<Button @click="toggleProfile" severity="secondary" text size="large" class="text-2xl"
					><i class="pi pi-user" style="font-size: 1.5rem"
				/></Button>
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
import OverlayPanel from 'primevue/overlaypanel'

const user = useSupabaseUser()
const client = useSupabaseClient()

const colorMode = useColorMode()

const settingsSwitch = ref(false)

const op = ref<OverlayPanel | null>(null)
const settingsPanel = ref<OverlayPanel | null>(null)

const items = computed(() => [
	{
		label: user.value?.email,
		icon: 'pi pi-user',
		command: () => {
			navigateTo('/settings')
		},
	},
	{
		label: 'Manage Teams',
		icon: 'pi pi-users',
		command: () => {
			navigateTo('/team/manage')
		},
	},
	{
		label: 'IoT Devices',
		icon: 'pi pi-globe',
		command: () => {
			navigateTo('/settings')
		},
	},
	{
		label: 'Toggle Theme',
		icon: colorMode.preference == 'dark' ? 'pi pi-sun' : 'pi pi-moon',
		command: () => {
			setColorTheme(colorMode.preference == 'dark' ? 'light' : 'dark')
		},
	},
	{
		label: 'Help',
		icon: 'pi pi-question-circle',
		command: () => {
			navigateTo('/help')
		},
	},
	{
		label: 'Settings',
		icon: 'pi pi-cog',
		command: () => {
			navigateTo('/settings')
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

onMounted(() => {
  if (colorMode && colorMode.preference === 'system' && typeof window !== 'undefined') {
    const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
  }
})

const setColorTheme = (newTheme: 'light' | 'dark') => {
  if (colorMode) {
    colorMode.preference = newTheme
  }
}
</script>
