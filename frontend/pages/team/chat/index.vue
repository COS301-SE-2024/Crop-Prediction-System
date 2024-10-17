<template>
	<div v-show="isLoading" class="w-full h-full flex flex-col justify-center items-center gap-2">
		<ProgressSpinner />
		<h2 class="font-bold text-surface-700 dark:text-surface-0 text-xl">Fetching Team Messages</h2>
	</div>

	<div v-if="!isLoading && messages.length === 0" class="w-full h-full flex flex-col justify-center items-center">
		<h2 class="font-bold text-surface-700 dark:text-surface-0 text-xl">No messages found</h2>
	</div>

	<div
		v-if="!isLoading && messages.length > 0"
		ref="scrollableContainer"
		class="w-full flex flex-col gap-2 items-center justify-between rounded-md overflow-y-auto"
	>
		<div v-for="(message, index) in messages" :key="message.id" class="w-full">
			<!-- Show Tag only if this is the first message of the day -->
			<div v-if="shouldShowDateTag(index)" class="w-full gap-2 items-center justify-between flex flex-col">
				<Tag severity="contrast" class="mb-4">{{ formatDate(message.created_at) }}</Tag>
			</div>

			<div class="w-full items-center justify-between flex flex-col">
				<Card :class="checkMessage(message)" style="box-shadow: none; padding: 20px" :key="message" class="rounded-xl">
					<template #title>
						<div class="flex flex-row w-full justify-between items-center">
							<div
								class="flex flex-col md:flex-row gap-1 md:gap-2 items-start md:items-center justify-between mb-2"
							>
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
import { ref, onMounted, watch, nextTick } from 'vue'

const messages = ref([])
const supabase = useSupabaseClient()
const currentUser = ref(null)
const team_id = ref('')
const isLoading = ref(true)

const scrollableContainer = ref(null)

const scrollToLastMessage = () => {
	const lastChild = scrollableContainer.value?.lastElementChild
	setTimeout(() => {
		lastChild?.scrollIntoView({ behavior: 'smooth' })
	}, 500)
}

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
		isLoading.value = false
		nextTick(() => {
			scrollToLastMessage()
		})
	}
}

const fetchMessages = async () => {
	const response = await $fetch(`/api/getTeamMessages?team_id=${team_id.value}`)
	messages.value = response
}

const fetchUser = async () => {
	const user = useSupabaseUser()
	const response = await $fetch(`/api/getUser?user_id=${user.value.id}`)
	currentUser.value = response
}

const unreadMessages = useState('unreadMessages')

const route = useRoute()

watch(route, (newRoute) => {
	if (newRoute.path === '/team/chat') {
		unreadMessages.value = 0
	}
})

onMounted(() => {
	fetchUser()
	getTeamMessages()

	const subscription = supabase
		.channel('public:team_chat')
		.on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'team_chat' }, (payload) => {
			if (payload.new.team_id === team_id.value) {
				messages.value = [...messages.value, payload.new]
				nextTick(() => {
					scrollToLastMessage()
				})
			}
		})
		.subscribe()

	onUnmounted(() => {
		supabase.removeChannel(subscription)
	})
})

const formatDate = (dateString) => {
	const date = new Date(dateString)
	return !isNaN(date) ? date.toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' }) : 'Invalid Date'
}

const formatTime = (dateString) => {
	const date = new Date(dateString)
	return !isNaN(date) ? date.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit', hour12: false }) : 'Invalid Time'
}

const checkMessage = (message) => {
	return currentUser.value.email === message.user_email
		? 'w-[90%] self-end border-2 border-primary-500 rounded-br-none mb-2'
		: 'w-[90%] self-start border-2 border-surface-300 dark:border-surface-600 rounded-bl-none mb-2'
}

const shouldShowDateTag = (index) => {
	if (index === 0) return true
	const currentMessageDate = new Date(messages.value[index].created_at).toDateString()
	const previousMessageDate = new Date(messages.value[index - 1].created_at).toDateString()

	return currentMessageDate !== previousMessageDate
}

definePageMeta({
	layout: 'chat',
	middleware: 'auth',
})
</script>
