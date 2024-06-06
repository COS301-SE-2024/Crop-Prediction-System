<script setup lang>
import Card from 'primevue/card'
import Password from 'primevue/password'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'
import { ref } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { required, email } from '@vuelidate/validators'

const client = useSupabaseClient()
const userEmail = ref('')
const password = ref(null)
const errorMsg = ref(null)

const rules = {
	email: { required, email },
	password: { required },
}

const validation = useVuelidate(rules, { email: userEmail, password })

const signIn = async () => {
	try {
		validation.value.$touch()
		if (validation.value.$error) return

		const { error } = await client.auth.signInWithPassword({
			email: userEmail.value,
			password: password.value,
		})
		if (error) throw error
		navigateTo('/')
	} catch (error) {
		errorMsg.value = error.message
	}
}

definePageMeta({
	layout: 'auth',
})
</script>

<template>
	<div class="w-full h-screen flex flex-col justify-center items-center p-4 dark:bg-surface-900 bg-surface-500">
		<div class="self-center">
			<div
				class="flex flex-col gap-5 items-center w-[400px] max-w-md bg-opacity-50 dark:bg-opacity-50 _bg-gray-100 _dark:bg-gray-600 backdrop-blur-md _border border-surface-500 text-center dark:text-white text-black p-8 rounded-xl"
			>
				<div class="w-full grid gap-4">
					<div class="">
						<div class="flex flex-col gap-3 items-center">
							<img src="~/assets/logo_only.png" alt="Logo" class="w-20" />
							<h1 class="text-2xl">Log in to TerraByte</h1>
						</div>
					</div>
					<div>
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
								<div class="card flex justify-center w-full">
									<Password v-model="password" toggleMask class="w-full" :feedback="false">
										<template #header>
											<h6 class="font-medium m-0 mb-2 text-base">Enter your password</h6>
										</template>
									</Password>
									<small v-if="validation.password.$dirty && validation.password.$error" class="text-red-500">{{
										validation.password.$message
									}}</small>
								</div>
							</div>
							<small v-if="errorMsg" class="text-red-500">{{ errorMsg }}</small>
							<Button class="w-full" label="Login" @click="signIn" />
							<small class="text-center"
								>Don't have an account? <NuxtLink to="/signup" class="underline">Sign up </NuxtLink></small
							>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>
