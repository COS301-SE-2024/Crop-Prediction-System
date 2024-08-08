<template>
	<div class="flex flex-col gap-2">
		<div class="flex flex-row justify-center items-center">
			<small class="mr-3">Suitable</small>
			<div class="green-legend-color"></div>
			<div class="orange-legend-color"></div>
			<div class="legend-color"></div>
			<small class="ml-3">Not Suitable</small>
		</div>
	</div>
</template>

<script setup></script>

<style scoped>
.green-legend-color {
	display: inline-block;
	width: 60px;
	height: 12px;
	background-color: rgba(76, 175, 80, 0.4);
}

.orange-legend-color {
	display: inline-block;
	width: 60px;
	height: 12px;
	background-color: rgba(255, 205, 86, 0.4);
}

.legend-color {
	display: inline-block;
	width: 60px;
	height: 12px;
	background-color: rgba(255, 99, 132, 0.4);
}
</style>
