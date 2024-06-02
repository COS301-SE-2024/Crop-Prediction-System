<script setup lang>
import Card from 'primevue/card'
import InputText from 'primevue/inputtext'
import { ref } from 'vue'
import Password from 'primevue/password'
import { useVuelidate } from '@vuelidate/core'
import { required, email, minLength, sameAs } from '@vuelidate/validators'

const client = useSupabaseClient()
const userEmail = ref('')
const password = ref(null)
const confirmPassword = ref(null)
const errorMsg = ref(null)
const successMsg = ref(null)

const rules = {
  userEmail: { required, email },
  password: { required, minLength: minLength(8) },
  confirmPassword: { required, sameAsPassword: sameAs(password) }
}

const validation = useVuelidate(rules, { userEmail, password, confirmPassword })

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
      email: userEmail.value,
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
					v-model="userEmail"
					placeholder="email@example.com"
					:class="{ 'p-invalid': validation.userEmail.$dirty && validation.userEmail.$error }"
				  />
				  <small v-if="validation.userEmail.$dirty && validation.userEmail.required" class="text-red-500">Email is required.</small>
				  <small v-if="validation.userEmail.$dirty && validation.userEmail.email" class="text-red-500">Invalid email format.</small>
				</div>
				<div class="flex flex-col gap-2 items-start">
				  <h3 class="font-semibold">Password</h3>
				  <div class="card flex justify-center w-full">
					<Password v-model="password" toggleMask class="w-full">
					  <template #header>
						<h6 class="font-medium m-0 mb-2 text-base">Choose a password</h6>
					  </template>
					</Password>
					<small v-if="validation.password.$dirty && validation.password.required" class="text-red-500">Password is required.</small>
					<small v-if="validation.password.$dirty && validation.password.minLength" class="text-red-500">Password must be at least 8 characters.</small>
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
					<small v-if="validation.confirmPassword.$dirty && validation.confirmPassword.sameAsPassword" class="text-red-500">Passwords do not match.</small>
				  </div>
				</div>
				<small v-if="errorMsg" class="text-red-500">{{ errorMsg }}</small>
				<small v-if="successMsg" class="text-primary">{{ successMsg }}</small>
				<Button class="w-full" label="Sign up" :disabled="validation.$anyError" />
				<small class="text-center">Already have an account? <NuxtLink to="/login" class="underline">Login</NuxtLink></small>
			  </form>
			</template>
		  </Card>
		</div>
	  </div>
	</div>
</template>
