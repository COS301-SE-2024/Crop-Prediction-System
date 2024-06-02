<template>
	<div class="h-full w-full" ref="mapContainer"></div>
</template>

<script setup lang="js">
import { ref, onMounted, onUnmounted } from 'vue'

const emit = defineEmits(['polygonDrawn'])
const props = defineProps({
	isDrawingEnabled: { type: Boolean, default: false },
})

const mapsLoader = useNuxtApp().$mapsLoader
const mapContainer = ref(null)
let map = null
let drawingManager = null
const polygons = ref([])

const polygonOptions = {
	fillColor: '#00FF00', // Green fill color (change as needed)
	fillOpacity: 0.3, // Transparency (0-1)
	strokeColor: '#000000', // Black border (change as needed)
	strokeWeight: 2, // Border thickness
	clickable: true,
	editable: true,
	draggable: true,
}

onMounted(async () => {
	await mapsLoader.load() // Use the loader from the plugin

	await fetchFields()

	if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(
			initializeMap, // Pass the position directly to initializeMap
			handleGeolocationError,
			{ timeout: 10000 }, // Optional: Timeout after 10 seconds
		)
	} else {
		handleGeolocationError() // Geolocation not supported
	}
})

function initializeMap(position) {
	const center = position ? { lat: position.coords.latitude, lng: position.coords.longitude } : { lat: -25.7479, lng: 28.2293 } // Default
	map = new google.maps.Map(mapContainer.value, {
		center, // Set the map's center to the current location
		zoom: 19, // Adjust the default zoom level as needed
		mapTypeId: 'satellite',
	})

	drawingManager = new google.maps.drawing.DrawingManager({
		drawingMode: props.isDrawingEnabled ? google.maps.drawing.OverlayType.POLYGON : null,
		drawingControl: false,
		drawingControlOptions: {
			position: google.maps.ControlPosition.TOP_CENTER,
			drawingModes: [google.maps.drawing.OverlayType.POLYGON],
		},
		polygonOptions: polygonOptions,
	})
	drawingManager.setMap(map)

	google.maps.event.addListener(drawingManager, 'overlaycomplete', (event) => {
		if (event.type === google.maps.drawing.OverlayType.POLYGON) {
			polygons.value.push(event.overlay)
			const paths = event.overlay.getPath().getArray()
			emit('polygonDrawn', paths)
		}
	})

	drawExistingPolygons()
}

function handleGeolocationError(error = null) {
	console.warn('Error getting geolocation:', error ? error.message : 'Not supported')
	initializeMap()
}

function drawExistingPolygons() {
	fieldInfos.value.forEach((field, index) => {
		const polygonCoords = field.field_area.coordinates[0].map((coord) => ({
			lat: parseFloat(coord[0]),
			lng: parseFloat(coord[1]),
		}))
		const polygon = new google.maps.Polygon({
			paths: polygonCoords,
			...polygonOptions,
			map: map,
		})
		polygons.value.push(polygon)
	})
}

onUnmounted(() => {
	google.maps.event.clearListeners(drawingManager, 'overlaycomplete')
})

function clearPolygons() {
	polygons.value.forEach((polygon) => polygon.setMap(null))
	polygons.value = []
}

function setDrawingMode(enabled) {
	if (drawingManager) {
		drawingManager.setDrawingMode(enabled ? google.maps.drawing.OverlayType.POLYGON : null)
	}
}

function getPolygonPaths() {
	return polygons.value.map((polygon) => polygon.getPath().getArray())
}

const fieldInfos = ref([])
const error = ref(null)

async function fetchFields() {
	try {
		const promises = []
		for (let fieldid = 106; fieldid <= 109; fieldid++) {
			promises.push(
				useFetch('/api/fieldInfo', {
					params: { fieldid: fieldid },
				}).then((response) => response.data),
			)
		}

		const results = await Promise.all(promises)

		results.forEach((result) => {
			if (result.error) {
				throw new Error(result.error)
			}
			fieldInfos.value.push(result.value[0])
		})
	} catch (err) {
		error.value = err.message
	}
}

// console.log(`FieldInfos`, fieldInfos.value[0].field_area.coordinates);

defineExpose({
	getPolygonPaths,
	clearPolygons,
	setDrawingMode,
})
</script>
