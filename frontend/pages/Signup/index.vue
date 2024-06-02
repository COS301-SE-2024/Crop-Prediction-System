<script setup lang>
import Card from 'primevue/card'
import InputText from 'primevue/inputtext'
import { ref } from 'vue'
import Password from 'primevue/password'
import { useVuelidate } from '@vuelidate/core'
import { required, email, minLength, helpers } from '@vuelidate/validators'

const client = useSupabaseClient()
// const email = ref(null)
const password = ref(null)
const confirmPassword = ref(null)
const errorMsg = ref(null)
const successMsg = ref(null)

const passwordPattern = helpers.regex('passwordPattern', /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()_+}{"':;?/>.<,]).{8,}$/)

const rules = {
  email: { required, email },
  password: { required, minLength: minLength(8) },
  confirmPassword: { required }
}

const validation = useVuelidate(rules, { email, password, confirmPassword })

async function signUp() {
  try {
    validation.value.$touch()
    if (validation.value.$error) {
		return
	}

    if (password.value !== confirmPassword.value) {
      errorMsg.value = 'Passwords do not match'
      return
    }

    const { error } = await client.auth.signUp({
      email: email.value,
      password: password.value,
    })
    if (error) throw error
    successMsg.value = 'Check your email to confirm your account.'
  } catch (error) {
    errorMsg.value = error.message
  }
}

definePageMeta({
	layout: 'auth',
})
</script>

<template>
	<div class="w-full h-screen flex flex-col justify-center items-center p-4">
		<img src="~/assets/logo.png" alt="Logo" class="absolute top-2 left-2" />
		<div class="self-center">
			<div class="flex flex-col gap-5 items-center w-[400px] max-w-lg">
				<Card class="w-full border border-surface-border">
					<template #title>
						<h1>Sign up</h1>
					</template>
					<template #content>
						<form @submit.prevent="signUp" class="flex flex-col gap-3">
							<div class="flex flex-col gap-2 items-start">
								<h3 class="font-semibold">Email Address</h3>
								<InputText
									id="email"
									type="email"
									class="w-full"
									v-model="email"
									placeholder="email@example.com"
									:class="{ 'p-invalid': validation.email.$dirty && validation.email.$error }"
								/>
								<small v-if="validation.email.$dirty && validation.email.$error" class="text-red-500">{{ validation.email.$message }}</small>
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
												<li>At least one lowercase</li>
												<li>At least one uppercase</li>
												<li>At least one numeric</li>
												<li>Minimum 8 characters</li>
											</ul>
										</template>
									</Password>
									<small v-if="validation.password.$dirty && validation.password.$error" class="text-red-500">{{ validation.password.$message }}</small>
								</div>
							</div>
							<div class="flex flex-col gap-2 items-start">
								<h3 class="font-semibold">Confirm Password</h3>
								<div class="card flex justify-center w-full">
									<Password v-model="confirmPassword" toggleMask class="w-full">
										<template #header>
											<h6 class="font-medium m-0 mb-2 text-base">Confirm your password</h6>
										</template>
									</Password>
									<small v-if="validation.confirmPassword.$dirty && validation.confirmPassword.$error" class="text-red-500">{{ validation.confirmPassword.$message }}</small>
								</div>
							</div>
							<small v-if="errorMsg" class="text-red-500">{{ errorMsg }}</small>
							<small v-if="successMsg" class="text-primary">{{ successMsg }}</small>
							<Button class="w-full" label="Sing up" @click="signUp" />
							<small class="text-center"
								>Already have an account? <NuxtLink to="/login" class="underline">Login </NuxtLink></small
							>
						</form>
					</template>
				</Card>
			</div>
		</div>
	</div>
</template>
