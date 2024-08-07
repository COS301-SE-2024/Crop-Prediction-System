import path from 'path';

export default defineNuxtConfig({
	css: ['./assets/css/tailwind.css', 'primeicons/primeicons.css'],
	devtools: { enabled: true },
	modules: [
		'@nuxt/eslint',
		'@nuxtjs/tailwindcss',
		'@nuxtjs/color-mode',
		'nuxt-primevue',
		'@nuxtjs/supabase',
		'@nuxt/test-utils/module',
		'@vueuse/nuxt',
	],
	colorMode: {
		classSuffix: '',
	},
	primevue: {
		options: {
			unstyled: true,
		},
		importPT: { from: path.resolve(__dirname, './presets/lara/') },
	},
	components: {
		global: true,
		dirs: ['`/components'],
	},
	plugins: ['~/plugins/maps.client.js'],
	runtimeConfig: {
		public: {
			googleMapsApiKey: process.env.GOOGLE_MAPS_API_KEY,
			apiBaseUrl: process.env.API_BASE_URL,
			openweatherApiUrl: 'https://api.openweathermap.org/data/2.5/',
			openweatherApiKey: process.env.OPENWEATHER_API_KEY,
		},
	},
	supabase: {
		redirect: true,
		redirectOptions: {
			login: '/login',
			callback: '/confirm',
			exclude: ['/signup'],
		},
	},
})
