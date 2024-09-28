<template>
	<Card v-if="activeIndex === 6" class="mt-6 p-5">
		<template #content>
			<div class="w-full flex flex-col justify-between items-start gap-4">
				<h1 class="text-2xl font-semibold">Chat Help</h1>
				<p>
					Welcome to the Chat page! This page allows you to communicate with your team members in real-time. You can
					send messages, view messages from others, and stay connected with your team.
				</p>
				<h2 class="text-xl font-semibold">Chat Layout</h2>
				<p>The chat page is divided into three main sections:</p>
				<ul class="list-disc ml-6">
					<li><strong>Header:</strong> Contains the navigation bar.</li>
					<li><strong>Messages Area:</strong> Displays all the chat messages.</li>
					<li><strong>Message Input:</strong> Allows you to compose and send new messages.</li>
				</ul>
				<h2 class="text-xl font-semibold">Viewing Messages</h2>
				<p>The messages area displays all the messages from your team:</p>
				<div
					class="w-full flex flex-col gap-2 items-center justify-between rounded-md overflow-y-auto border-2 border-surface-500 p-4"
				>
					<!-- Date Tag -->
					<Tag severity="contrast" class="mb-4">16 August 2024</Tag>
					<div class="w-full items-center justify-between flex flex-col">
						<Card
							class="w-[90%] self-start border-2 border-surface-300 dark:border-surface-600 rounded-bl-none mb-2 shadow-none p-5"
						>
							<template #title>
								<div class="flex flex-row w-full justify-between items-center">
									<div
										class="flex flex-col md:flex-row gap-1 md:gap-2 items-start md:items-center justify-between mb-2"
									>
										<h2 class="text-lg">John Doe</h2>
										<span class="text-sm text-surface-400 dark:text-surface-0/60 font-normal">
											john.doe@example.com
										</span>
									</div>
									<span class="text-sm text-surface-400 dark:text-surface-0/60 font-normal"> 14:35 </span>
								</div>
							</template>
							<template #content>
								<p>Hello team! Don't forget about the meeting tomorrow.</p>
							</template>
						</Card>
					</div>
					<div class="w-full items-center justify-between flex flex-col">
						<Card class="w-[90%] self-end border-2 border-primary-500 rounded-br-none mb-2 shadow-none p-5">
							<template #title>
								<div class="flex flex-row w-full justify-between items-center">
									<div
										class="flex flex-col md:flex-row gap-1 md:gap-2 items-start md:items-center justify-between mb-2"
									>
										<h2 class="text-lg">You</h2>
										<span class="text-sm text-surface-400 dark:text-surface-0/60 font-normal">
											your.email@example.com
										</span>
									</div>
									<span class="text-sm text-surface-400 dark:text-surface-0/60 font-normal"> 14:36 </span>
								</div>
							</template>
							<template #content>
								<p>Thanks for the reminder! I'll be there.</p>
							</template>
						</Card>
					</div>
				</div>
				<h2 class="text-xl font-semibold">Sending Messages</h2>
				<p>To send a message to your team:</p>
				<ul class="list-disc ml-6">
					<li>Type your message in the message input area at the bottom of the page.</li>
					<li>
						Press the <kbd>Enter</kbd> key or click the <Button icon="pi pi-send" severity="secondary" text /> button
						to send your message.
					</li>
				</ul>
				<p>Example:</p>
				<div class="w-full h-28 rounded-md flex justify-between items-center gap-2 border-2 border-surface-500 p-5">
					<Textarea placeholder="Type your message..." class="w-full h-full" />
					<Button icon="pi pi-send" severity="secondary" text size="large" />
				</div>
				<h2 class="text-xl font-semibold">Message Features</h2>
				<p>Messages display the following information:</p>
				<ul class="list-disc ml-6">
					<li><strong>Sender's Name:</strong> The name of the team member who sent the message.</li>
					<li><strong>Email Address:</strong> The email address of the sender.</li>
					<li><strong>Time Sent:</strong> The time the message was sent.</li>
					<li><strong>Message Content:</strong> The actual message text.</li>
				</ul>
				<p>Your messages are styled differently for easy identification.</p>
				<h2 class="text-xl font-semibold">Date Tags</h2>
				<p>Date tags appear to separate messages from different days:</p>
				<div
					class="w-full flex flex-col border-surface-500 gap-2 items-center justify-between rounded-md overflow-y-auto border-2 p-5"
				>
					<Tag severity="contrast">17 August 2024</Tag>
				</div>
				<h2 class="text-xl font-semibold">Real-Time Updates</h2>
				<p>
					The chat updates in real-time. New messages from your team members will appear automatically without needing
					to refresh the page.
				</p>
				<h2 class="text-xl font-semibold">Error Handling</h2>
				<p>
					If there's an error sending your message, an error message will appear. Please try again later or check your
					internet connection.
				</p>
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
