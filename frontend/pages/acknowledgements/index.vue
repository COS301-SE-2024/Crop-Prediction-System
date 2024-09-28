<template>
	<div class="mt-6 p-5">
		<div class="w-full flex flex-col justify-between items-start gap-4 text-surface-700 dark:text-surface-0">
			<h1 class="text-2xl font-semibold">Acknowledgements</h1>
			<p class="text-surface-600 dark:text-surface-0/60">
				We would like to express our gratitude to the following organizations and services for providing valuable data and
				resources that made this application possible:
			</p>

			<h2 class="text-xl font-semibold">Data Sources and Services</h2>
			<ul class="list-disc ml-6">
				<li class="mb-4">
					<h3 class="text-lg font-semibold">OpenWeather API</h3>
					<p class="text-surface-600 dark:text-surface-0/60">
						The OpenWeather API provides current weather data, forecasts, and historical data for any location. We
						utilize this service to gather accurate and up-to-date weather information for our models.
					</p>
					<a href="https://openweathermap.org/" target="_blank" class="text-blue-500 hover:underline">
						https://openweathermap.org/
					</a>
				</li>
				<li class="mb-4">
					<h3 class="text-lg font-semibold">Grain SA</h3>
					<p class="text-surface-600 dark:text-surface-0/60">
						Grain SA is a non-profit organization that represents the interests of grain producers in South Africa. We
						use market data from Grain SA to enhance our revenue dashboard.
					</p>
					<a href="https://www.grainsa.co.za/" target="_blank" class="text-blue-500 hover:underline">
						https://www.grainsa.co.za/
					</a>
				</li>
				<li class="mb-4">
					<h3 class="text-lg font-semibold">South African Grain Information Service (SAGIS)</h3>
					<p class="text-surface-600 dark:text-surface-0/60">
						SAGIS provides comprehensive grain industry information. We leverage their data to ensure our revenue
						insights are accurate and informative.
					</p>
					<a href="https://www.sagis.org.za/" target="_blank" class="text-blue-500 hover:underline">
						https://www.sagis.org.za/
					</a>
				</li>
			</ul>

			<h2 class="text-xl font-semibold">Licenses and Attributions</h2>
			<p class="text-surface-600 dark:text-surface-0/60">
				We acknowledge that some data and services require attribution under their licenses. We have ensured that all such
				requirements are met in accordance with the terms provided by each service.
			</p>
		</div>
	</div>
</template>
