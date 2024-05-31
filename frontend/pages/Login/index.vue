<template>
  <div class="min-h-screen flex flex-col justify-center items-center bg-gray-100">
    <h1 class="text-3xl font-bold mt-4 mb-2">Welcome to TerraByte!</h1>
    <p class="text-lg text-center mb-4">Please login using your<br/>personal details below.</p>
    <div class="bg-white p-6 rounded-2xl shadow-md w-full max-w-md">
      <h2 class="text-2xl font-semibold mb-4">Log in</h2>

      <div class="mb-4">
        <label for="email" class="block text-sm font-medium text-gray-700">Email Address</label>
        <InputText 
          id="email" 
          v-model="email" 
          type="email" 
          placeholder="email@example.com"
          required
          class="input mt-1 block w-full border-gray-300 rounded-xl text-gray-900 bg-white"
        />
        <small v-if="!email" class="text-red-500 text-sm">Please provide an email address</small>
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
          :inputStyle="{backgroundColor: 'white', color: 'black', borderRadius: '0.75rem'}"
          class="mt-1 block w-full border-gray-300 rounded-md text-gray-900 bg-white"
        />
        <small v-if="loginError" class="text-red-500 text-sm">Incorrect Email Address or Password</small>
      </div>

      <Button 
        label="Login" 
        @click="handleLogin" 
        :disabled="isFormInvalid" 
        class="w-full bg-primary text-white py-2 rounded-xl mt-4 mb-2"
      />
    </div>
  </div>
</template>

<script>
import Password from 'primevue/password';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';

export default {
  components: {
    Password,
    InputText,
    Button,
  },
  data() {
    return {
      email: '',
      password: '',
      confirmPassword: '',
      loginError: false,
    };
  },
  computed: {
    isFormInvalid() {
      return !this.email || !this.password;
    },
  },
  methods: {
    handleLogin() {
      if (!this.email) {
        return; // Exit early if email is not provided
      }

      // Simulate login process
      if (this.email === 'correct@email.com' && this.password === 'correctpassword') {
        console.log('Login successful');
        // Redirect or perform action for successful login
      } else {
        this.loginError = true; // Set login error to true
      }
    },
  },
};
</script>

<style scoped>
  .input {
    background-color: white;
    color: black;
  }
</style>
