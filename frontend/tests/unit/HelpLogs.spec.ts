// @vitest-environment nuxt
import { mountSuspended } from '@nuxt/test-utils/runtime'
import { it, expect, describe } from 'vitest'
import HelpLogs from '~/components/HelpLogs.vue' // Adjust the path as needed

describe('HelpLogs', () => {
	it('can mount the component', async () => {
		const component = await mountSuspended(HelpLogs, {
			props: { activeIndex: 4 }, // Set the prop that activates the component
		})
		expect(component.exists()).toBe(true)
	})

	it('renders the correct title when activeIndex is 4', async () => {
		const wrapper = await mountSuspended(HelpLogs, {
			props: { activeIndex: 4 },
		})
		expect(wrapper.find('h1').text()).toBe('View Logs')
	})

	it('renders the editable fields correctly', async () => {
		const wrapper = await mountSuspended(HelpLogs, {
			props: { activeIndex: 4 },
		})

		const editableFieldsText = /tempmax|tempmin|tempmean|pressure|humidity|dew_point|rain|uvi|soil_moisture|soil_temperature/i
		expect(wrapper.text()).toMatch(editableFieldsText)
	})

	it('renders the non-editable fields correctly', async () => {
		const wrapper = await mountSuspended(HelpLogs, {
			props: { activeIndex: 4 },
		})

		const nonEditableFieldsText = /health|yield|sprayability/i
		expect(wrapper.text()).toMatch(nonEditableFieldsText)
	})

	it('does not render the component when activeIndex is not 4', async () => {
		const wrapper = await mountSuspended(HelpLogs, {
			props: { activeIndex: 1 }, // Using a different activeIndex
		})
		// Check if the wrapper does not contain the text 'View Logs'
		expect(wrapper.text()).not.toContain('View Logs')
	})

	it('renders action buttons', async () => {
		const wrapper = await mountSuspended(HelpLogs, {
			props: { activeIndex: 4 },
		})

		// Check if the button labels are present in the text
		expect(wrapper.text()).toContain('Export')
		expect(wrapper.text()).toContain('Generate Field Report')
	})

	it('renders the success message example', async () => {
		const wrapper = await mountSuspended(HelpLogs, {
			props: { activeIndex: 4 },
		})

		expect(wrapper.text()).toContain('Action completed successfully!')
	})
})
