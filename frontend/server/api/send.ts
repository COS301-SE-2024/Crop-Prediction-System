import { Resend } from 'resend'

const resend = new Resend(process.env.RESEND_API_KEY)

export default defineEventHandler(async (event) => {
	const to = getQuery(event).to
	const team_id = getQuery(event).team_id

	try {
		const data = await resend.emails.send({
			from: 'Terrabyte <terra@terrabyte.software>',
			to: [`${to}`],
			subject: 'Team Invite',
			html: `<h2>You have been invited!</h2><p>You have been invited to join a team on the terrabyte app. Please use the code below when creating your account.</p><strong>Code: ${team_id}</strong>`,
		})

		return data
	} catch (error) {
		return { error }
	}
})
