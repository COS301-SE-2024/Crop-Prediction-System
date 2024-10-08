<template>
	<nav class="p-2 px-5 z-50 w-full sm:w-full md:w-full shadow-sm bg-surface-100 dark:bg-surface-800 sticky top-0 left-0">
		<div class="flex justify-between xl:justify-normal xl:grid xl:grid-cols-3 h-full w-full">
			<Sidebar />
			<NuxtLink to="/" class="text-2xl font-[500] text-primary-500 justify-self-center self-center h-full">
				<img src="../assets/logo.png" alt="Logo" class="w-36 xl:h-14 xl:w-auto object-cover dark:hidden block" />
				<img src="../assets/logo-alt.png" alt="Logo" class="w-36 xl:h-14 xl:w-auto object-cover hidden dark:block" />
			</NuxtLink>
			<OverlayPanel ref="op" class="flex flex-col justify-center items-center mt-2">
				<div class="flex flex-col items-center justify-center gap-5">
					<Menu :model="items">
						<template #item="{ item }">
							<a :href="item.url" class="flex flex-row gap-2 items-center p-2 cursor-pointer">
								<span :class="item.icon" />
								<span>{{ item.label }}</span>
							</a>
						</template>
					</Menu>
				</div>
			</OverlayPanel>
			<OverlayPanel
				ref="settingsPanel"
				class="flex flex-col justify-center items-center p-2 bg-surface-100 dark:bg-surface-800 rounded-md border-black border-2"
			>
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
			<div class="flex flex-row items-center h-full justify-end justify-self-end">
				<!-- <div class="p-5 sm:p-0">
					<i class="pi pi-bell" style="font-size: 1.5rem" />
				</div> -->
				<i
					class="pi pi-question-circle"
					style="font-size: 1.5rem; padding-top: 16px; padding-bottom: 16px; padding-left: 8px; padding-right: 8px"
					:class="'text-surface-500 dark:text-surface-300 rounded-md hover:bg-surface-300/20 hover:cursor-pointer'"
					@click="navigateTo('/help')"
				/>
				<i
					class="pi pi-comment"
					style="
						font-size: 1.5rem;
						position: relative;
						padding-top: 16px;
						padding-bottom: 16px;
						padding-left: 8px;
						padding-right: 8px;
					"
					:class="'text-surface-500 dark:text-surface-300 hover:bg-surface-300/20 rounded-md hover:cursor-pointer'"
					@click="navigateTo('/team/chat')"
				>
					<div
						v-show="unreadMessages > 0"
						class="absolute -top-[-10px] -right-[-1px] text-xs leading-[1rem] text-center inline-block p-0 px-1 min-w-[1rem] h-[1rem] rounded-full bg-primary font-bold text-primary-inverse"
					>
						<p style="font-family: Open Sans">{{ unreadMessages }}</p>
					</div>
				</i>
				<i
					class="pi pi-user"
					style="font-size: 1.5rem; padding-top: 16px; padding-bottom: 16px; padding-left: 8px; padding-right: 8px"
					:class="'text-surface-500 dark:text-surface-300 rounded-md hover:bg-surface-300/20 hover:cursor-pointer'"
					@click="toggleProfile"
				/>
			</div>
		</div>
		<Toast />
	</nav>
</template>

<script setup lang="ts">
import Sidebar from '../components/Sidebar.vue'
import { ref } from 'vue'
import OverlayPanel from 'primevue/overlaypanel'
import { useToast } from 'primevue/usetoast'

const toast = useToast()
const user = useSupabaseUser()
const client = useSupabaseClient()

const op = ref<OverlayPanel | null>(null)
const settingsPanel = ref<OverlayPanel | null>(null)

const currentUser = ref()
const fetchUser = async () => {
	const user = useSupabaseUser()
	const response = await $fetch(`/api/getUser?user_id=${user?.value?.id}`)
	currentUser.value = response
}

const items = computed(() => [
	{
		label: user.value?.email,
		icon: 'pi pi-user',
		url: '/settings',
	},
	{
		label: 'Manage Teams',
		icon: 'pi pi-users',
		url: '/team/manage',
	},
	{
		label: 'Toggle Theme',
		icon: useColorMode().preference == 'dark' ? 'pi pi-sun' : 'pi pi-moon',
		command: () => {
			setColorTheme(useColorMode().preference == 'dark' ? 'light' : 'dark')
		},
	},
	{
		label: 'Acknowledgements',
		icon: 'pi pi-info-circle',
		url: '/acknowledgements',
	},
	{
		label: 'Settings',
		icon: 'pi pi-cog',
		url: '/settings',
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

// get unread messages
const unreadMessages = useState('unreadMessages', () => 0)

const supabase = useSupabaseClient()
const route = useRoute()

onMounted(() => {
	fetchUser()
	// Ensure the theme is correctly initialized on the first load
	if (useColorMode().preference === 'system' && typeof window !== 'undefined') {
		const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
		setColorTheme(systemTheme)
	}

	// Getting unread messages
	const subscription = supabase
		.channel('public:team_chat')
		.on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'team_chat' }, (payload) => {
			if (payload.new.team_id === currentUser.value.team_id) {
				// Increment unread messages if not on the /team/chat page
				if (route.path !== '/team/chat') {
					unreadMessages.value += 1
					toast.add({
						severity: 'info',
						summary: 'New Message',
						detail: `New message received from ${payload.new.user_name}`,
						life: 3000,
					})
				}
			}
		})
		.subscribe()

	// Cleanup on unmount
	onUnmounted(() => {
		supabase.removeChannel(subscription)
	})
})
</script>
