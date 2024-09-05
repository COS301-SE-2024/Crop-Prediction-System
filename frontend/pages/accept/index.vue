<script setup lang="ts">
import Card from 'primevue/card'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'

const team_id = '1111-2222-3333-4444' // Get team_id from the query params

// TODO: add role

// async function joinTeam() {
// 	try {
// 		// Make a POST request to the server API to add the user to the team
// 		const response = await $fetch('/api/addToTeam', {
// 			method: 'POST',
// 			body: {
// 				team_id: team_id,
// 				user_id: newUserID.value,
// 				role: role,
// 			},
// 		})
//
// 		if (response?.error) {
// 			throw new Error(response.error)
// 		}
//
// 		// Handle success response
// 		successMsg.value = 'You have successfully joined the team!'
// 	} catch (error: any) {
// 		// Handle any errors that occurred during the API call
// 		errorMsg.value = error.message || 'Failed to join the team.'
// 	} finally {
// 		step.value = 3
// 	}
// }

definePageMeta({
	middleware: 'auth',
})
</script>

<template>
	<div class="w-full h-screen flex flex-col justify-center items-center p-4 overflow-auto">
		<div class="w-full max-w-[450px] px-4 overflow-auto">
			<!-- Step 2: Team Confirmation -->
			<Card class="w-full border border-surface-border">
				<template #title>
					<h1 class="font-medium">Team Confirmation</h1>
				</template>
				<template #subtitle>
					<p>Double-check the code sent to your email and ensure it matches the one below.</p>
				</template>
				<template #content>
					<div class="flex flex-col gap-3">
						<!-- Team Code -->
						<div class="flex flex-col gap-2 items-start">
							<h3 class="font-semibold">Team Code</h3>
							<InputText id="teamCode" type="text" class="w-full" v-model="team_id" readonly />
						</div>
					</div>
				</template>
				<template #footer>
					<Button class="w-full" label="Join Team" @click="joinTeam" />
				</template>
			</Card>
		</div>
	</div>
</template>
