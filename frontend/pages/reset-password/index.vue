<template>
	<div class="w-full h-screen flex flex-col justify-center items-center p-4 overflow-auto dark:">
		<Card class="p-5">
			<template #title>
				<h1 class="font-medium my-4">Enter New Password</h1>
			</template>
			<template #content>
				<div class="flex flex-col gap-2 items-start">
					<h3 class="font-semibold">Password</h3>
					<div class="card flex justify-center w-full">
						<Password v-model="password" toggleMask class="w-full">
							<template #header>
								<h6 class="font-medium m-0 mb-2 text-base">Pick a password</h6>
							</template>
							<template #footer>
								<Divider />
								<p class="mt-2 p-0 mb-2">Suggestions</p>
								<ul class="p-0 pl-2 m-0 ml-2 list-disc leading-6" style="line-height: 1.5">
									<li :class="{ 'text-primary': passwordChecks.hasLowercase }">At least one lowercase</li>
									<li :class="{ 'text-primary': passwordChecks.hasUppercase }">At least one uppercase</li>
									<li :class="{ 'text-primary': passwordChecks.hasNumber }">At least one numeric</li>
									<li :class="{ 'text-primary': passwordChecks.hasSymbol }">At least one symbol</li>
									<li :class="{ 'text-primary': passwordChecks.hasMinLength }">Minimum 8 characters</li>
								</ul>
							</template>
						</Password>
						<small v-if="validation.password.$dirty && validation.password.$error" class="text-red-500">{{
							validation.password.$message
						}}</small>
					</div>
				</div>
				<div class="flex flex-col gap-2 items-start">
					<h3 class="font-semibold">Confirm Password</h3>
					<div class="card flex flex-col justify-center w-full">
						<Password v-model="confirmPassword" toggleMask class="w-full" :feedback="false">
							<template #header>
								<h6 class="font-medium m-0 mb-2 text-base">Confirm your password</h6>
							</template>
						</Password>
						<small v-if="!passwordsMatch" class="w-full text-red-500">Passwords do not match</small>
					</div>
				</div>
			</template>
			<template #footer>
				<Button
					label="Update Password"
					class="w-full"
					:loading="loading"
					:disabled="password !== confirmPassword"
					@click="updatePassword"
				/>
			</template>
		</Card>
		<Toast />
	</div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { required, email, minLength, sameAs, helpers } from '@vuelidate/validators'
import { useToast } from 'primevue/usetoast'

const client = useSupabaseClient()
const userEmail = ref('')
const password = ref('')
const confirmPassword = ref('')
const errorMsg = ref('')
const successMsg = ref('')
const toast = useToast()
const loading = ref(false)

const passwordPattern = helpers.regex('passwordPattern', /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()_+}{"':;?/>.<,]).{8,}$/)

const rules = {
	userEmail: { required, email },
	password: { required, minLength: minLength(8), passwordPattern },
	confirmPassword: { required, sameAsPassword: sameAs(password) },
}

const passwordChecks = computed(() => {
	const checks = {
		hasLowercase: /[a-z]/.test(password.value),
		hasUppercase: /[A-Z]/.test(password.value),
		hasNumber: /\d/.test(password.value),
		hasSymbol: /[!@#$%^&*()_+}{"':;?/>.<,]/.test(password.value),
		hasMinLength: password.value.length >= 8,
	}
	return checks
})

const validation = useVuelidate(rules, { userEmail, password, confirmPassword })
const passwordsMatch = computed(() => password.value === confirmPassword.value)

const updatePassword = async () => {
	try {
		loading.value = true
		const { data, error } = await client.auth.updateUser({
			password: password.value,
		})

		if (error) throw error
		successMsg.value = 'Your Password has been updated!'
	} catch (error) {
		errorMsg.value = error.message
		loading.value = false
	} finally {
		toast.add({
			severity: 'success',
			summary: 'Password Updated',
			detail: successMsg.value,
			life: 3000,
		})
		loading.value = false
		setTimeout(() => {
			navigateTo('/')
		}, 3000)
	}
}

definePageMeta({
	layout: 'auth',
})
</script>
