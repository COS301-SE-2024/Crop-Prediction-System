<template>
	<nav class="p-2 h-[65px] z-50 w-full shadow-md">
		<div class="flex justify-between items-center h-full">
			<Sidebar />
			<img src="../assets/logo.png" alt="Logo" class="h-full object-cover self-center" />
			<div class="flex flex-row items-center gap-4">
				<i class="pi pi-bell" style="font-size: 1.5rem" />
				<i class="pi pi-user" @click="toggle" style="font-size: 1.5rem" />
				<i class="pi pi-cog" style="font-size: 1.5rem" />
				<OverlayPanel ref="op" class="w-56 border border-surface-border">
					<div class="flex flex-col items-center gap-5">
						<h3>{{ user.email }}</h3>
						<Button label="Log Out" severity="danger" class="w-full" @click="signOut" />
					</div>
				</OverlayPanel>
			</div>
		</div>
	</nav>
</template>

<script setup lang="ts">
import Sidebar from '../components/Sidebar.vue'
import { ref } from 'vue'
import Button from 'primevue/button'

const user = useSupabaseUser()
const client = useSupabaseClient()

const op = ref()

const toggle = (event) => {
	op.value.toggle(event)
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
</script>
