<template>
	<Menu :model="items" class="border-none">
		<template #submenuheader="{ item }">
			<span class="text-black dark:text-white ml-[-12px] font-[500] p-0">{{ item.label }}</span>
		</template>
		<template #item="{ item }">
			<RouterLink v-if="!item.separator" :to="item.url || ''" custom v-slot="{ href, isActive }">
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
import type { MenuItem } from 'primevue/menuitem'

const items = ref([
	{
		label: 'HOME',
		items: [
			{
				label: 'Field Dashboard',
				icon: 'pi pi-chart-bar',
				url: '/',
			},
			{
				label: 'Revenue Dashboard',
				icon: 'pi pi-wallet',
				url: '/market',
			},
		],
	},
	{
		label: 'FIELDS',
		items: [
			{
				label: 'Manage Fields',
				url: '/inputs/manage-fields',
				icon: 'pi pi-pen-to-square',
			},
			{
				label: 'Add New Field',
				url: '/inputs/add-field',
				icon: 'pi pi-map',
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
		label: 'TEAM',
		items: [
			{
				label: 'Manage Team',
				url: '/team/manage',
				icon: 'pi pi-users',
			},
			{
				label: 'Team Chat',
				url: '/team/chat',
				icon: 'pi pi-comment',
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
