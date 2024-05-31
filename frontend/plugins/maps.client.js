import { Loader } from '@googlemaps/js-api-loader'

export default defineNuxtPlugin((nuxtApp) => {
  const loader = new Loader({
    apiKey: process.env.GOOGLE_MAPS_API_KEY,
    libraries: ['places', 'drawing'], // Add any needed libraries
  })

  nuxtApp.provide('mapsLoader', loader)
})
