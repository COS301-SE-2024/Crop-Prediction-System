<script setup lang="ts">
import { ref, computed } from 'vue'
import OverlayPanel from 'primevue/overlaypanel'
import Menu from 'primevue/menu'

function smoothScroll(id) {
	document.body.click()
	document.querySelector(id).scrollIntoView({
		behavior: 'smooth',
	})
}

const menu = ref()
const items = computed(() => [
	{
		label: 'Toggle Theme',
		icon: useColorMode().preference == 'dark' ? 'pi pi-sun' : 'pi pi-moon',
		command: () => {
			setColorTheme(useColorMode().preference == 'dark' ? 'light' : 'dark')
		},
	},
	{
		label: 'Signup',
		icon: 'pi pi-signup',
		command: () => {
			window.location.href = '/help'
		},
	},
	{
		label: 'Login',
		icon: 'pi pi-login',
		command: () => {
			window.location.href = '/settings'
		},
	},
])

const toggle = (event) => {
	menu.value.toggle(event)
}

type Theme = 'light' | 'dark'

const setColorTheme = (newTheme: Theme) => {
	useColorMode().preference = newTheme
}
</script>

<template>
	<div class="bg-surface-0 dark:bg-surface-900">
		<div id="home" class="landing-wrapper overflow-hidden">
			<!-- <div class="py-6 px-6 mx-0 md:mx-12 lg:mx-20 lg:px-20 flex items-center justify-between relative lg:static"> -->
			<!-- <template>
				<div class="py-6 px-6 mx-0 md:mx-12 lg:mx-20 lg:px-20 flex items-center justify-between relative lg:static">
					<div class="flex justify-between px-0 py-0 text-surface-900 dark:text-surface-0 font-medium text-xl w-full">
						<Menubar :model="menu">
							<template #start>
								<img
									src="../assets/logo.png"
									alt="Logo"
									class="w-36 xl:h-14 xl:w-auto object-cover dark:hidden block"
								/>
								<img
									src="../assets/logo-alt.png"
									alt="Logo"
									class="w-36 xl:h-14 xl:w-auto object-cover hidden dark:block"
								/>
							</template>
							<template #item="{ item, props, hasSubmenu, root }">
								<a
									v-ripple
									class="items rounded-md transition-colors duration-200 hover:bg-gray-100 dark:hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-gray-300 dark:focus:ring-gray-600"
									v-bind="props.action"
								>
									<span :class="item.icon" />
									<span class="ml-2">{{ item.label }}</span>
									<Badge v-if="item.badge" :class="{ 'ml-auto': !root, 'ml-2': root }" :value="item.badge" />
									<span
										v-if="item.shortcut"
										class="ml-auto border border-surface rounded bg-emphasis text-muted-color text-xs p-1"
										>{{ item.shortcut }}</span
									>
									<i
										v-if="hasSubmenu"
										:class="[
											'pi pi-angle-down',
											{ 'pi-angle-down ml-2': root, 'pi-angle-right ml-auto': !root },
										]"
									></i>
								</a>
							</template>
						</Menubar>
					</div>
				</div>
			</template> -->
			<!-- <div
					class="items-center bg-surface-0 dark:bg-surface-900 grow justify-between hidden lg:flex absolute lg:static w-full left-0 top-full px-12 lg:px-0 z-20 rounded-border"
				>
					<NuxtLink to="/" class="text-2xl font-[500] text-primary-500 justify-self-center self-center h-full">
						<img src="../assets/logo.png" alt="Logo" class="w-36 xl:h-14 xl:w-auto object-cover dark:hidden block" />
						<img
							src="../assets/logo-alt.png"
							alt="Logo"
							class="w-36 xl:h-14 xl:w-auto object-cover hidden dark:block"
						/>
					</NuxtLink>
				</div>
				<Button
					class="lg:!hidden"
					text
					severity="secondary"
					rounded
					v-styleclass="{
						selector: '@next',
						enterFromClass: 'hidden',
						enterActiveClass: 'animate-scalein',
						leaveToClass: 'hidden',
						leaveActiveClass: 'animate-fadeout',
						hideOnOutsideClick: true,
					}"
				>
					<i class="pi pi-bars !text-2xl"></i>
				</Button>
				<div
					class="items-center bg-surface-0 dark:bg-surface-900 grow justify-between hidden lg:flex absolute lg:static w-full left-0 top-full px-12 lg:px-0 z-20 rounded-border"
				>
					<ul class="list-none p-0 m-0 flex lg:items-center select-none flex-col lg:flex-row cursor-pointer gap-8">
						<li>
							<a
								@click="() => smoothScroll('#hero')"
								class="px-0 py-4 text-surface-900 dark:text-surface-0 font-medium text-xl"
							>
								<span>HOME</span>
							</a>
						</li>
						<li>
							<a
								@click="() => smoothScroll('#features')"
								class="px-0 py-4 text-surface-900 dark:text-surface-0 font-medium text-xl"
							>
								<span>FEATURES</span>
							</a>
						</li>
						<li>
							<a
								@click="() => smoothScroll('#about')"
								class="px-0 py-4 text-surface-900 dark:text-surface-0 font-medium text-xl"
							>
								<span>ABOUT</span>
							</a>
						</li>
						<li>
							<a
								@click="() => smoothScroll('#contact')"
								class="px-0 py-4 text-surface-900 dark:text-surface-0 font-medium text-xl"
							>
								<span>CONTACT</span>
							</a>
						</li>
						<li>
							<a class="px-0 py-4 text-surface-900 dark:text-surface-0 font-medium text-xl">
								<Button>Register</Button>
							</a>
						</li>
						<li>
							<a
								@click="() => smoothScroll('#contact')"
								class="px-0 py-4 text-surface-900 dark:text-surface-0 font-medium text-xl"
								label: 'Toggle Theme',
								icon: useColorMode().preference == 'dark' ? 'pi pi-sun' : 'pi pi-moon',
								command: () => {
									setColorTheme(useColorMode().preference == 'dark' ? 'light' : 'dark')
								},
							>
								<span>Theme</span>
							</a>
						</li>
					</ul>
				</div>
			</div> -->
			<div
				id="hero"
				class="flex flex-col pt-6 px-6 lg:px-20 overflow-hidden"
				style="
					background: linear-gradient(0deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.2)),
						radial-gradient(77.36% 256.97% at 77.36% 57.52%, rgb(238, 239, 175) 0%, rgb(195, 227, 250) 100%);
					clip-path: ellipse(150% 87% at 93% 13%);
				"
			>
				<div class="mx-6 md:mx-20 mt-0 md:mt-6">
					<h1 class="text-6xl font-bold text-gray-900 leading-tight">
						<span class="font-light block">Eu sem integer</span>eget magna fermentum
					</h1>
					<p class="font-normal text-2xl leading-normal md:mt-4 text-gray-700">
						Sed blandit libero volutpat sed cras. Fames ac turpis egestas integer. Placerat in egestas erat...
					</p>
					<Button label="Get Started" as="router-link" to="/" rounded class="!text-xl mt-8 !px-4"></Button>
				</div>
				<div class="flex justify-center md:justify-end">
					<img src="" alt="Hero Image" class="w-9/12 md:w-auto" />
				</div>
			</div>
			<div id="features" class="py-6 px-6 lg:px-20 mt-8 mx-0 lg:mx-20">
				<div class="grid grid-cols-12 gap-4 justify-center">
					<div class="col-span-12 text-center mt-20 mb-6">
						<div class="text-surface-900 dark:text-surface-0 font-normal mb-2 text-4xl">Marvelous Features</div>
						<span class="text-muted-color text-2xl">Placerat in egestas erat...</span>
					</div>
					<div class="col-span-12 md:col-span-12 lg:col-span-4 p-0 lg:pr-8 lg:pb-8 mt-6 lg:mt-0">
						<div
							style="
								height: 160px;
								padding: 2px;
								border-radius: 10px;
								background: linear-gradient(90deg, rgba(253, 228, 165, 0.2), rgba(187, 199, 205, 0.2)),
									linear-gradient(180deg, rgba(253, 228, 165, 0.2), rgba(187, 199, 205, 0.2));
							"
						>
							<div class="p-4 bg-surface-0 dark:bg-surface-900 h-full" style="border-radius: 8px">
								<div
									class="flex items-center justify-center bg-yellow-200 mb-4"
									style="width: 3.5rem; height: 3.5rem; border-radius: 10px"
								>
									<i class="pi pi-fw pi-users !text-2xl text-yellow-700"></i>
								</div>
								<h5 class="mb-2 text-surface-900 dark:text-surface-0">Easy to Use</h5>
								<span class="text-surface-600 dark:text-surface-200">Posuere morbi leo urna molestie.</span>
							</div>
						</div>
					</div>
					<div class="col-span-12 md:col-span-12 lg:col-span-4 p-0 lg:pr-8 lg:pb-8 mt-6 lg:mt-0">
						<div
							style="
								height: 160px;
								padding: 2px;
								border-radius: 10px;
								background: linear-gradient(90deg, rgba(145, 226, 237, 0.2), rgba(251, 199, 145, 0.2)),
									linear-gradient(180deg, rgba(253, 228, 165, 0.2), rgba(172, 180, 223, 0.2));
							"
						>
							<div class="p-4 bg-surface-0 dark:bg-surface-900 h-full" style="border-radius: 8px">
								<div
									class="flex items-center justify-center bg-cyan-200 mb-4"
									style="width: 3.5rem; height: 3.5rem; border-radius: 10px"
								>
									<i class="pi pi-fw pi-palette !text-2xl text-cyan-700"></i>
								</div>
								<h5 class="mb-2 text-surface-900 dark:text-surface-0">Fresh Design</h5>
								<span class="text-surface-600 dark:text-surface-200">Semper risus in hendrerit.</span>
							</div>
						</div>
					</div>
					<div class="col-span-12 md:col-span-12 lg:col-span-4 p-0 lg:pb-8 mt-6 lg:mt-0">
						<div
							style="
								height: 160px;
								padding: 2px;
								border-radius: 10px;
								background: linear-gradient(90deg, rgba(145, 226, 237, 0.2), rgba(172, 180, 223, 0.2)),
									linear-gradient(180deg, rgba(172, 180, 223, 0.2), rgba(246, 158, 188, 0.2));
							"
						>
							<div class="p-4 bg-surface-0 dark:bg-surface-900 h-full" style="border-radius: 8px">
								<div
									class="flex items-center justify-center bg-indigo-200"
									style="width: 3.5rem; height: 3.5rem; border-radius: 10px"
								>
									<i class="pi pi-fw pi-map !text-2xl text-indigo-700"></i>
								</div>
								<div class="mt-6 mb-1 text-surface-900 dark:text-surface-0 text-xl font-semibold">
									Well Documented
								</div>
								<span class="text-surface-600 dark:text-surface-200"
									>Non arcu risus quis varius quam quisque.</span
								>
							</div>
						</div>
					</div>
					<div class="col-span-12 md:col-span-12 lg:col-span-4 p-0 lg:pr-8 lg:pb-8 mt-6 lg:mt-0">
						<div
							style="
								height: 160px;
								padding: 2px;
								border-radius: 10px;
								background: linear-gradient(90deg, rgba(187, 199, 205, 0.2), rgba(251, 199, 145, 0.2)),
									linear-gradient(180deg, rgba(253, 228, 165, 0.2), rgba(145, 210, 204, 0.2));
							"
						>
							<div class="p-4 bg-surface-0 dark:bg-surface-900 h-full" style="border-radius: 8px">
								<div
									class="flex items-center justify-center bg-slate-200 mb-4"
									style="width: 3.5rem; height: 3.5rem; border-radius: 10px"
								>
									<i class="pi pi-fw pi-id-card !text-2xl text-slate-700"></i>
								</div>
								<div class="mt-6 mb-1 text-surface-900 dark:text-surface-0 text-xl font-semibold">
									Responsive Layout
								</div>
								<span class="text-surface-600 dark:text-surface-200">Nulla malesuada pellentesque elit.</span>
							</div>
						</div>
					</div>
					<div class="col-span-12 md:col-span-12 lg:col-span-4 p-0 lg:pr-8 lg:pb-8 mt-6 lg:mt-0">
						<div
							style="
								height: 160px;
								padding: 2px;
								border-radius: 10px;
								background: linear-gradient(90deg, rgba(187, 199, 205, 0.2), rgba(246, 158, 188, 0.2)),
									linear-gradient(180deg, rgba(145, 226, 237, 0.2), rgba(160, 210, 250, 0.2));
							"
						>
							<div class="p-4 bg-surface-0 dark:bg-surface-900 h-full" style="border-radius: 8px">
								<div
									class="flex items-center justify-center bg-orange-200 mb-4"
									style="width: 3.5rem; height: 3.5rem; border-radius: 10px"
								>
									<i class="pi pi-fw pi-star !text-2xl text-orange-700"></i>
								</div>
								<div class="mt-6 mb-1 text-surface-900 dark:text-surface-0 text-xl font-semibold">Clean Code</div>
								<span class="text-surface-600 dark:text-surface-200">Condimentum lacinia quis vel eros.</span>
							</div>
						</div>
					</div>
					<div class="col-span-12 md:col-span-12 lg:col-span-4 p-0 lg:pb-8 mt-6 lg:mt-0">
						<div
							style="
								height: 160px;
								padding: 2px;
								border-radius: 10px;
								background: linear-gradient(90deg, rgba(251, 199, 145, 0.2), rgba(246, 158, 188, 0.2)),
									linear-gradient(180deg, rgba(172, 180, 223, 0.2), rgba(212, 162, 221, 0.2));
							"
						>
							<div class="p-4 bg-surface-0 dark:bg-surface-900 h-full" style="border-radius: 8px">
								<div
									class="flex items-center justify-center bg-pink-200 mb-4"
									style="width: 3.5rem; height: 3.5rem; border-radius: 10px"
								>
									<i class="pi pi-fw pi-moon !text-2xl text-pink-700"></i>
								</div>
								<div class="mt-6 mb-1 text-surface-900 dark:text-surface-0 text-xl font-semibold">Dark Mode</div>
								<span class="text-surface-600 dark:text-surface-200"
									>Convallis tellus id interdum velit laoreet.</span
								>
							</div>
						</div>
					</div>
					<div class="col-span-12 md:col-span-12 lg:col-span-4 p-0 lg:pr-8 mt-6 lg:mt-0">
						<div
							style="
								height: 160px;
								padding: 2px;
								border-radius: 10px;
								background: linear-gradient(90deg, rgba(145, 210, 204, 0.2), rgba(160, 210, 250, 0.2)),
									linear-gradient(180deg, rgba(187, 199, 205, 0.2), rgba(145, 210, 204, 0.2));
							"
						>
							<div class="p-4 bg-surface-0 dark:bg-surface-900 h-full" style="border-radius: 8px">
								<div
									class="flex items-center justify-center bg-teal-200 mb-4"
									style="width: 3.5rem; height: 3.5rem; border-radius: 10px"
								>
									<i class="pi pi-fw pi-shopping-cart !text-2xl text-teal-700"></i>
								</div>
								<div class="mt-6 mb-1 text-surface-900 dark:text-surface-0 text-xl font-semibold">
									Ready to Use
								</div>
								<span class="text-surface-600 dark:text-surface-200">Mauris sit amet massa vitae.</span>
							</div>
						</div>
					</div>
					<div class="col-span-12 md:col-span-12 lg:col-span-4 p-0 lg:pr-8 mt-6 lg:mt-0">
						<div
							style="
								height: 160px;
								padding: 2px;
								border-radius: 10px;
								background: linear-gradient(90deg, rgba(145, 210, 204, 0.2), rgba(212, 162, 221, 0.2)),
									linear-gradient(180deg, rgba(251, 199, 145, 0.2), rgba(160, 210, 250, 0.2));
							"
						>
							<div class="p-4 bg-surface-0 dark:bg-surface-900 h-full" style="border-radius: 8px">
								<div
									class="flex items-center justify-center bg-blue-200 mb-4"
									style="width: 3.5rem; height: 3.5rem; border-radius: 10px"
								>
									<i class="pi pi-fw pi-globe !text-2xl text-blue-700"></i>
								</div>
								<div class="mt-6 mb-1 text-surface-900 dark:text-surface-0 text-xl font-semibold">
									Modern Practices
								</div>
								<span class="text-surface-600 dark:text-surface-200"
									>Elementum nibh tellus molestie nunc non.</span
								>
							</div>
						</div>
					</div>
					<div class="col-span-12 md:col-span-12 lg:col-span-4 p-0 lg-4 mt-6 lg:mt-0">
						<div
							style="
								height: 160px;
								padding: 2px;
								border-radius: 10px;
								background: linear-gradient(90deg, rgba(160, 210, 250, 0.2), rgba(212, 162, 221, 0.2)),
									linear-gradient(180deg, rgba(246, 158, 188, 0.2), rgba(212, 162, 221, 0.2));
							"
						>
							<div class="p-4 bg-surface-0 dark:bg-surface-900 h-full" style="border-radius: 8px">
								<div
									class="flex items-center justify-center bg-purple-200 mb-4"
									style="width: 3.5rem; height: 3.5rem; border-radius: 10px"
								>
									<i class="pi pi-fw pi-eye !text-2xl text-purple-700"></i>
								</div>
								<div class="mt-6 mb-1 text-surface-900 dark:text-surface-0 text-xl font-semibold">Privacy</div>
								<span class="text-surface-600 dark:text-surface-200">Neque egestas congue quisque.</span>
							</div>
						</div>
					</div>

					<div
						class="col-span-12 mt-20 mb-20 p-2 md:p-20"
						style="
							border-radius: 20px;
							background: linear-gradient(0deg, rgba(255, 255, 255, 0.6), rgba(255, 255, 255, 0.6)),
								radial-gradient(77.36% 256.97% at 77.36% 57.52%, #efe1af 0%, #c3dcfa 100%);
						"
					>
						<div class="flex flex-col justify-center items-center text-center px-4 py-4 md:py-0">
							<div class="text-gray-900 mb-2 text-3xl font-semibold">Joséphine Miller</div>
							<span class="text-gray-600 text-2xl">Peak Interactive</span>
							<p class="text-gray-900 sm:line-height-2 md:line-height-4 text-2xl mt-6" style="max-width: 800px">
								“Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
								pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt
								mollit anim id est laborum.”
							</p>
							<img src="" class="mt-6" alt="Company logo" />
						</div>
					</div>
				</div>
			</div>
			<div id="highlights" class="py-6 px-6 lg:px-20 mx-0 my-12 lg:mx-20">
				<div class="text-center">
					<div class="text-surface-900 dark:text-surface-0 font-normal mb-2 text-4xl">Powerful Everywhere</div>
					<span class="text-muted-color text-2xl">Amet consectetur adipiscing elit...</span>
				</div>
				<div class="grid grid-cols-12 gap-4 mt-20 pb-2 md:pb-20">
					<div
						class="flex justify-center col-span-12 lg:col-span-6 bg-purple-100 p-0 order-1 lg:order-none"
						style="border-radius: 8px"
					>
						<img src="" class="w-11/12" alt="mockup mobile" />
					</div>
					<div class="col-span-12 lg:col-span-6 my-auto flex flex-col lg:items-end text-center lg:text-right gap-4">
						<div
							class="flex items-center justify-center bg-purple-200 self-center lg:self-end"
							style="width: 4.2rem; height: 4.2rem; border-radius: 10px"
						>
							<i class="pi pi-fw pi-mobile !text-4xl text-purple-700"></i>
						</div>
						<div class="leading-none text-surface-900 dark:text-surface-0 text-3xl font-normal">
							Congue Quisque Egestas
						</div>
						<span
							class="text-surface-700 dark:text-surface-100 text-2xl leading-normal ml-0 md:ml-2"
							style="max-width: 650px"
							>Lectus arcu bibendum at varius vel pharetra vel turpis nunc. Eget aliquet nibh praesent tristique
							magna sit amet purus gravida. Sit amet mattis vulputate enim nulla aliquet.</span
						>
					</div>
				</div>
				<div class="grid grid-cols-12 gap-4 my-20 pt-2 md:pt-20">
					<div class="col-span-12 lg:col-span-6 my-auto flex flex-col text-center lg:text-left lg:items-start gap-4">
						<div
							class="flex items-center justify-center bg-yellow-200 self-center lg:self-start"
							style="width: 4.2rem; height: 4.2rem; border-radius: 10px"
						>
							<i class="pi pi-fw pi-desktop !text-3xl text-yellow-700"></i>
						</div>
						<div class="leading-none text-surface-900 dark:text-surface-0 text-3xl font-normal">
							Celerisque Eu Ultrices
						</div>
						<span
							class="text-surface-700 dark:text-surface-100 text-2xl leading-normal mr-0 md:mr-2"
							style="max-width: 650px"
							>Adipiscing commodo elit at imperdiet dui. Viverra nibh cras pulvinar mattis nunc sed blandit libero.
							Suspendisse in est ante in. Mauris pharetra et ultrices neque ornare aenean euismod elementum
							nisi.</span
						>
					</div>
					<div
						class="flex justify-end order-1 sm:order-2 col-span-12 lg:col-span-6 bg-yellow-100 p-0"
						style="border-radius: 8px"
					>
						<img src="" class="w-11/12" alt="mockup" />
					</div>
				</div>
			</div>
			<div id="about" class="py-6 px-6 lg:px-20 mx-0 my-12 lg:mx-20">
				<div class="text-center">
					<div class="text-surface-900 dark:text-surface-0 font-normal mb-2 text-4xl">Powerful Everywhere</div>
					<span class="text-muted-color text-2xl">Amet consectetur adipiscing elit...</span>
				</div>
				<div class="grid grid-cols-12 gap-4 mt-20 pb-2 md:pb-20">
					<div
						class="flex justify-center col-span-12 lg:col-span-6 bg-purple-100 p-0 order-1 lg:order-none"
						style="border-radius: 8px"
					>
						<img src="" class="w-11/12" alt="mockup mobile" />
					</div>
					<div class="col-span-12 lg:col-span-6 my-auto flex flex-col lg:items-end text-center lg:text-right gap-4">
						<div
							class="flex items-center justify-center bg-purple-200 self-center lg:self-end"
							style="width: 4.2rem; height: 4.2rem; border-radius: 10px"
						>
							<i class="pi pi-fw pi-mobile !text-4xl text-purple-700"></i>
						</div>
						<div class="leading-none text-surface-900 dark:text-surface-0 text-3xl font-normal">
							Congue Quisque Egestas
						</div>
						<span
							class="text-surface-700 dark:text-surface-100 text-2xl leading-normal ml-0 md:ml-2"
							style="max-width: 650px"
							>Lectus arcu bibendum at varius vel pharetra vel turpis nunc. Eget aliquet nibh praesent tristique
							magna sit amet purus gravida. Sit amet mattis vulputate enim nulla aliquet.</span
						>
					</div>
				</div>
				<div class="grid grid-cols-12 gap-4 my-20 pt-2 md:pt-20">
					<div class="col-span-12 lg:col-span-6 my-auto flex flex-col text-center lg:text-left lg:items-start gap-4">
						<div
							class="flex items-center justify-center bg-yellow-200 self-center lg:self-start"
							style="width: 4.2rem; height: 4.2rem; border-radius: 10px"
						>
							<i class="pi pi-fw pi-desktop !text-3xl text-yellow-700"></i>
						</div>
						<div class="leading-none text-surface-900 dark:text-surface-0 text-3xl font-normal">
							Celerisque Eu Ultrices
						</div>
						<span
							class="text-surface-700 dark:text-surface-100 text-2xl leading-normal mr-0 md:mr-2"
							style="max-width: 650px"
							>Adipiscing commodo elit at imperdiet dui. Viverra nibh cras pulvinar mattis nunc sed blandit libero.
							Suspendisse in est ante in. Mauris pharetra et ultrices neque ornare aenean euismod elementum
							nisi.</span
						>
					</div>
					<div
						class="flex justify-end order-1 sm:order-2 col-span-12 lg:col-span-6 bg-yellow-100 p-0"
						style="border-radius: 8px"
					>
						<img src="" class="w-11/12" alt="mockup" />
					</div>
				</div>
			</div>
			<div id="contact" class="py-6 px-6 lg:px-20 mx-0 my-12 lg:mx-20">
				<div class="text-center">
					<div class="text-surface-900 dark:text-surface-0 font-normal mb-2 text-4xl">Powerful Everywhere</div>
					<span class="text-muted-color text-2xl">Amet consectetur adipiscing elit...</span>
				</div>
				<div class="grid grid-cols-12 gap-4 mt-20 pb-2 md:pb-20">
					<div
						class="flex justify-center col-span-12 lg:col-span-6 bg-purple-100 p-0 order-1 lg:order-none"
						style="border-radius: 8px"
					>
						<img src="" class="w-11/12" alt="mockup mobile" />
					</div>
					<div class="col-span-12 lg:col-span-6 my-auto flex flex-col lg:items-end text-center lg:text-right gap-4">
						<div
							class="flex items-center justify-center bg-purple-200 self-center lg:self-end"
							style="width: 4.2rem; height: 4.2rem; border-radius: 10px"
						>
							<i class="pi pi-fw pi-mobile !text-4xl text-purple-700"></i>
						</div>
						<div class="leading-none text-surface-900 dark:text-surface-0 text-3xl font-normal">
							Congue Quisque Egestas
						</div>
						<span
							class="text-surface-700 dark:text-surface-100 text-2xl leading-normal ml-0 md:ml-2"
							style="max-width: 650px"
							>Lectus arcu bibendum at varius vel pharetra vel turpis nunc. Eget aliquet nibh praesent tristique
							magna sit amet purus gravida. Sit amet mattis vulputate enim nulla aliquet.</span
						>
					</div>
				</div>
				<div class="grid grid-cols-12 gap-4 my-20 pt-2 md:pt-20">
					<div class="col-span-12 lg:col-span-6 my-auto flex flex-col text-center lg:text-left lg:items-start gap-4">
						<div
							class="flex items-center justify-center bg-yellow-200 self-center lg:self-start"
							style="width: 4.2rem; height: 4.2rem; border-radius: 10px"
						>
							<i class="pi pi-fw pi-desktop !text-3xl text-yellow-700"></i>
						</div>
						<div class="leading-none text-surface-900 dark:text-surface-0 text-3xl font-normal">
							Celerisque Eu Ultrices
						</div>
						<span
							class="text-surface-700 dark:text-surface-100 text-2xl leading-normal mr-0 md:mr-2"
							style="max-width: 650px"
							>Adipiscing commodo elit at imperdiet dui. Viverra nibh cras pulvinar mattis nunc sed blandit libero.
							Suspendisse in est ante in. Mauris pharetra et ultrices neque ornare aenean euismod elementum
							nisi.</span
						>
					</div>
					<div
						class="flex justify-end order-1 sm:order-2 col-span-12 lg:col-span-6 bg-yellow-100 p-0"
						style="border-radius: 8px"
					>
						<img src="" class="w-11/12" alt="mockup" />
					</div>
				</div>
			</div>
		</div>
	</div>
</template>
