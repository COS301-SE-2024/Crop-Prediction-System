<template>
	<Menu :model="items" class="border-none dark:bg-surface-800">
		<template #submenuheader="{ item }">
			<span class="text-black dark:text-white ml-[-12px] font-[500] p-0">{{ item.label }}</span>
		</template>
		<template #item="{ item }">
			<RouterLink v-if="!item.separator" :to="item.url" custom v-slot="{ href, isActive }">
				<a :href="href" :class="{ active: isActive }" class="flex flex-row gap-2 items-center py-2">
					<span :class="item.icon" class="pl-4" />
					<span>{{ item.label }}</span>
				</a>
			</RouterLink>
		</template>
	</Menu>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import Menu from 'primevue/menu'
import { useRoute } from 'vue-router'

const items = ref([
	{
		label: 'HOME',
		items: [
			{
				label: 'Dashboard',
				icon: 'pi pi-home',
				url: '/',
			},
		],
	},
	{
		label: 'INPUTS',
		items: [
			{
				label: 'Add Field Data',
				icon: 'pi pi-plus-circle',
				url: '/inputs/add-field-data',
			},
			{
				label: 'Manage Fields',
				url: '/inputs/manage-fields',
				icon: 'pi pi-map-marker',
			},
		],
	},
	{
		label: 'LOGS',
		items: [
			{
				label: 'View Logs',
				url: '/log-data/view-logs',
				icon: 'pi pi-list',
			},
		],
	},
	{
		label: 'MODEL TRAINING',
		items: [
			{
				label: 'Manage Model',
				url: '/model-training/manage-model',
				icon: 'pi pi-microchip-ai',
			},
		],
	},
	{
		label: 'ANALYTICS',
		items: [
			{
				label: 'Crop Yield Data',
				url: '/analytics/crop-yield-data',
				icon: 'pi pi-chart-pie',
			},
		],
	},
	{
		label: 'TEAM MANAGEMENT',
		items: [
			{
				label: 'Manage Team',
				url: '/team/manage',
				icon: 'pi pi-users',
			},
			// {
			// 	label: 'Create a Team',
			// 	url: '/team/create',
			// 	icon: 'pi pi-plus-circle',
			// },
			{
				label: 'Join a Team',
				url: '/team/join',
				icon: 'pi pi-sign-in',
			},
		],
	},
])

const route = useRoute()

// Watch the route for changes and update the active item

function updateActiveItem(items: MenuItem[], path: string) {
	for (const item of items) {
		if (item.url === path) {
			item.active = true
		} else if (item.items) {
			updateActiveItem(item.items, path)
		} else {
			item.active = false
		}
	}
}

watch(
	() => route.path,
	(newPath) => {
		updateActiveItem(items.value, newPath)
	},
)
</script>

<style>
.active {
	color: #11b981;
}
</style>
