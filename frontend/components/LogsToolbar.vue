<template>
	<Toolbar>
		<template #start>
			<Button icon="pi pi-plus" class="mr-2" severity="secondary" />
			<Button icon="pi pi-print" class="mr-2" severity="secondary" />
			<Button icon="pi pi-upload" severity="secondary" />
		</template>

		<template #center>
			<IconField iconPosition="left" class="hidden lg:block">
				<InputIcon>
					<i class="pi pi-search" />
				</InputIcon>
				<InputText placeholder="Search" />
			</IconField>
		</template>

		<template #end> <SplitButton label="Save" :model="items"></SplitButton></template>
	</Toolbar>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const items = ref([
	{
		label: 'Update',
		icon: 'pi pi-refresh',
	},
	{
		label: 'Delete',
		icon: 'pi pi-times',
	},
])
</script>
