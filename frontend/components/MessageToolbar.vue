<template>
	<div class="w-full flex h-full justify-between items-center gap-2">
		<Textarea v-model="message" class="w-full h-full" :invalid="!hasMessage" @keydown.enter.prevent="sendMessage" />
		<Button icon="pi pi-send" severity="secondary" text size="large" @click="sendMessage" />
	</div>
	<Toast />
</template>

<script setup>
import { ref } from 'vue'
import { useToast } from 'primevue/usetoast'

const toast = useToast()
const message = ref('')
const currentUser = ref(null)

const hasMessage = ref(true)

const fetchUser = async () => {
	const user = useSupabaseUser()
	const response = await $fetch(`/api/getUser?user_id=${user.value.id}`)
	currentUser.value = response
}

const sendMessage = async () => {
	if (message.value.trim() !== '') {
		try {
			console.log(message.value)
			await $fetch('/api/sendMessage', {
				method: 'POST',
				body: {
					team_id: currentUser.value.team_id,
					user_name: currentUser.value.full_name,
					user_email: currentUser.value.email,
					message: message.value,
				},
			})
		} catch (error) {
			toast.add({
				severity: 'error',
				summary: 'Error',
				detail: 'Failed to send message, please try again later.',
				life: 3000,
			})
		} finally {
			message.value = ''
			hasMessage.value = true
		}
	} else {
		toast.add({
			severity: 'warn',
			summary: 'Message Empty',
			detail: 'Please enter a message to send',
			life: 3000,
		})
		hasMessage.value = false
	}
}

onMounted(async () => {
	await fetchUser()
})
</script>
