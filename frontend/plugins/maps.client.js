import { Loader } from '@googlemaps/js-api-loader'

export default defineNuxtPlugin((nuxtApp) => {
	const loader = new Loader({
		apiKey: 'AIzaSyAM5zZT_BdKRMrQBSxfIO7XeygeSFAmJOo',
		libraries: ['places', 'drawing'], // Add any needed libraries
	})

	nuxtApp.provide('mapsLoader', loader)
})
