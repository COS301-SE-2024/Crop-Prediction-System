import path from 'path'

export default defineNuxtConfig({
	css: ['./assets/css/tailwind.css', 'primeicons/primeicons.css'],
	devtools: { enabled: true },
	modules: ['@nuxt/eslint', '@nuxtjs/tailwindcss', '@nuxtjs/color-mode', 'nuxt-primevue', '@nuxtjs/supabase', '@vueuse/nuxt'],
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
})
