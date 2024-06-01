import { Loader } from '@googlemaps/js-api-loader'

export default defineNuxtPlugin((nuxtApp) => {
  const config = useRuntimeConfig();
  const loader = new Loader({
    apiKey: config.public.googleMapsApiKey,
    libraries: ['places', 'drawing'], // Add any needed libraries
  })

  nuxtApp.provide('mapsLoader', loader)
})
