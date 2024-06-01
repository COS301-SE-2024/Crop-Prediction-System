import path from 'path';

export default defineNuxtConfig({
  css: ['./assets/css/tailwind.css', 'primeicons/primeicons.css'],
  devtools: { enabled: true },
  modules: ["@nuxt/eslint", "@nuxtjs/tailwindcss", "nuxt-primevue"],
  primevue: {
    options: {
      unstyled: true
    },
    importPT: { from: path.resolve(__dirname, './presets/lara/') }
  },
  components: {
    global: true,
    dirs: ["`/components"],
  },
  plugins: [
    "~/plugins/maps.client.js"
  ],
  runtimeConfig: {
    public: {
      googleMapsApiKey: process.env.GOOGLE_MAPS_API_KEY,
    }
  }
})
