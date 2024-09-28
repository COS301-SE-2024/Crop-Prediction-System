<template>
	<nav id="nav" class="bg-surface-0 dark:bg-surface-900 text-surface-700 dark:text-surface-0 shadow-md">
		<div class="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
			<div class="flex items-center justify-between h-16">
				<!-- Logo -->
				<div class="flex-shrink-0">
					<img src="../assets/logo.png" alt="Logo" class="w-36 xl:h-14 xl:w-auto object-cover dark:hidden block" />
					<img src="../assets/logo-alt.png" alt="Logo" class="w-36 xl:h-14 xl:w-auto object-cover hidden dark:block" />
				</div>

				<!-- Desktop Menu -->
				<div class="hidden lg:flex lg:flex-grow lg:items-center lg:justify-end">
					<ul class="flex space-x-4">
						<li v-for="item in menuItems" :key="item.name">
							<a
								@click="() => smoothScroll(item.href)"
								class="px-2 py-2 rounded-md text-sm font-medium text-gray-700 dark:text-gray-200 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-700 transition duration-150 ease-in-out cursor-pointer whitespace-nowrap"
							>
								<i :class="item.icon" class="mr-2"></i>
								{{ item.name }}
							</a>
						</li>
						<li v-for="item in items" :key="item.name">
							<a
								@click="item.command"
								class="px-2 py-2 rounded-md text-sm font-medium text-gray-700 dark:text-gray-200 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-700 transition duration-150 ease-in-out cursor-pointer whitespace-nowrap"
							>
								<i :class="item.icon"></i>
								<span v-if="item.name" class="ml-2">{{ item.name }}</span>
							</a>
						</li>
					</ul>
				</div>

				<!-- Mobile menu button -->
				<div class="lg:hidden">
					<button
						@click="toggle"
						class="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500"
					>
						<span class="sr-only">Open main menu</span>
						<i :class="{ hidden: mobileMenuOpen, block: !mobileMenuOpen, 'pi pi-bars': true }" aria-hidden="true"></i>
					</button>
				</div>
			</div>
		</div>

		<!-- Mobile menu, show/hide based on menu state -->
		<div :class="{ block: mobileMenuOpen, hidden: !mobileMenuOpen }" class="lg:hidden">
			<div class="px-2 pt-2 pb-3 space-y-1">
				<a
					v-for="item in menuItems"
					:key="item.name"
					@click="
						() => {
							smoothScroll(item.href)
							mobileMenuOpen = false
						}
					"
					class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 dark:text-gray-200 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer align-middle"
				>
					<i :class="item.icon" class="mr-2"></i>
					{{ item.name }}
				</a>
				<a
					v-for="item in items"
					:key="item.name"
					@click="item.command"
					class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 dark:text-gray-200 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer align-middle"
				>
					<i :class="item.icon" class="mr-2"></i>
					{{ item.name }}
				</a>
			</div>
		</div>
	</nav>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const mobileMenuOpen = ref(false)
const menu = ref()

const menuItems = [
	{ name: 'HOME', icon: 'pi pi-home', href: '#hero' },
	{ name: 'FEATURES', icon: 'pi pi-star', href: '#features' },
	{ name: 'HIGHLIGHTS', icon: 'pi pi-star-fill', href: '#highlights' },
	{ name: 'ABOUT', icon: 'pi pi-info-circle', href: '#about' },
]

const items = computed(() => [
	{
		name: 'TOGGLE THEME',
		icon: useColorMode().preference === 'dark' ? 'pi pi-sun' : 'pi pi-moon',
		command: () => {
			setColorTheme(useColorMode().preference === 'dark' ? 'light' : 'dark')
		},
	},
	{
		name: 'REGISTER',
		icon: 'pi pi-user-plus',
		command: () => {
			window.open('https://app.terrabyte.software/login')
		},
	},
	{
		icon: 'pi pi-github',
		command: () => {
			window.open('https://github.com/COS301-SE-2024/Crop-Prediction-System')
		},
	},
])

const smoothScroll = (elementId: string) => {
	const element = document.querySelector(elementId)
	element?.scrollIntoView({ behavior: 'smooth' })
}

const toggle = (event: Event) => {
	menu.value?.toggle(event)
	mobileMenuOpen.value = !mobileMenuOpen.value
}

type Theme = 'light' | 'dark'
const setColorTheme = (newTheme: Theme) => {
	useColorMode().preference = newTheme
}
</script>
