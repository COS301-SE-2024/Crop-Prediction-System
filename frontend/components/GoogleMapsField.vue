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

const emit = defineEmits(['update:selectedField'])

const mapsLoader = useNuxtApp().$mapsLoader
const mapContainer = ref(null)
let map = null
let polygons = ref<google.maps.Polygon[]>([])

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
	await mapsLoader.load()
	initializeMap()

	watch(
		() => props.selectedField,
		(newField) => {
			if (newField) {
				panToField(newField)
			}
		},
	)

	drawPolygons(props.fields)
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
