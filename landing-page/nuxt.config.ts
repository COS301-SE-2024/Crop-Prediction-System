import { defineNuxtConfig } from 'nuxt/config'
import Lara from '@primevue/themes/lara'

export default defineNuxtConfig({
	css: ['./assets/css/tailwind.css', 'primeicons/primeicons.css'],
	modules: [
		'@primevue/nuxt-module',
		'@nuxt/eslint',
		'@nuxtjs/tailwindcss',
		'@nuxtjs/color-mode',
		'@vueuse/nuxt',
		'@nuxt/fonts',
	],
	colorMode: {
		classSuffix: '',
	},
	compatibilityDate: '2024-04-03',
	primevue: {
		options: {
			theme: {
				preset: Lara,
			},
		},
	},
})
