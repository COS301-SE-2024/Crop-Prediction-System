<script setup lang="ts">
import Button from 'primevue/button'
import Chart from 'primevue/chart'
import { ref, onMounted } from 'vue'

onMounted(() => {
	chartData.value = setChartData()
	chartOptions.value = setChartOptions()
})

const chartData = ref()
const chartOptions = ref()

const setChartData = () => {
	const documentStyle = getComputedStyle(document.documentElement)

	return {
		labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
		datasets: [
			{
				label: 'First Dataset',
				data: [65, 59, 80, 81, 56, 55, 40],
				fill: false,
				tension: 0.4,
				borderColor: documentStyle.getPropertyValue('--p-cyan-500'),
			},
			{
				label: 'Second Dataset',
				data: [28, 48, 40, 19, 86, 27, 90],
				fill: false,
				borderDash: [5, 5],
				tension: 0.4,
				borderColor: documentStyle.getPropertyValue('--p-orange-500'),
			},
			{
				label: 'Third Dataset',
				data: [12, 51, 62, 33, 21, 62, 45],
				fill: true,
				borderColor: documentStyle.getPropertyValue('--p-gray-500'),
				tension: 0.4,
				backgroundColor: 'rgba(107, 114, 128, 0.2)',
			},
		],
	}
}
const setChartOptions = () => {
	const documentStyle = getComputedStyle(document.documentElement)
	const textColor = documentStyle.getPropertyValue('--p-text-color')
	const textColorSecondary = documentStyle.getPropertyValue('--p-text-muted-color')
	const surfaceBorder = documentStyle.getPropertyValue('--p-content-border-color')

	return {
		maintainAspectRatio: false,
		aspectRatio: 0.6,
		plugins: {
			legend: {
				labels: {
					color: textColor,
				},
			},
		},
		scales: {
			x: {
				ticks: {
					color: textColorSecondary,
				},
				grid: {
					color: surfaceBorder,
				},
			},
			y: {
				ticks: {
					color: textColorSecondary,
				},
				grid: {
					color: surfaceBorder,
				},
			},
		},
	}
}
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
				<div class="mx-6 md:mx-20 mt-0 md:mt-6">
					<h1 class="text-6xl font-bold text-gray-900 leading-tight">
						<span class="font-light block">Eu sem integer</span>eget magna fermentum
					</h1>
					<p class="font-normal text-2xl leading-normal md:mt-4 text-gray-700">
						Sed blandit libero volutpat sed cras. Fames ac turpis egestas integer. Placerat in egestas erat...
					</p>
					<Button
						label="Get Started"
						as="router-link"
						to="/"
						rounded
						class="bg-surface-200 text-surface-900 !text-xl mt-8 !px-4"
					></Button>
				</div>
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
									<i class="pi pi-thumbs-up text-2xl text-yellow-700 dark:text-yellow-200"></i>
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
									<i class="pi pi-lock text-2xl text-indigo-700 dark:text-indigo-200"></i>
								</div>
								<h2 class="text-xl font-semibold text-surface-900 dark:text-surface-0 mb-2">Fast and Secure</h2>
								<p class="text-surface-600 dark:text-surface-200">
									One of our main priorities is to ensure that our product is fast and secure. We have
									implemented a wide range of security features to ensure that your data is safe, and that speed
									will not be a concern.
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
									<i class="pi pi-cloud text-2xl text-green-700 dark:text-green-200"></i>
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
									<i class="pi pi-microchip-ai text-2xl text-purple-700 dark:text-purple-200"></i>
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
									<i class="pi pi-map-marker text-2xl text-orange-700 dark:text-orange-200"></i>
								</div>
								<h2 class="text-xl font-semibold text-surface-900 dark:text-surface-0 mb-2">
									Google Maps Integration
								</h2>
								<p class="text-surface-600 dark:text-surface-200">
									Our product integrates with Google Maps for easy navigation and location access. This improves
									the user experience, but also the predictions our AI model will make.
								</p>
							</div>
						</div>
						<!-- Feature 7 -->
						<div
							class="bg-gradient-to-br from-emerald-100 to-emerald-200 dark:from-emerald-900 dark:to-emerald-800 p-0.5 rounded-lg"
						>
							<div class="bg-surface-0 dark:bg-surface-900 h-full p-6 rounded-lg">
								<div
									class="flex items-center justify-center w-12 h-12 bg-emerald-200 dark:bg-emerald-700 rounded-lg mb-4"
								>
									<i class="pi pi-chart-bar text-2xl text-emerald-700 dark:text-emerald-200"></i>
								</div>
								<h2 class="text-xl font-semibold text-surface-900 dark:text-surface-0 mb-2">
									Data Visualisation
								</h2>
								<p class="text-surface-600 dark:text-surface-200">
									Our product features a wide range of graphs and charts, each displaying crucial data received
									from the AI model in order to help our users better their Crop's health and potential yield.
								</p>
							</div>
						</div>
						<!-- Feature 8 -->
						<div
							class="bg-gradient-to-br from-slate-200 to-slate-300 dark:from-slate-800 dark:to-slate-700 p-0.5 rounded-lg"
						>
							<div class="bg-surface-0 dark:bg-surface-900 h-full p-6 rounded-lg">
								<div
									class="flex items-center justify-center w-12 h-12 bg-slate-200 dark:bg-slate-700 rounded-lg mb-4"
								>
									<i class="pi pi-mobile text-2xl text-slate-700 dark:text-slate-200"></i>
								</div>
								<h2 class="text-xl font-semibold text-surface-900 dark:text-surface-0 mb-2">Mobile Friendly</h2>
								<p class="text-surface-600 dark:text-surface-200">
									Our product is mobile friendly to ensure anyone anywhere can use our product. Our product is
									built for farmers, therefore mobile friendliness is key.
								</p>
							</div>
						</div>
						<!-- Feature 9 -->
						<div
							class="bg-gradient-to-br from-rose-100 to-rose-200 dark:from-rose-900 dark:to-rose-800 p-0.5 rounded-lg"
						>
							<div class="bg-surface-0 dark:bg-surface-900 h-full p-6 rounded-lg">
								<div
									class="flex items-center justify-center w-12 h-12 bg-rose-200 dark:bg-rose-700 rounded-lg mb-4"
								>
									<i class="pi pi-users text-2xl text-rose-700 dark:text-rose-200"></i>
								</div>
								<h2 class="text-xl font-semibold text-surface-900 dark:text-surface-0 mb-2">Team Availability</h2>
								<p class="text-surface-600 dark:text-surface-200">
									We added teams to our product to allow farmers and their helpers to have access to the same
									set of fields and crops. This allows for better collaboration and communication.
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
						class="flex justify-center col-span-12 lg:col-span-6 bg-blue-200 p-0 order-1 lg:order-none"
						style="border-radius: 8px"
					>
						<img
							src="../assets/mockups/phone/Screenshot 2024-09-10 142053-portrait.png"
							class="w-1/3"
							alt="mockup mobile"
						/>
						<img
							src="../assets/mockups/phone/Screenshot 2024-09-10 142120-portrait.png"
							class="w-1/3"
							alt="mockup mobile"
						/>
						<img
							src="../assets/mockups/phone/Screenshot 2024-09-10 142143-portrait.png"
							class="w-1/3"
							alt="mockup mobile"
						/>
					</div>
					<div class="col-span-12 lg:col-span-6 my-auto flex flex-col lg:items-end text-center lg:text-right gap-4">
						<div
							class="flex items-center justify-center bg-blue-200 self-center lg:self-end"
							style="width: 4.2rem; height: 4.2rem; border-radius: 10px"
						>
							<i class="pi pi-map-marker !text-4xl text-blue-700"></i>
						</div>
						<div class="leading-none text-surface-900 dark:text-surface-0 text-3xl font-normal">
							Map Functionality
						</div>
						<span
							class="text-surface-700 dark:text-surface-100 text-xl leading-normal ml-0 md:ml-2"
							style="max-width: 550px"
							>When a user is ready to add a field to the app, they simply search for the field's location in the
							search bar, and then just enter the coordinates manually on the map. We implemented it this way to
							ensure accurate locations and make the whole system easier to use for our clients.
						</span>
					</div>
				</div>
				<div class="grid grid-cols-12 gap-4 my-20 pt-2 md:pt-20">
					<div class="col-span-12 lg:col-span-6 my-auto flex flex-col text-center lg:text-left lg:items-start gap-4">
						<div
							class="flex items-center justify-center bg-yellow-200 self-center lg:self-start"
							style="width: 4.2rem; height: 4.2rem; border-radius: 10px"
						>
							<i class="pi pi-chart-line !text-3xl text-yellow-700"></i>
						</div>
						<div class="leading-none text-surface-900 dark:text-surface-0 text-3xl font-normal">
							Charts and Graphs
						</div>
						<span
							class="text-surface-700 dark:text-surface-100 text-xl leading-normal mr-0 md:mr-2"
							style="max-width: 550px"
							>Our product features a wide range of graphs and charts, each displaying crucial data received from
							the AI model in order to help our users better their Crop's health and potential yield.
						</span>
					</div>
					<div
						class="flex justify-center order-1 sm:order-2 col-span-12 lg:col-span-6 bg-yellow-100 p-0"
						style="border-radius: 8px"
					>
						<div class="grid grid-cols-1 place-content-center text-surface-700">
							<div>
								<Chart type="line" :data="chartData" :options="chartOptions" class="h-[20rem] w-[30rem]" />
							</div>
							<div class="justify-self-center ml-2">text</div>
						</div>
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
						class="flex justify-center col-span-12 lg:col-span-6 bg-blue-100 p-0 order-1 lg:order-none"
						style="border-radius: 8px"
					>
						<img src="" class="w-11/12" alt="mockup mobile" />
					</div>
					<div class="col-span-12 lg:col-span-6 my-auto flex flex-col lg:items-end text-center lg:text-right gap-4">
						<div
							class="flex items-center justify-center bg-blue-200 self-center lg:self-end"
							style="width: 4.2rem; height: 4.2rem; border-radius: 10px"
						>
							<i class="pi pi-fw pi-mobile !text-4xl text-blue-700"></i>
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
