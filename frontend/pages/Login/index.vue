<template>
	<div class="min-h-screen flex flex-col justify-center items-center">
		<h1 class="text-3xl font-bold mt-4 mb-2">Welcome to TerraByte!</h1>
		<p class="text-md text-center mb-4">Please login using your<br />personal details below.</p>
		<div class="border border-surface-border bg-white p-6 rounded-2xl shadow-md w-full max-w-md">
			<h2 class="text-2xl font-semibold mb-4">Log in</h2>

			<div class="mb-4">
				<label for="email" class="block text-sm font-medium text-gray-700">Email Address</label>
				<InputText id="email" v-model="email" type="email" placeholder="email@example.com" class="w-full" />
			</div>

			<div class="mb-4">
				<label for="password" class="block text-sm font-medium text-gray-700">Password</label>
				<Password
					id="password"
					v-model="password"
					placeholder="Password"
					feedback
					:toggleMask="true"
					promptLabel="Password"
					weakLabel="Weak Password"
					mediumLabel="Moderate Password"
					strongLabel="Strong Password"
					required
					class="mt-1 block w-full border-gray-300 rounded-md text-gray-900 bg-white"
				/>
				<small v-if="loginError" class="text-red-500 text-sm">Incorrect Email Address or Password</small>
			</div>
			<small v-if="errorMsg" class="text-red-500">{{ errorMsg }}</small>
			<Button label="Login" class="w-full" @submit.prevent="signIn" @click="signIn" />
			<small class="text-center">Dont have an account? <NuxtLink to="/signup" class="underline">Sign up</NuxtLink></small>
		</div>
	</div>
	<img src="~/assets/logo.png" alt="Logo" class="absolute top-2 left-2" />
</template>

<script setup>
import Password from 'primevue/password'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'
import { ref } from 'vue'

const email = ref(null)
const password = ref(null)
const errorMsg = ref(null)

definePageMeta({
	layout: 'auth',
})

const client = useSupabaseClient()
const signIn = async () => {
	try {
		const { error } = await client.auth.signInWithPassword({
			email: email.value,
			password: password.value,
		})
		if (error) throw error
		navigateTo('/')
	} catch (error) {
		errorMsg.value = error.message
	}
}

function isFormInvalid() {
	return !this.email || !this.password
}

// export default {
//   components: {
//     Password,
//     InputText,
//     Button,
//   },
//   data() {
//     return {
//       email: '',
//       password: '',
//       confirmPassword: '',
//       loginError: false,
//     }
//   },
//   computed: {
//     isFormInvalid() {
//       return !this.email || !this.password
//     },
//   },
//   methods: {
//     handleLogin() {
//       if (!this.email) {
//         return // Exit early if email is not provided
//       }
//
//       // Simulate login process
//       if (this.email === 'correct@email.com' && this.password === 'correctpassword') {
//         console.log('Login successful')
//         // Redirect or perform action for successful login
//       } else {
//         this.loginError = true // Set login error to true
//       }
//     },
//   },
// }
</script>

<style scoped>
.input {
	background-color: white;
	color: black;
}
</style>
