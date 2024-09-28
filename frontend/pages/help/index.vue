<template>
	<div>
		<Dropdown v-model="selectedItem" :options="items" optionLabel="name" placeholder="Select a Menu" class="w-full md:w-64" />
		<HelpFieldDashboard :activeIndex="activeIndex" />
		<HelpRevenueDashboard :activeIndex="activeIndex" />
		<HelpManageFields :activeIndex="activeIndex" />
		<HelpAddField :activeIndex="activeIndex" />
		<HelpLogs :activeIndex="activeIndex" />
		<HelpTeamManage :activeIndex="activeIndex" />
		<HelpChat :activeIndex="activeIndex" />
	</div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import HelpFieldDashboard from '~/components/HelpFieldDashboard.vue'
import HelpRevenueDashboard from '~/components/HelpRevenueDashboard.vue'
import HelpManageFields from '~/components/HelpManageFields.vue'
import HelpAddField from '~/components/HelpAddField.vue'
import HelpLogs from '~/components/HelpLogs.vue'
import HelpTeamManage from '~/components/HelpTeamManage.vue'
import HelpChat from '~/components/HelpChat.vue'

const activeIndex = ref(0)

const selectedItem = ref({ name: 'Home Dashboard', activeIndex: 0 })
const items = ref([
	{ name: 'Field Dashboard', activeIndex: 0 },
	{ name: 'Revenue Dashboard', activeIndex: 1 },
	{ name: 'Manage Fields', activeIndex: 2 },
	{ name: 'Add Field', activeIndex: 3 },
	{ name: 'View Logs', activeIndex: 4 },
	{ name: 'Manage Team', activeIndex: 5 },
	{ name: 'Team Chat', activeIndex: 6 },
])

watch(selectedItem, (value) => {
	activeIndex.value = value.activeIndex
})

definePageMeta({
	middleware: 'auth',
})
</script>
