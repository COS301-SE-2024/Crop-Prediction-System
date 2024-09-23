<template>
	<div class="w-full flex h-full flex-col justify-between gap-4 items-center">
		<InputText v-model="searchQuery" id="search-input" class="w-full" placeholder="Search for a place" />
		<label for="googlemap" class="self-start">
			Please click on the outer bounds of the field to draw a polygon. Make sure to connect the last polygon point to the
			first one to complete the shape of the field. If the map is too small, click on the
			<i class="pi pi-expand" style="font-size: 1.5rem; margin-left: 5px; margin-right: 5px"></i> icon to enlarge the map.
		</label>
		<div class="h-[400px] w-full md:h-[600px] rounded-md" id="googlemap" ref="mapContainer"></div>
	</div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, defineExpose } from 'vue'

const emit = defineEmits(['polygonDrawn', 'polygonUpdated'])
const props = defineProps({
	isDrawingEnabled: { type: Boolean, default: false },
})

const mapsLoader = useNuxtApp().$mapsLoader
const mapContainer = ref(null)
let map = null
let drawingManager = null
let polygon = null
const polygons = ref([]) // This holds polygons of existing fields
const userFields = ref([]) // This holds the user fields fetched from API

const searchQuery = ref('')

const polygonOptions = {
	fillColor: '#ba55f4',
	fillOpacity: 0.5,
	strokeColor: '#ba55f4',
	strokeWeight: 2,
	clickable: true,
	editable: false, // Ensure existing polygons are non-editable
	draggable: false, // Ensure existing polygons are non-draggable
}

onMounted(async () => {
	await mapsLoader.load()

	if (mapContainer.value) {
		if (navigator.geolocation) {
			navigator.geolocation.getCurrentPosition(initializeMap, handleGeolocationError, { timeout: 10000 })
		} else {
			handleGeolocationError()
		}

		// Fetch user fields and draw existing polygons
		await fetchUserFields()
		drawExistingPolygons()
	}
})

async function fetchUserFields() {
	const session = useSupabaseClient()
	let currentUser = null
	if (session) {
		const {
			data: { user },
		} = await session.auth.getUser()
		if (user) currentUser = user
	}

	if (currentUser) {
		try {
			const teamID = await $fetch('/api/getTeamID', {
				params: { userid: currentUser?.id },
			})
			const fields = await $fetch('/api/getTeamFields', {
				params: { team_id: teamID.team_id },
			})
			userFields.value = fields // Store the fields for rendering polygons
		} catch (error) {
			console.error('Error fetching user fields:', error)
		}
	}
}

function initializeMap(position) {
	if (!mapContainer.value) return // Ensure the map container is available

	const center = position ? { lat: position.coords.latitude, lng: position.coords.longitude } : { lat: -25.7479, lng: 28.2293 } // Default center if geolocation fails

	map = new google.maps.Map(mapContainer.value, {
		center,
		zoom: 18,
		mapTypeId: 'satellite',
	})

	drawingManager = new google.maps.drawing.DrawingManager({
		drawingMode: google.maps.drawing.OverlayType.POLYGON, // Start directly in drawing mode
		drawingControl: false, // Hide drawing control (since we're forcing polygon mode)
		polygonOptions: {
			...polygonOptions,
			editable: true, // Allow editing for new polygons
			draggable: true, // Allow dragging for new polygons
		},
	})
	drawingManager.setMap(map)

	// Listen for polygon drawing completion
	google.maps.event.addListener(drawingManager, 'overlaycomplete', (event) => {
		if (event.type === google.maps.drawing.OverlayType.POLYGON) {
			// Clear any existing user-drawn polygon before drawing a new one
			if (polygon) polygon.setMap(null)

			polygon = event.overlay

			const paths = polygon
				.getPath()
				.getArray()
				.map((point) => [point.lat(), point.lng()])

			emit('polygonDrawn', paths)

			// Listen for polygon edits
			enablePolygonEditing(polygon)

			// Disable further drawing after one polygon
			drawingManager.setDrawingMode(null)
		}
	})

	initializeAutocomplete()
}

function initializeAutocomplete() {
	const input = document.getElementById('search-input')
	const autocomplete = new google.maps.places.Autocomplete(input)
	autocomplete.bindTo('bounds', map)

	autocomplete.addListener('place_changed', () => {
		const place = autocomplete.getPlace()

		if (!place.geometry || !place.geometry.location) {
			console.error('Place contains no geometry')
			return
		}

		if (place.geometry.viewport) {
			map.fitBounds(place.geometry.viewport)
		} else {
			map.setCenter(place.geometry.location)
			map.setZoom(17)
		}
	})
}

function handleGeolocationError(error = null) {
	console.warn('Error getting geolocation:', error ? error.message : 'Not supported')
	initializeMap()
}

// Function to draw polygons for existing fields
function drawExistingPolygons() {
	userFields.value.forEach((field) => {
		const polygonCoords = field.field_area.map((coord) => ({
			lat: parseFloat(coord[0]),
			lng: parseFloat(coord[1]),
		}))
		const existingPolygon = new google.maps.Polygon({
			paths: polygonCoords,
			...polygonOptions,
			map: map, // Add to map
		})
		polygons.value.push(existingPolygon)
	})
}

// Function to enable polygon editing and handle updates
function enablePolygonEditing(polygon) {
	polygon.setEditable(true)
	const path = polygon.getPath()
	google.maps.event.addListener(path, 'set_at', () => updatePolygonCoords(polygon))
	google.maps.event.addListener(path, 'insert_at', () => updatePolygonCoords(polygon))
}

function updatePolygonCoords(polygon) {
	const updatedPaths = polygon
		.getPath()
		.getArray()
		.map((point) => [point.lat(), point.lng()])
	emit('polygonUpdated', updatedPaths)
}

// INFO: Function to clear polygons
function finalizePolygon() {
	if (polygon) {
		// Make the polygon non-editable and non-draggable
		polygon.setEditable(false)
		polygon.setDraggable(false)

		// Add the finalized polygon to the list of existing polygons
		polygons.value.push(polygon)

		// Reset the polygon variable
		polygon = null

		// Re-enable drawing mode for new polygons
		if (drawingManager) {
			drawingManager.setDrawingMode(google.maps.drawing.OverlayType.POLYGON)
		}
	}
}

defineExpose({
	finalizePolygon,
})

// Cleanup listeners and map when the component is unmounted
onBeforeUnmount(() => {
	if (drawingManager) {
		google.maps.event.clearListeners(drawingManager, 'overlaycomplete')
	}
	if (polygon) {
		google.maps.event.clearListeners(polygon.getPath(), 'set_at')
		google.maps.event.clearListeners(polygon.getPath(), 'insert_at')
	}
	if (map) {
		map = null
	}
})
</script>
