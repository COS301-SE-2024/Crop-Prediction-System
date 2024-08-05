<template>
	<div class="h-full w-full" ref="mapContainer"></div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted } from 'vue'

const props = defineProps({
	selectedField: {
		type: Object,
		default: null,
	},
	fields: {
		type: Array,
		default: () => [],
	},
})

const mapsLoader = useNuxtApp().$mapsLoader
const mapContainer = ref(null)
let map = null
const polygons = ref({}) // Store polygons in an object keyed by field ID

const polygonOptions = {
	fillColor: '#00FF00', // Green fill color (change as needed)
	fillOpacity: 0.3, // Transparency (0-1)
	strokeColor: '#000000', // Black border (change as needed)
	strokeWeight: 2, // Border thickness
	clickable: true,
	editable: false,
	draggable: false,
}

onMounted(async () => {
	await mapsLoader.load() // Use the loader from the plugin

	initializeMap()

	drawAllFields(props.fields)

	watch(
		() => props.selectedField,
		(newField) => {
			if (newField) {
				panToField(newField)
			}
		},
		{ immediate: false },
	)
})

function initializeMap() {
	const center = { lat: -25.7479, lng: 28.2293 } // Default center
	map = new google.maps.Map(mapContainer.value, {
		center,
		zoom: 19, // Set an initial zoom level that makes sense for your map
		mapTypeId: 'satellite',
	})
}

function drawAllFields(fields) {
	fields.forEach((field) => {
		const polygonCoords = field.field_area.map((coord) => ({
			lat: parseFloat(coord[0]),
			lng: parseFloat(coord[1]),
		}))

		const polygon = new google.maps.Polygon({
			paths: polygonCoords,
			...polygonOptions,
			map: map,
		})

		polygons.value[field.id] = polygon
	})
}

function panToField(field) {
	if (!map || !field) return

	const polygon = polygons.value[field.id]

	if (polygon) {
		const bounds = new google.maps.LatLngBounds()
		polygon
			.getPath()
			.getArray()
			.forEach((coord) => {
				bounds.extend(coord)
			})
		map.fitBounds(bounds)

		// Set a timeout to ensure fitBounds has finished before adjusting the zoom
		setTimeout(() => {
			const currentZoom = map.getZoom()
			if (currentZoom > 19) {
				// Adjust this value as needed
				map.setZoom(19) // Set the desired maximum zoom level
			}
		}, 500) // Delay to allow fitBounds to finish
	}
}

onUnmounted(() => {
	google.maps.event.clearListeners(map, 'overlaycomplete')
})
</script>

<style scoped>
/* Ensure the map height matches the card height */
.h-full {
	height: 100%;
}
</style>
