<template>
	<nav class="p-2 px-5 z-50 w-full shadow-md dark:bg-surface-900">
		<div class="flex justify-between xl:justify-normal xl:grid xl:grid-cols-3 h-full w-full">
			<Sidebar class="justify-self-start"/>
            <NuxtLink to="/" class="text-2xl font-[500] text-primary-500 justify-self-center self-center h-full">
                <img src="../assets/logo.png" alt="Logo" class="w-36 xl:h-14 xl:w-auto object-cover dark:hidden block" />
                <img src="../assets/logo-alt.png" alt="Logo" class="w-36 xl:h-14 xl:w-auto object-cover hidden dark:block" />
            </NuxtLink>
			<div class="flex flex-row items-center justify-end gap-4 justify-self-end dark:text-white">
                <div class="p-5 sm:p-0">
                    <i class="pi pi-bell" style="font-size: 1.5rem" />
                </div>
                <div class="hidden sm:block">
                    <i class="pi pi-user" style="font-size: 1.5rem" />
                </div>
                <div class="hidden sm:block">
                    <i class="pi pi-cog" style="font-size: 1.5rem" />
                </div>
			</div>
		</div>
	</nav>
</template>

<script setup lang="ts">
import Sidebar from '../components/Sidebar.vue'
</script>
