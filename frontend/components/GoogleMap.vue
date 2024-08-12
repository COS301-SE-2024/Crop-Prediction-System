<template>
	<div class="md:h-screen h-[45rem] w-full _sm:h-[200px] _md:h-[850px]" ref="mapContainer"></div>
</template>

<script setup lang="ts">
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
	fillColor: '#ba55f4', // Green fill color (change as needed)
	fillOpacity: 0.5, // Transparency (0-1)
	strokeColor: '#ba55f4', // Black border (change as needed)
	strokeWeight: 2, // Border thickness
	clickable: true,
	editable: true,
	draggable: true,
}

const userFields = ref([])

onMounted(async () => {
	await mapsLoader.load() // Use the loader from the plugin

	if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(
			initializeMap, // Pass the position directly to initializeMap
			handleGeolocationError,
			{ timeout: 10000 }, // Optional: Timeout after 10 seconds
		)
	} else {
		handleGeolocationError() // Geolocation not supported
	}

	await fetchUserFields()
})

async function fetchUserFields() {
	const session = useSupabaseClient()
	let currentUser = null
	if (session) {
		const {
			data: { user },
		} = await session.auth.getUser()
		if (user) currentUser = user
		console.error('user: ', user?.id)
	}

	if (currentUser) {
		try {
			const teamID = await $fetch('/api/getTeamID', {
				params: { userid: currentUser?.id },
			})
			const fields = await $fetch('/api/getTeamFields', {
				params: { team_id: teamID.team_id },
			})
			userFields.value = fields
			drawExistingPolygons()
		} catch (error) {
			console.error('Error fetching user fields:', error)
		}
	}
}

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
	userFields.value.forEach((field) => {
		const polygonCoords = field.field_area.map((coord) => ({
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

defineExpose({
	getPolygonPaths,
	clearPolygons,
	setDrawingMode,
})
</script>
