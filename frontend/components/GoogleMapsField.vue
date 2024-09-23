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

const emit = defineEmits(['update:selectedField', 'savePolygonCoords'])

const mapsLoader = useNuxtApp().$mapsLoader
const mapContainer = ref(null)
let map = null
let polygons = ref([])
const loading = ref(true)

const defaultPolygonOptions = {
	fillColor: '#ba55f4',
	fillOpacity: 0.5,
	strokeColor: '#ba55f4',
	strokeWeight: 2,
	clickable: true,
	editable: false,
	draggable: false,
}

const selectedPolygonOptions = {
	fillColor: '#b3df91',
	fillOpacity: 0.7,
	strokeColor: '#ba55f4',
	strokeWeight: 2,
	clickable: true,
	editable: false,
	draggable: false,
}

watch(
	() => props.isEditMode,
	(newEditMode) => {
		if (props.selectedField) {
			togglePolygonEditability(props.selectedField, newEditMode)
		}
	},
)

watch(
	() => props.fields,
	(newFields) => {
		if (newFields && newFields.length > 0 && map) {
			drawPolygons(newFields)
		}
	},
	{ deep: true },
)

watch(
	() => props.selectedField,
	(newField) => {
		if (newField && map) {
			highlightSelectedField(newField)
			panToField(newField)
		}
	},
	{ deep: true },
)

function togglePolygonEditability(field, isEditable) {
	polygons.value.forEach((polygon, index) => {
		const isSelected = field.id === props.fields[index].id
		if (isSelected) {
			polygon.setOptions({ editable: isEditable, draggable: isEditable })

			if (isEditable) {
				google.maps.event.addListener(polygon.getPath(), 'set_at', () => {
					logNewPolygonCoords(polygon)
				})
				google.maps.event.addListener(polygon.getPath(), 'insert_at', () => {
					logNewPolygonCoords(polygon)
				})
			} else {
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

function logNewPolygonCoords(polygon) {}

function initializeMap() {
	const center = { lat: -25.7479, lng: 28.2293 }
	map = new google.maps.Map(mapContainer.value, {
		center,
		zoom: 15,
		mapTypeId: 'satellite',
	})
}

function drawPolygons(fields) {
	clearPolygons()

	fields.forEach((field) => {
		const polygonCoords = field.field_area.map((coord) => ({
			lat: coord[0],
			lng: coord[1],
		}))

		if (polygonCoords.length < 3) {
			console.error('Not enough valid coordinates to form a polygon for field:', field.id)
			return
		}

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

function clearPolygons() {
	polygons.value.forEach((polygon) => polygon.setMap(null))
	polygons.value = []
}

function highlightSelectedField(selectedField) {
	polygons.value.forEach((polygon, index) => {
		const field = props.fields[index]
		const isSelected = field.id === selectedField.id
		polygon.setOptions(isSelected ? selectedPolygonOptions : defaultPolygonOptions)
	})
}

function panToField(field) {
	if (!map) return

	const bounds = new google.maps.LatLngBounds()
	field.field_area.forEach((coord) => {
		bounds.extend({ lat: coord[0], lng: coord[1] })
	})

	map.fitBounds(bounds)

	setTimeout(() => {
		const currentZoom = map.getZoom()
		if (currentZoom > 19) {
			map.setZoom(19)
		}
	}, 500)
}

onMounted(async () => {
	loading.value = true
	try {
		await mapsLoader.load()
		initializeMap()
		if (props.fields.length > 0) {
			drawPolygons(props.fields)
		}
		if (props.selectedField) {
			highlightSelectedField(props.selectedField)
			panToField(props.selectedField)
		}
	} catch (error) {
		console.error('Error initializing map:', error)
	} finally {
		loading.value = false
	}
})

onUnmounted(() => {
	if (map) {
		google.maps.event.clearListeners(map, 'click')
	}
})
</script>

<style scoped>
.custom-spinner {
	width: 60px;
	height: 60px;
	border: 6px solid rgba(0, 0, 0, 0.1);
	border-top-color: rgba(0, 0, 0, 0.8);
	border-radius: 50%;
	animation: spin 1s linear infinite;
}

@media (prefers-color-scheme: dark) {
	.custom-spinner {
		border: 6px solid rgba(255, 255, 255, 0.1);
		border-top-color: rgba(255, 255, 255, 0.8);
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
