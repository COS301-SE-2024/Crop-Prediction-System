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
const userFullName = ref('')
const password = ref('')
const confirmPassword = ref('')
const errorMsg = ref('')
const successMsg = ref('')

const newUserID = ref('')

const team_id = useRoute().query.team_id as string // Get team_id from the query params
const role = useRoute().query.role as string
const step = ref(1) // Step state to manage multi-step

const passwordPattern = helpers.regex('passwordPattern', /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()_+}{"':;?/>.<,]).{8,}$/)

const rules = {
	userEmail: { required, email },
	password: { required, minLength: minLength(8), passwordPattern },
	confirmPassword: { required, sameAsPassword: sameAs(password) },
}

const validation = useVuelidate(rules, { userEmail, password, confirmPassword })

async function signUp() {
	try {
		const { data, error } = await client.auth.signUp({
			email: userEmail.value,
			password: password.value,
			options: {
				data: {
					email: userEmail.value,
					full_name: userFullName.value,
				},
			},
		})
		if (error) throw error
		successMsg.value = 'Check your email to confirm your account.'
		// Move to the next step
		step.value = 2
		newUserID.value = data?.user.id
		console.log('New ID from ref:', newUserID.value)
	} catch (error: any) {
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

async function joinTeam() {
	try {
		// Make a POST request to the server API to add the user to the team
		const response = await $fetch('/api/addToTeam', {
			method: 'POST',
			body: {
				team_id: team_id,
				user_id: newUserID.value,
				role: role,
			},
		})

		if (response?.error) {
			throw new Error(response.error)
		}

		// Handle success response
		successMsg.value = 'You have successfully joined the team!'
	} catch (error: any) {
		// Handle any errors that occurred during the API call
		errorMsg.value = error.message || 'Failed to join the team.'
	} finally {
		step.value = 3
	}
}

definePageMeta({
	layout: 'auth',
})
</script>

<template>
	<div class="w-full h-screen flex flex-col justify-center items-center p-4 overflow-auto">
		<div class="w-full max-w-[450px] px-4 overflow-auto">
			<!-- Step 1: Sign Up -->
			<Card v-if="step === 1" class="w-full border border-surface-border">
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
					<h1 class="font-medium">Join Team</h1>
				</template>
				<template #subtitle>
					<p>Please fill in your details below to create your account. You will confirm your team on the next page.</p>
				</template>
				<template #content>
					<div class="flex flex-col gap-3">
						<div class="flex flex-col gap-2 items-start">
							<h3 class="font-semibold">Full Name</h3>
							<InputText
								id="userFullName"
								type="text"
								class="w-full"
								v-model="userFullName"
								placeholder="John Doe"
							/>
						</div>
						<!-- Email -->
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
						<!-- Password -->
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
						<!-- Confirm Password -->
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
						<!-- Error/Success Message -->
						<small v-if="errorMsg" class="text-red-500">{{ errorMsg }}</small>
						<small v-if="successMsg" class="text-primary">{{ successMsg }}</small>
						<!-- Sign Up Button -->
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
					</div>
				</template>
			</Card>

			<!-- Step 2: Team Confirmation -->
			<Card v-if="step === 2" class="w-full border border-surface-border">
				<template #title>
					<h1 class="font-medium">Team Confirmation</h1>
				</template>
				<template #subtitle>
					<p>Double-check the code sent to your email and ensure it matches the one below.</p>
				</template>
				<template #content>
					<div class="flex flex-col gap-3">
						<!-- Team Code -->
						<div class="flex flex-col gap-2 items-start">
							<h3 class="font-semibold">Team Code</h3>
							<InputText id="teamCode" type="text" class="w-full" v-model="team_id" readonly />
						</div>
					</div>
				</template>
				<template #footer>
					<Button class="w-full" label="Join Team" @click="joinTeam" />
				</template>
			</Card>

			<!-- Step 3: Success -->
			<!-- Step 3: Email Confirmation Prompt -->
			<Card v-if="step === 3" class="w-full border border-surface-border">
				<template #title>
					<h1 class="font-medium">Email Confirmation</h1>
				</template>
				<template #subtitle>
					<p>You have successfully joined the team!</p>
				</template>
				<template #content>
					<p>
						Please check your email to confirm your account and to start using the app. If you haven't received an
						email, please check your spam or junk folder.
					</p>
				</template>
			</Card>
		</div>
	</div>
</template>
