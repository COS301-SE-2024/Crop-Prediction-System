<template>
	<div class="w-full h-screen flex flex-col justify-center items-center p-4 overflow-auto">
		<Card class="p-5 w-80">
			<template #title>
				<h1 class="font-medium my-4">Rest Password</h1>
			</template>
			<template #content>
				<div class="flex flex-col gap-2 items-start">
					<h3 class="font-semibold">Email Address</h3>
					<InputText id="email" type="email" class="w-full" v-model="userEmail" placeholder="email@example.com" />
				</div>
			</template>
			<template #footer>
				<Button :loading="loading" @click="send" label="Send Reset Email" class="w-full" />
			</template>
		</Card>
		<Toast />
	</div>
</template>

<script setup>
import { useToast } from 'primevue/usetoast'

const toast = useToast()
const userEmail = ref('')
const supabase = useSupabaseClient()
const appBaseUrl = useRuntimeConfig().public.appBaseUrl
const loading = ref(false)
const route = useRoute()

const redirectTo = route.query.redirectTo || 'reset-password'

const send = async () => {
	try {
		loading.value = true
		const { data, error } = await supabase.auth.resetPasswordForEmail(userEmail.value, {
			redirectTo: `${appBaseUrl}/confirm?redirectTo=${redirectTo}`,
		})
		console.log(data)
		console.log('error:', error)
	} catch (error) {
		console.log(error)
	} finally {
		loading.value = false
		toast.add({
			severity: 'info',
			summary: 'Email Sent',
			detail: 'An email has been sent to your account to reset your password',
			life: 3000,
		})
	}
}

definePageMeta({
	layout: 'auth',
})
</script>
