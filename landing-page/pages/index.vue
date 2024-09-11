<script setup lang="ts">
import Tabs from 'primevue/tabs'
import TabList from 'primevue/tablist'
import Tab from 'primevue/tab'
import TabPanels from 'primevue/tabpanels'
import TabPanel from 'primevue/tabpanel'
</script>

<template>
	<div class="bg-surface-0 dark:bg-surface-900 text-surface-900 dark:text-surface-0">
		<div id="home" class="landing-wrapper overflow-hidden">
			<div
				id="hero"
				class="flex flex-col pt-6 px-6 lg:px-20 overflow-hidden"
				style="
					background: linear-gradient(0deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.2)),
						radial-gradient(77.36% 256.97% at 77.36% 57.52%, rgb(238, 239, 175) 0%, rgb(195, 227, 250) 100%);
					clip-path: ellipse(150% 87% at 93% 13%);
				"
			>
				<div class="mx-6 md:mx-20 mt-0 md:mt-6"></div>
				<div class="flex justify-center md:justify-end">
					<img src="../assets/image-light.png" alt="Logo" class="object-cover dark:hidden block" />
					<img src="../assets/image-dark.png" alt="Logo" class="object-cover hidden dark:block" />
				</div>
			</div>
			<div id="features" class="py-12 px-4 sm:px-6 lg:px-8">
				<div class="max-w-7xl mx-auto">
					<div class="text-center">
						<h2 class="text-3xl sm:text-4xl lg:text-5xl font-bold text-surface-900 dark:text-surface-0 mb-4">
							Our Features
						</h2>
						<p class="text-xl text-surface-600 dark:text-surface-200 mb-12"></p>
					</div>

					<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
						<!-- Feature 1 -->
						<div
							class="bg-gradient-to-br from-yellow-100 to-yellow-200 dark:from-yellow-900 dark:to-yellow-800 p-0.5 rounded-lg"
						>
							<div class="bg-surface-0 dark:bg-surface-900 h-full p-6 rounded-lg">
								<div
									class="flex items-center justify-center w-12 h-12 bg-yellow-200 dark:bg-yellow-700 rounded-lg mb-4"
								>
									<i class="pi pi-users text-2xl text-yellow-700 dark:text-yellow-200"></i>
								</div>
								<h2 class="text-xl font-semibold text-surface-900 dark:text-surface-0 mb-2">Easy to Use</h2>
								<p class="text-surface-600 dark:text-surface-200">
									We have ensured that our product is very user-friendly by designing it such that it is easily
									understandably and easy to navigate. We also provide a help menus for extra information.
								</p>
							</div>
						</div>

						<!-- Feature 2 -->
						<div
							class="bg-gradient-to-br from-cyan-100 to-cyan-200 dark:from-cyan-900 dark:to-cyan-800 p-0.5 rounded-lg"
						>
							<div class="bg-surface-0 dark:bg-surface-900 h-full p-6 rounded-lg">
								<div
									class="flex items-center justify-center w-12 h-12 bg-cyan-200 dark:bg-cyan-700 rounded-lg mb-4"
								>
									<i class="pi pi-palette text-2xl text-cyan-700 dark:text-cyan-200"></i>
								</div>
								<h2 class="text-xl font-semibold text-surface-900 dark:text-surface-0 mb-2">Fresh Design</h2>
								<p class="text-surface-600 dark:text-surface-200">
									Our product has a modern and sleek design that catches the eye. It implements a bunch of
									interesting and unique features that makes it stand out.
								</p>
							</div>
						</div>

						<!-- Feature 3 -->
						<div
							class="bg-gradient-to-br from-indigo-100 to-indigo-200 dark:from-indigo-900 dark:to-indigo-800 p-0.5 rounded-lg"
						>
							<div class="bg-surface-0 dark:bg-surface-900 h-full p-6 rounded-lg">
								<div
									class="flex items-center justify-center w-12 h-12 bg-indigo-200 dark:bg-indigo-700 rounded-lg mb-4"
								>
									<i class="pi pi-file text-2xl text-indigo-700 dark:text-indigo-200"></i>
								</div>
								<h2 class="text-xl font-semibold text-surface-900 dark:text-surface-0 mb-2">Well Documented</h2>
								<p class="text-surface-600 dark:text-surface-200">
									Our product has comprehensive documentation for easy reference and understanding. We
									implemented an in-app help menu for extra information.
								</p>
							</div>
						</div>
						<!-- Feature 4 -->
						<div
							class="bg-gradient-to-br from-green-100 to-green-200 dark:from-green-900 dark:to-green-800 p-0.5 rounded-lg"
						>
							<div class="bg-surface-0 dark:bg-surface-900 h-full p-6 rounded-lg">
								<div
									class="flex items-center justify-center w-12 h-12 bg-green-200 dark:bg-green-700 rounded-lg mb-4"
								>
									<i class="pi pi-cloud text-2xl text-yellow-700 dark:text-yellow-200"></i>
								</div>
								<h2 class="text-xl font-semibold text-surface-900 dark:text-surface-0 mb-2">
									IOT Sensor Integration
								</h2>
								<p class="text-surface-600 dark:text-surface-200">
									Our product provides thew functionality to integrate with IOT sensors for real-time data. We
									have a wide range of sensors that can be integrated.
								</p>
							</div>
						</div>

						<!-- Feature 5 -->
						<div
							class="bg-gradient-to-br from-purple-100 to-purple-200 dark:from-purple-900 dark:to-purple-800 p-0.5 rounded-lg"
						>
							<div class="bg-surface-0 dark:bg-surface-900 h-full p-6 rounded-lg">
								<div
									class="flex items-center justify-center w-12 h-12 bg-purple-200 dark:bg-purple-700 rounded-lg mb-4"
								>
									<i class="pi pi-microchip-ai text-2xl text-cyan-700 dark:text-cyan-200"></i>
								</div>
								<h2 class="text-xl font-semibold text-surface-900 dark:text-surface-0 mb-2">
									AI Crop Predictions
								</h2>
								<p class="text-surface-600 dark:text-surface-200">
									Our product makes use of our in-house state of the art AI model to predict crop yields. This
									model is is trained and can be used to predict various types of crops.
								</p>
							</div>
						</div>

						<!-- Feature 6 -->
						<div
							class="bg-gradient-to-br from-orange-100 to-orange-200 dark:from-orange-900 dark:to-orange-800 p-0.5 rounded-lg"
						>
							<div class="bg-surface-0 dark:bg-surface-900 h-full p-6 rounded-lg">
								<div
									class="flex items-center justify-center w-12 h-12 bg-orange-200 dark:bg-orange-700 rounded-lg mb-4"
								>
									<i class="pi pi-map-marker text-2xl text-indigo-700 dark:text-indigo-200"></i>
								</div>
								<h2 class="text-xl font-semibold text-surface-900 dark:text-surface-0 mb-2">
									Google Maps Integration
								</h2>
								<p class="text-surface-600 dark:text-surface-200">
									Our product allows for easy integration with Google Maps for easy navigation and location
									access. This improves the user experience, but also the predictions our AI model will make.
								</p>
							</div>
						</div>
					</div>
				</div>
			</div>
			<div id="highlights" class="py-6 px-6 lg:px-20 mx-0 my-12 lg:mx-20">
				<div class="text-center">
					<div class="text-surface-900 dark:text-surface-0 font-normal mb-2 text-5xl">Highlights of our Product</div>
					<span class="text-muted-color text-2xl"></span>
				</div>
				<div class="grid grid-cols-12 gap-4 mt-20 pb-2 md:pb-20">
					<div
						class="flex justify-center col-span-12 lg:col-span-6 bg-purple-200 p-0 order-1 lg:order-none"
						style="border-radius: 8px"
					>
						<img
							src="../assets/mockups/phone/Screenshot 2024-09-10 142053-portrait.png"
							class="w-4/12"
							alt="mockup mobile"
						/>
						<img
							src="../assets/mockups/phone/Screenshot 2024-09-10 142120-portrait.png"
							class="w-4/12"
							alt="mockup mobile"
						/>
						<img
							src="../assets/mockups/phone/Screenshot 2024-09-10 142143-portrait.png"
							class="w-4/12"
							alt="mockup mobile"
						/>
					</div>
					<div class="col-span-12 lg:col-span-6 my-auto flex flex-col lg:items-end text-center lg:text-right gap-4">
						<div
							class="flex items-center justify-center bg-purple-200 self-center lg:self-end"
							style="width: 4.2rem; height: 4.2rem; border-radius: 10px"
						>
							<i class="pi pi-fw pi-mobile !text-4xl text-purple-700"></i>
						</div>
						<div class="leading-none text-surface-900 dark:text-surface-0 text-3xl font-normal">Mobile Friendly</div>
						<span
							class="text-surface-700 dark:text-surface-100 text-xl leading-normal ml-0 md:ml-2"
							style="max-width: 650px"
							>Our product is mobile friendly to ensure anyone anywhere can use our product. Our product is built
							for farmers, therefore mobile friendliness is necessary.</span
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
					<div class="flex justify-end order-1 sm:order-2 col-span-12 lg:col-span-6 bg-yellow-100 p-0">
						<Tabs value="0">
							<TabList>
								<Tab value="0" as="div" class="flex items-center gap-2">
									<span>1</span>
								</Tab>
								<Tab value="1" as="div" class="flex items-center gap-2">
									<span class="font-bold whitespace-nowrap">2</span>
								</Tab>
							</TabList>
							<TabPanels>
								<TabPanel value="0" as="p" class="m-0">
									HI
									<img
										src="../assets/mockups/laptop/Screenshot 2024-09-10 143225-front.png"
										class="w-5/5"
										alt="mockup mobile"
									/>
								</TabPanel>
								<TabPanel value="1" as="p" class="m-0">
									Hello
									<img
										src="../assets/mockups/laptop/Screenshot 2024-09-10 143334-front.png"
										class="w-5/5"
										alt="mockup mobile"
									/>
								</TabPanel>
							</TabPanels>
						</Tabs>
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
		</div>
	</div>
</template>
