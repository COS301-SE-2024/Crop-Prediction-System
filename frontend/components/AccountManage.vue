<template>
	<div class="flex justify-content-center w-full">
		<OverlayPanel ref="op">
			<div class="flex flex-col w-full">
				<Menu :model="items" class="w-[200px]" />
			</div>
		</OverlayPanel>
		<div
			class="w-full flex flex-row gap-3 items-center dark:hover:bg-surface-400/10 hover:bg-surface-100 cursor-pointer p-2 rounded-lg"
			@click="toggle"
		>
			<Avatar icon="pi pi-user" size="large" shape="circle" />
			<h1>{{ props.email }}</h1>
		</div>
	</div>
</template>

<script setup>
import { ref } from 'vue'

const client = useSupabaseClient()

const op = ref()

const toggle = (event) => {
	op.value.toggle(event)
}

const props = defineProps({
	email: {
		type: String,
		required: true,
	},
})

const items = ref([
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
