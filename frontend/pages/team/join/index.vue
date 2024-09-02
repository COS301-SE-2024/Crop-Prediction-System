<template>
	<div>
		<Toolbar class="mb-6">
			<template #start>
				<Button outlined label="New" icon="pi pi-plus" size="small" severity="secondary" class="mr-2" />
				<p class="text-primary-600">This is a test</p>
			</template>
		</Toolbar>

		<div class="flex flex-col gap-3 items-center justify-between">
			<InputText type="email" v-model="email" />
			<Button label="Invite User" icon="pi pi-plus" size="small" @click="send" class="mr-2" />
		</div>
	</div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'

const email = ref(null)
const currentUser = useSupabaseUser()
console.log(currentUser.value)

const teamID = await $fetch('/api/getTeamID', {
	params: { userid: currentUser?.value?.id },
})

console.log(teamID.team_id)

const send = async () => {
	await $fetch('/api/send', {
		params: { to: email.value, team_id: teamID.team_id },
	})
}

definePageMeta({
	middleware: 'auth',
})
</script>
