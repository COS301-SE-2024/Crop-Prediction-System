<script setup lang="ts">
import Card from 'primevue/card'
import InputText from 'primevue/inputtext'
import Password from 'primevue/password'
import Divider from 'primevue/divider'
import Button from 'primevue/button'
import { ref, computed } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { required, email, minLength, sameAs, helpers } from '@vuelidate/validators'

const client = useSupabaseClient()
const userEmail = ref('')
const password = ref('')
const confirmPassword = ref('')
const errorMsg = ref('')
const successMsg = ref('')

const passwordPattern = helpers.regex('passwordPattern', /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()_+}{"':;?/>.<,]).{8,}$/)

const rules = {
	userEmail: { required, email },
	password: { required, minLength: minLength(8), passwordPattern },
	confirmPassword: { required, sameAsPassword: sameAs(password) },
}

const validation = useVuelidate(rules, { userEmail, password, confirmPassword })

async function signUp() {
	try {
		const { error } = await client.auth.signUp({
			email: userEmail.value,
			password: password.value,
		})
		if (error) throw error
		successMsg.value = 'Check your email to confirm your account.'
	} catch (error) {
		errorMsg.value = error.message
	}
}

const signInWithOauth = async () => {
	try {
		const { error } = await client.auth.signInWithOAuth({
			provider: 'google',
			options: {
				redirectTo: `https://terrabyte.software/confirm/`,
			},
		})
		if (error) throw error
	} catch (error) {
		errorMsg.value = error.message
	}
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

const passwordsMatch = computed(() => password.value === confirmPassword.value)

definePageMeta({
	layout: 'auth',
})
</script>

<template>
	<div class="w-full h-screen flex flex-col justify-center items-center p-4 overflow-auto">
		<div class="w-full max-w-[450px] px-4 overflow-auto">
			<!-- <div class="flex flex-col gap-5 items-center w-[400px] max-w-lg"> -->
			<Card class="w-full border border-surface-border">
				<template #header>
					<div class="flex justify-center items-center p-4">
						<img
							src="../../assets/logo-alt.png"
							alt="Logo"
							class="hidden dark:block pt-1 w-[auto] h-[70px] self-center"
						/>
						<img
							src="../../assets/logo.png"
							alt="Logo"
							class="dark:hidden block pt-1 w-[auto] h-[70px] self-center"
						/>
					</div>
				</template>
				<template #title>
					<h1 class="font-medium">Sign up</h1>
				</template>
				<template #content>
					<div class="flex flex-col gap-3">
						<div class="flex flex-col gap-2 items-start">
							<h3 class="font-semibold">Email Address</h3>
							<InputText
								id="email"
								type="email"
								class="w-full"
								v-model="userEmail"
								placeholder="email@example.com"
								:class="{ 'p-invalid': validation.userEmail.$dirty && validation.userEmail.$error }"
							/>
							<small v-if="validation.userEmail.$dirty && validation.userEmail.$error" class="text-red-500">{{
								validation.userEmail.$message
							}}</small>
						</div>
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
											<li :class="{ 'text-primary': passwordChecks.hasLowercase }">
												At least one lowercase
											</li>
											<li :class="{ 'text-primary': passwordChecks.hasUppercase }">
												At least one uppercase
											</li>
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
						<small v-if="errorMsg" class="text-red-500">{{ errorMsg }}</small>
						<small v-if="successMsg" class="text-primary">{{ successMsg }}</small>
						<Button
							class="w-full"
							label="Sign up"
							@click="signUp"
							:disabled="
								validation.$anyError ||
								userEmail === '' ||
								!password ||
								!confirmPassword ||
								password !== confirmPassword
							"
						/>
						<Divider align="center">
							<b class="bg-none">or</b>
						</Divider>
						<Button icon="pi pi-google" class="w-full" @click="signInWithOauth" />
						<small class="text-center"
							>Already have an account? <NuxtLink to="/login" class="underline">Login</NuxtLink>
						</small>
					</div>
				</template>
			</Card>
		</div>
	</div>
	<!-- </div> -->
</template>
