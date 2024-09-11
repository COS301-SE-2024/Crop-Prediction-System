<template>
	<div class="flex flex-col h-full p-4 bg-gray-100">
		<!-- Messages display area -->
		<div class="flex-grow overflow-y-auto space-y-4">
			<div v-for="message in messages" :key="message.id" class="p-3 bg-white shadow rounded-md">
				<div class="flex items-center justify-between mb-1 w-full">
					<div class="flex flex-col sm:flex-row justify-between items-start gap-1">
						<span class="text-sm">{{ message.user_name }}</span>
						<span class="text-sm">({{ message.user_email }})</span>
					</div>
					<span class="text-xs text-gray-400">{{ new Date(message.created_at).toLocaleString() }}</span>
				</div>
				<p class="text-gray-700 mt-4">{{ message.message }}</p>
			</div>
		</div>
	</div>
</template>

<script setup>
const messages = ref([])
const supabase = useSupabaseClient()

const team_id = ref('')

// TODO: Add sending messages functionality (POST call to API backend)
// TODO: Format messages with time and date above the message card
// TODO: Adjust not current user messages to be on left and current user messages to be on the right

// Fetching Team ID first
async function getTeamMessages() {
	try {
		const currentUser = useSupabaseUser()
		const teamID = await $fetch('/api/getTeamID', {
			params: { userid: currentUser?.value?.id },
		})
		team_id.value = teamID.team_id
	} catch (error) {
		console.error('Error fetching team details:', error)
	} finally {
		fetchMessages()
	}
}

// Fetch initial messages from team_chat table for the team
// TODO: Fetch team messages from backend API
const fetchMessages = async () => {
	const { data, error } = await supabase
		.from('team_chat')
		.select('*')
		.eq('team_id', team_id.value)
		.order('created_at', { ascending: true })
	messages.value = data
}

// Real-time subscription to new messages
onMounted(() => {
	getTeamMessages()

	const subscription = supabase
		.channel('public:team_chat')
		.on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'team_chat' }, (payload) => {
			if (payload.new.team_id === team_id.value) {
				messages.value.push(payload.new)
			}
		})
		.subscribe()

	// Cleanup on unmount
	onUnmounted(() => {
		supabase.removeChannel(subscription)
	})
})
</script>
