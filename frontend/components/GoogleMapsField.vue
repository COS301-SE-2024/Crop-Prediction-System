<template>
	<div v-show="!loading" class="w-full h-full rounded-md bg-surface-100 dark:bg-surface-800">
		<div class="h-full w-full" ref="mapContainer"></div>
	</div>
	<div
		v-show="loading"
		class="w-full h-full rounded-md bg-surface-100 dark:bg-surface-800 flex flex-col justify-center items-center gap-4"
	>
		<h2 class="text-2xl font-bold text-surface-700 dark:text-surface-0">Loading Map...</h2>
		<div
			class="w-16 h-16 border-4 border-t-4 rounded-full border-gray-300 dark:border-gray-600 border-t-gray-700 dark:border-t-white animate-spin"
		></div>
	</div>
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
	isEditMode: {
		type: Boolean,
		default: false,
	},
})

watch(
	() => props.isEditMode,
	(newEditMode) => {
		if (props.selectedField) {
			togglePolygonEditability(props.selectedField, newEditMode)
		}
	},
)

function togglePolygonEditability(field, isEditable) {
	polygons.value.forEach((polygon, index) => {
		const isSelected = field.id === props.fields[index].id
		if (isSelected) {
			polygon.setOptions({ editable: isEditable, draggable: isEditable })

			if (isEditable) {
				google.maps.event.addListener(polygon.getPath(), 'set_at', () => {
					// Keep track of changes, but don't emit yet
					logNewPolygonCoords(polygon)
				})
				google.maps.event.addListener(polygon.getPath(), 'insert_at', () => {
					logNewPolygonCoords(polygon)
				})
			} else {
				// When edit mode ends (Save Changes clicked), emit the new coordinates
				const updatedCoords = polygon
					.getPath()
					.getArray()
					.map((coord) => ({
						lat: coord.lat(),
						lng: coord.lng(),
					}))
				emit('savePolygonCoords', updatedCoords)
			}
		}
	})
}

function logNewPolygonCoords(polygon) {
	// You can track real-time changes here if needed, but only emit on save
}

const emit = defineEmits(['update:selectedField', 'savePolygonCoords'])

const mapsLoader = useNuxtApp().$mapsLoader
const mapContainer = ref(null)
let map = null
let polygons = ref<google.maps.Polygon[]>([])
const loading = ref(true)

const defaultPolygonOptions = {
	fillColor: '#ba55f4', // Green fill color for unselected fields
	fillOpacity: 0.5, // Transparency
	strokeColor: '#ba55f4', // Black border
	strokeWeight: 2, // Border thickness
	clickable: true,
	editable: false,
	draggable: false,
}

const selectedPolygonOptions = {
	fillColor: '#b3df91', // Red fill color for the selected field
	fillOpacity: 0.7, // Higher transparency for the selected field
	strokeColor: '#ba55f4', // Black border
	strokeWeight: 2,
	clickable: true,
	editable: false,
	draggable: false,
}

onMounted(async () => {
	loading.value = true
	try {
		await mapsLoader.load()
		initializeMap()
		drawPolygons(props.fields)
	} finally {
		loading.value = false
		if (props.selectedField !== null) {
			panToField(props.selectedField)
		}
	}

	watch(
		() => props.selectedField,
		(newField) => {
			if (newField) {
				panToField(newField)
			}
		},
	)
})

function initializeMap() {
	const center = { lat: -25.7479, lng: 28.2293 } // Default center
	map = new google.maps.Map(mapContainer.value, {
		center,
		zoom: 15, // Set an initial zoom level
		mapTypeId: 'satellite',
	})
}

function panToField(field) {
	if (!map) return

	const polygonCoords = field.field_area.map((coord) => ({
		lat: parseFloat(coord[0]),
		lng: parseFloat(coord[1]),
	}))

	const bounds = new google.maps.LatLngBounds()
	polygonCoords.forEach((coord) => {
		bounds.extend(coord)
	})

	// Pan to the selected field
	map.fitBounds(bounds)

	// Adjust zoom level after panning
	setTimeout(() => {
		const currentZoom = map.getZoom()
		if (currentZoom > 19) {
			map.setZoom(19) // Adjust this value as needed
		}
	}, 500)

	// After panning, highlight the selected field
	highlightSelectedField(field)
}

function drawPolygons(fields) {
	clearPolygons()

	fields.forEach((field) => {
		const polygonCoords = field.field_area.map((coord) => ({
			lat: parseFloat(coord[0]),
			lng: parseFloat(coord[1]),
		}))

		const polygonOptions = field.id === props.selectedField?.id ? selectedPolygonOptions : defaultPolygonOptions

		const polygon = new google.maps.Polygon({
			paths: polygonCoords,
			...polygonOptions,
			map: map,
		})

		polygon.addListener('click', () => {
			emit('update:selectedField', field)
		})

		polygons.value.push(polygon)
	})
}

function highlightSelectedField(selectedField) {
	polygons.value.forEach((polygon, index) => {
		const field = props.fields[index]
		const isSelected = field.id === selectedField.id

		polygon.setOptions(isSelected ? selectedPolygonOptions : defaultPolygonOptions)
	})
}

function clearPolygons() {
	polygons.value.forEach((polygon) => polygon.setMap(null))
	polygons.value = []
}

onUnmounted(() => {
	google.maps.event.clearListeners(map, 'overlaycomplete')
})
</script>

<style scoped>
.custom-spinner {
	width: 60px; /* Larger size */
	height: 60px; /* Larger size */
	border: 6px solid rgba(0, 0, 0, 0.1);
	border-top-color: rgba(0, 0, 0, 0.8);
	border-radius: 50%;
	animation: spin 1s linear infinite;
}

/* Dark mode variant */
@media (prefers-color-scheme: dark) {
	.custom-spinner {
		border: 6px solid rgba(255, 255, 255, 0.1); /* Light gray for dark mode */
		border-top-color: rgba(255, 255, 255, 0.8); /* White for dark mode */
	}
}

@keyframes spin {
	0% {
		transform: rotate(0deg);
	}
	100% {
		transform: rotate(360deg);
	}
}
</style>
