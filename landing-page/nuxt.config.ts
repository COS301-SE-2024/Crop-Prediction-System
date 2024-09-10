import { defineNuxtConfig } from 'nuxt/config'
import aura from '@primevue/themes/lara'

export default defineNuxtConfig({
	css: ['./assets/css/tailwind.css', 'primeicons/primeicons.css'],
	modules: ['@primevue/nuxt-module', '@nuxt/eslint', '@nuxtjs/tailwindcss', '@nuxtjs/color-mode', '@vueuse/nuxt'],
	colorMode: {
		classSuffix: '',
	},
	compatibilityDate: '2024-04-03',
	primevue: {
		theme: aura,
	},
})
