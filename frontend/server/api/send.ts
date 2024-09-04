import { Resend } from 'resend'

const resend = new Resend(process.env.RESEND_API_KEY)
const config = useRuntimeConfig()

export default defineEventHandler(async (event) => {
	const to = getQuery(event).to
	const team_id = getQuery(event).team_id
	const appURL = config.public.appBaseUrl

	try {
		const data = await resend.emails.send({
			from: 'Terrabyte <terra@terrabyte.software>',
			to: [`${to}`],
			subject: 'Team Invite',
			html: `<h2>You have been invited!</h2><p>You have been invited to join a team on the terrabyte app. Please use this code below for refernce when you join the team.</p><strong>Code: ${team_id}</strong> <p>Please follow the link below to register your account.</p><a href="${appURL}/join?team_id=${team_id}">${appURL}/join?team_id=${team_id}</a>`,
		})

		return data
	} catch (error) {
		return { error }
	}
})
