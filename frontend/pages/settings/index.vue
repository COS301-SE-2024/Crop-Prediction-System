<template>
	<div class="flex justify-center items-center px-4 sm:px-6 lg:px-8 mt-20">
		<div class="space-y-6 bg-surface-100 dark:bg-surface-800 p-5 text-surface-700 dark:text-surface-0 rounded-md shadow-md">
			<div>
				<h1 class="text-xl sm:text-2xl">Account</h1>
				<p class="text-sm sm:text-base text-surface-600 dark:text-surface-0/60">
					Manage your account settings and other preferences
				</p>
			</div>
			<div class="w-full flex flex-col gap-4 sm:gap-6">
				<div class="flex flex-col gap-2 sm:gap-4">
					<label for="first_name" class="block text-sm sm:text-base">Full Name</label>
					<InputText
						id="first_name"
						v-model="first_name"
						:placeholder="userData.full_name"
						class="w-full text-sm sm:text-base"
					/>
				</div>
				<div class="flex flex-col gap-2 sm:gap-4">
					<label for="email" class="block text-sm sm:text-base">Email</label>
					<InputText id="email" disabled v-model="userData.email" class="w-full text-sm sm:text-base" />
				</div>
			</div>
			<div>
				<div class="field flex items-center gap-2 sm:gap-4">
					<p class="text-sm sm:text-base">Dark Mode</p>
					<InputSwitch v-model="checked" @change="setColorTheme(checked ? 'dark' : 'light')" />
				</div>
			</div>
			<div>
				<div class="flex flex-row justify-end gap-2 sm:gap-4">
					<Button label="Cancel" @click="cancelEditProfileRequest" severity="secondary" />
					<Button label="Save" :loading="loading" @click="updateUserProfile" />
				</div>
			</div>
		</div>
	</div>
	<Toast />
</template>

<script setup lang="ts">
import { ref } from 'vue'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'
import { useToast } from 'primevue/usetoast'
import { getTeamId } from '~/utils/apiUtils'

const toast = useToast()
const user = useSupabaseUser()
const team_id = ref(null)
const userData = ref({
	full_name: '',
	email: '',
})

onMounted(async () => {
	userData.value = await getUser()
	team_id.value = await getTeamId(useSupabaseUser()?.value?.id)
})

async function getUser() {
	return await $fetch('/api/getUser', {
		params: { user_id: user?.value?.id },
	})
}

const first_name = ref('')

const cancelEditProfileRequest = () => {
	first_name.value = ''
}

const checked = ref(useColorMode().preference === 'dark')

type Theme = 'light' | 'dark'

function setColorTheme(theme: Theme) {
	useColorMode().preference = theme
}

const loading = ref(false)
async function updateUserProfile() {
	try {
		loading.value = true
		const user = useSupabaseUser()
		await $fetch('/api/updateUser', {
			method: 'PUT',
			body: {
				id: user?.value?.id,
				full_name: first_name.value,
				team_id: team_id.value.team_id,
			},
		})
	} catch (error) {
		console.error('Error updating user profile:', error)
		toast.add({
			severity: 'error',
			summary: 'Error',
			detail: 'Error updating user profile. Please try again later.',
			life: 3000,
		})
		loading.value = false
	} finally {
		loading.value = false
		toast.add({
			severity: 'success',
			summary: 'Updated',
			detail: 'Your profile has been successfully updated.',
			life: 3000,
		})
		userData.value.full_name = first_name.value
		first_name.value = ''
	}
}

definePageMeta({
	middleware: 'auth',
})
</script>
