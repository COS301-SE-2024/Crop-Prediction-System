<template>
  <img src="../../assets/logo.png" alt="Logo" class="ml-4 mt-4 mb-4">
  <div class="min-h-screen flex flex-col mb-4 items-center">
    <h1 class="text-3xl font-bold mt-4 mb-2">Welcome to TerraByte!</h1>
    <p class="text-lg text-center mb-4">Please sign up using your<br />personal details below.</p>
    <div class="p-6 rounded-2xl shadow-md w-full max-w-md">
      <h2 class="text-2xl font-semibold mb-4">Sign up</h2>

      <div class="mb-4">
        <label for="email" class="block text-sm font-medium">Email Address</label>
        <InputText
          id="email"
          v-model="email"
          type="email"
          placeholder="email@example.com"
          required
          class="mt-1 block w-full"
        />
        <small v-if="!email" class="text-red-500 text-sm">Please provide an email address</small>
      </div>

      <div class="mb-4">
        <label for="password" class="block text-sm font-medium">Password</label>
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
          class="mt-1 block w-full"
        />
        <small v-if="password && passwordErrors.length" class="text-red-500 text-sm">
          Password must:
          <ul>
            <li v-for="(error, index) in passwordErrors" :key="index">{{ error }}</li>
          </ul>
        </small>
      </div>

      <div class="mb-4">
        <label for="confirmPassword" class="block text-sm font-medium">Confirm Password</label>
        <Password
          id="confirmPassword"
          v-model="confirmPassword"
          placeholder="Password"
          :toggleMask="true"
          promptLabel="Confirm Password"
          required
          class="mt-1 block w-full"
        />
        <small v-if="confirmPassword && confirmPassword !== password" class="text-red-500 text-sm">Passwords do not match.</small>
      </div>

      <Button
        label="Submit"
        @click="handleSignUp"
        :disabled="isFormInvalid"
        class="w-full py-2 mt-4 mb-2"
      />
    </div>
  </div>
</template>

<script>
import Password from 'primevue/password';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';

definePageMeta({
  layout: false,
  head: {
    title: 'TerraByte | Signup'
  }
});

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
    };
  },
  computed: {
    passwordErrors() {
      const errors = [];
      if (!/(?=.*[a-z])/.test(this.password)) {
        errors.push('include at least one lowercase letter');
      }
      if (!/(?=.*[A-Z])/.test(this.password)) {
        errors.push('include at least one uppercase letter');
      }
      if (!/(?=.*[0-9])/.test(this.password)) {
        errors.push('include at least one number');
      }
      if (!/(?=.*[!@#$%^&*])/.test(this.password)) {
        errors.push('include at least one symbol');
      }
      if (this.password.length < 8) {
        errors.push('be at least 8 characters long');
      }
      return errors;
    },
    isPasswordValid() {
      return this.passwordErrors.length === 0;
    },
    isFormInvalid() {
      return !this.email || !this.isPasswordValid || this.password !== this.confirmPassword;
    },
  },
  methods: {
    handleSignUp() {
      if (this.isFormInvalid) {
        return;
      }
      // Handle sign up logic here
      console.log('Email:', this.email);
      console.log('Password:', this.password);
    },
  },
};
</script>

<style scoped>
</style>
