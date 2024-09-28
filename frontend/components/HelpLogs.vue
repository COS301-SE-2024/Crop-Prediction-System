<template>
	<Card v-if="activeIndex === 4" class="mt-6 p-5">
		<template #content>
			<div class="w-full flex flex-col justify-between items-start gap-4">
				<h1 class="text-2xl font-semibold">View Logs</h1>
				<p>
					Welcome to the View Logs page! This page allows you to view and manage your field data entries. You can edit
					certain fields directly in the table and perform actions like exporting data or printing charts.
				</p>

				<h2 class="text-xl font-semibold">Data Table</h2>
				<p>The table below displays data entries for your field. You can edit certain fields directly in the table.</p>
				<ul class="list-disc ml-6">
					<li>
						<strong>Editable Fields:</strong> <code>tempmax</code>, <code>tempmin</code>, <code>tempmean</code>,
						<code>pressure</code>, <code>humidity</code>, <code>dew_point</code>, <code>rain</code>, <code>uvi</code>,
						<code>soil_moisture</code>, <code>soil_temperature</code>.
					</li>
					<li>
						<strong>Non-Editable Fields:</strong> <code>health</code>, <code>yield</code>, <code>sprayability</code>.
					</li>
				</ul>
				<p>
					To edit a cell, click on it, make your changes, and press <kbd>Enter</kbd> to save or <kbd>Esc</kbd> to
					cancel.
				</p>

				<h2 class="text-xl font-semibold">Actions</h2>
				<p>You can perform the following actions on the selected data entries:</p>
				<ul class="list-disc ml-6">
					<li><strong>Export Selected to CSV:</strong> Exports the selected rows to a CSV file.</li>
					<li>
						<strong>Print Charts:</strong> Generates charts for the selected data and opens the print dialog. The
						charts are only shown when exporting.
					</li>
				</ul>
				<div class="flex gap-2 mt-4">
					<Button label="Export" icon="pi pi-external-link" severity="secondary" />
					<Button label="Generate Field Report" icon="pi pi-chart-line" />
				</div>

				<h2 class="text-xl font-semibold">Success Message</h2>
				<p>After performing an action, a success message will appear confirming that the action has been completed.</p>
				<p>Example:</p>
				<div class="flex items-center gap-2">
					<i class="pi pi-check-circle text-green-500"></i>
					<span class="text-green-500">Action completed successfully!</span>
				</div>
			</div>
		</template>
	</Card>
</template>

<script setup>
const props = defineProps({
	activeIndex: {
		type: Number,
		default: 0,
	},
})
</script>
