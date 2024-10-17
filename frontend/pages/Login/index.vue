<script setup lang>
import Card from 'primevue/card'
import Password from 'primevue/password'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'
import { ref } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { required, email } from '@vuelidate/validators'

const route = useRoute()
const client = useSupabaseClient()
const user = useSupabaseUser()
const userEmail = ref(route.query.email || '')
const password = ref(route.query.password || '')
const errorMsg = ref(null)

const rules = {
	email: { required, email },
	password: { required },
}

const validation = useVuelidate(rules, { email: userEmail, password })

const redirectTo = route.query.redirectTo || '/'

const signIn = async () => {
	try {
		validation.value.$touch()
		if (validation.value.$error) return

		const { error } = await client.auth.signInWithPassword({
			email: userEmail.value,
			password: password.value,
		})
		if (error) throw error
		navigateTo(`/confirm?redirectTo=${redirectTo}`)
	} catch (error) {
		errorMsg.value = error.message
	}
}

const config = useRuntimeConfig()

const signInWithOauth = async () => {
	try {
		const { error } = await client.auth.signInWithOAuth({
			provider: 'google',
			options: {
				redirectTo: `${config.public.appBaseUrl}/confirm?redirectTo=${redirectTo}`,
			},
		})
		if (error) throw error
	} catch (error) {
		errorMsg.value = error.message
	}
}

if (userEmail.value !== '' && password.value !== '') {
	rules.email = { email }
	rules.password = {}

	signIn()
}

definePageMeta({
	layout: 'auth',
})
</script>

<template>
	<div class="w-full h-screen flex flex-col justify-center items-center p-4 overflow-auto dark:">
		<div class="w-full max-w-[450px] px-4 overflow-auto">
			<!-- <div class="flex flex-col gap-5 items-center w-[400px] max-w-md"> -->
			<Card class="w-full bg-surface-100 dark:bg-surface-800 p-[20px]">
				<template #header>
					<div class="flex justify-center items-center p-4">
						<img src="../../assets/logo-alt.png" alt="Logo" class="w-[auto] h-[70px] self-center" />
					</div>
				</template>
				<template #title>
					<h1 class="font-medium my-4">Log in</h1>
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
								:class="{ 'p-invalid': validation.email.$dirty && validation.email.$error }"
							/>
							<small v-if="validation.email.$dirty && validation.email.$error" class="text-red-500">{{
								validation.email.$message
							}}</small>
						</div>
						<div class="flex flex-col gap-2 items-start">
							<h3 class="font-semibold">Password</h3>
							<div class="flex justify-center w-full">
								<Password v-model="password" toggleMask class="w-full" @keydown.enter="signIn" :feedback="false">
									<template #header>
										<h6 class="font-medium m-0 mb-2 text-base">Enter your password</h6>
									</template>
								</Password>
								<small v-if="validation.password.$dirty && validation.password.$error" class="text-red-500">{{
									validation.password.$message
								}}</small>
							</div>
							<small class="text-center w-full"
								>Forgot your password?
								<NuxtLink to="/reset" class="underline">Reset Password</NuxtLink>
							</small>
						</div>
						<small v-if="errorMsg" class="text-red-500">{{ errorMsg }}</small>
						<Button class="w-full" label="Login" @click="signIn" />
						<Divider align="center">
							<b class="bg-none">or</b>
						</Divider>
						<Button icon="pi pi-google" class="w-full" @click="signInWithOauth" />
						<small class="text-center"
							>Don't have an account?
							<NuxtLink to="/signup" class="underline">Sign up</NuxtLink>
						</small>
					</div>
				</template>
			</Card>
		</div>
	</div>
	<!-- </div> -->
</template>
