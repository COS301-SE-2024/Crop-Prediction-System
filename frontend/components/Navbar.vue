<template>
	<nav class="p-2 px-5 z-50 w-full shadow-md dark:bg-surface-900">
		<div class="flex justify-between xl:justify-normal xl:grid xl:grid-cols-3 h-full w-full">
			<Sidebar class="justify-self-start" />
			<NuxtLink to="/" class="text-2xl font-[500] text-primary-500 justify-self-center self-center h-full">
				<img src="../assets/logo.png" alt="Logo" class="w-36 xl:h-14 xl:w-auto object-cover dark:hidden block" />
				<img src="../assets/logo-alt.png" alt="Logo" class="w-36 xl:h-14 xl:w-auto object-cover hidden dark:block" />
			</NuxtLink>
			<OverlayPanel ref="op" class="w-60 flex flex-col justify-center items-center">
				<div class="flex flex-col items-center justify-center gap-5">
					<h3>{{ user.email }}</h3>
					<Button label="Log Out" severity="danger" class="w-full" @click="signOut" />
				</div>
			</OverlayPanel>
			<OverlayPanel ref="settingsPanel" class="w-60 flex flex-col justify-center items-center">
				<div class="flex flex-col items-center justify-center gap-5">
				<div class="flex items-center gap-2">
					<ToggleButton 
						v-model="settingsSwitch" 
						onIcon="pi pi-sun" 
						offIcon="pi pi-moon" 
						onLabel="Light" 
						offLabel="Dark" 
						@click="setColorTheme($colorMode.preference == 'dark' ? 'light' : 'dark')" 
					/>
				</div>
				</div>
			</OverlayPanel>
			<div class="flex flex-row items-center justify-end gap-4 justify-self-end dark:text-white">
				<div class="p-5 sm:p-0">
					<i class="pi pi-bell" style="font-size: 1.5rem" />
				</div>
				<div class="hidden sm:block">
					<i class="pi pi-user" @click="toggleProfile" style="font-size: 1.5rem" />
				</div>
				<div class="hidden sm:block">
					<i class="pi pi-cog" @click="toggleSettings" style="font-size: 1.5rem" />
				</div>
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

const user = useSupabaseUser()
const client = useSupabaseClient()

const settingsSwitch = ref(false);

const op = ref<OverlayPanel | null>(null);
const settingsPanel = ref<OverlayPanel | null>(null);

const toggleProfile = (event: Event) => {
  if (op.value) {
    op.value.toggle(event);
  }
};

const toggleSettings = (event: Event) => {
  if (settingsPanel.value) {
    settingsPanel.value.toggle(event);
  }
};

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