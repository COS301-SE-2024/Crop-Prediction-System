<template>
	<div ref="scrollableContainer" class="w-full flex flex-col gap-4 items-center justify-between rounded-md overflow-y-auto">
		<div v-for="(message, index) in messages" :key="message.id" class="w-full">
			<!-- Show Tag only if this is the first message of the day -->
			<div v-if="shouldShowDateTag(index)" class="w-full gap-2 items-center justify-between flex flex-col">
				<Tag severity="contrast" class="mb-2">{{ formatDate(message.created_at) }}</Tag>
			</div>

			<div class="w-full gap-2 items-center justify-between flex flex-col">
				<Card :class="checkMessage(message)" style="box-shadow: none" :key="message">
					<template #title>
						<div class="flex flex-row w-full justify-between items-center">
							<div class="flex flex-col md:flex-row gap-1 md:gap-2 items-start md:items-center justify-between">
								<h2 class="text-lg">{{ message.user_name }}</h2>
								<span class="text-sm text-surface-400 dark:text-surface-0/60 font-normal">
									{{ message.user_email }}
								</span>
							</div>
							<span class="text-sm text-surface-400 dark:text-surface-0/60 font-normal">
								{{ formatTime(message.created_at) }}
							</span>
						</div>
					</template>
					<template #content>
						<p>{{ message.message }}</p>
					</template>
				</Card>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, onMounted, onUpdated, nextTick } from 'vue'

const messages = ref([])
const supabase = useSupabaseClient()
const currentUser = ref(null)
const team_id = ref('')

// You need to declare a DOM ref to access the last message directly
const lastMessage = ref(null) // Ref to track the last message's DOM element

const scrollableContainer = ref(null)

// Scroll to the last message card
const scrollToLastMessage = () => {
	const lastChild = scrollableContainer.value.lastElementChild
	setTimeout(() => {
		lastChild.scrollIntoView({ behavior: 'smooth' })
	}, 500)
}

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
		await fetchMessages()
		// Scroll to the last message after messages are loaded
		nextTick(() => {
			scrollToLastMessage()
		})
	}
}

// Fetch initial messages from team_chat table for the team
const fetchMessages = async () => {
	const response = await $fetch(`/api/getTeamMessages?team_id=${team_id.value}`)
	messages.value = response
}

// Fetch user information
const fetchUser = async () => {
	const user = useSupabaseUser()
	const response = await $fetch(`/api/getUser?user_id=${user.value.id}`)
	currentUser.value = response
	console.log(currentUser.value)
}

// Real-time subscription to new messages
onMounted(() => {
	fetchUser()
	getTeamMessages()

	const subscription = supabase
		.channel('public:team_chat')
		.on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'team_chat' }, (payload) => {
			if (payload.new.team_id === team_id.value) {
				messages.value.push(payload.new)
				// Scroll to the last message when a new message is added
				nextTick(() => {
					scrollToLastMessage()
				})
			}
		})
		.subscribe()

	// Cleanup on unmount
	onUnmounted(() => {
		supabase.removeChannel(subscription)
	})
})

// Helper function to format the date
const formatDate = (dateString) => {
	const date = new Date(dateString)
	return !isNaN(date) ? date.toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' }) : 'Invalid Date'
}

// Helper function to format the time
const formatTime = (dateString) => {
	const date = new Date(dateString)
	return !isNaN(date) ? date.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit', hour12: false }) : 'Invalid Time'
}

// Helper function to style the message based on the user
const checkMessage = (message) => {
	return currentUser.value.email === message.user_email
		? 'w-[90%] self-end border-2 border-primary-500'
		: 'w-[90%] self-start border-2 border-surface-300 dark:border-surface-600'
}

// Function to check if the date tag should be shown (only for the first message of each day)
const shouldShowDateTag = (index) => {
	if (index === 0) return true // Always show for the first message
	const currentMessageDate = new Date(messages.value[index].created_at).toDateString()
	const previousMessageDate = new Date(messages.value[index - 1].created_at).toDateString()

	// Only show the date if it's different from the previous message
	return currentMessageDate !== previousMessageDate
}

definePageMeta({
	layout: 'chat',
})
</script>
