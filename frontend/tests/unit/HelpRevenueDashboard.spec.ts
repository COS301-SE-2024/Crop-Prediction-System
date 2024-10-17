// @vitest-environment nuxt
import { mount } from '@vue/test-utils'
import { it, expect, describe, beforeEach } from 'vitest'
import HelpRevenueDashboard from '~/components/HelpRevenueDashboard.vue'
import { vi } from 'vitest'

// Mocking required components
vi.mock('primevue/card', () => ({
	default: {
		name: 'Card',
		template: '<div><slot name="content" /></div>',
		props: ['class'],
	},
}))

vi.mock('primevue/dropdown', () => ({
	default: {
		name: 'Dropdown',
		template: '<select><slot /></select>',
		props: ['options', 'optionLabel', 'placeholder', 'class'],
	},
}))

vi.mock('primevue/chart', () => ({
	default: {
		name: 'Chart',
		template: '<div><slot /></div>',
		props: ['type', 'data', 'options', 'class'],
	},
}))

vi.mock('primevue/progressspinner', () => ({
	default: {
		name: 'ProgressSpinner',
		template: '<div>Loading...</div>',
	},
}))

describe('HelpRevenueDashboard', () => {
	let wrapper

	beforeEach(() => {
		wrapper = mount(HelpRevenueDashboard, {
			props: { activeIndex: 1 },
		})
	})

	it('mounts the component', () => {
		expect(wrapper.exists()).toBe(true)
	})

	it('renders the main heading', () => {
		const heading = wrapper.find('h1')
		expect(heading.exists()).toBe(true)
		expect(heading.text()).toBe('Revenue Dashboard Help')
	})

	it('renders the "Selecting a Crop" section', () => {
		const sectionHeading = wrapper.findAll('h2').at(0)
		expect(sectionHeading.text()).toBe('1. Selecting a Crop')
		expect(wrapper.text()).toContain("Use the dropdown at the top of the dashboard to select the crop you're interested in.")
	})

	it('renders the "Viewing Hectare and Yield Data" section', () => {
		const sectionHeading = wrapper.findAll('h2').at(1)
		expect(sectionHeading.text()).toBe('2. Viewing Hectare and Yield Data')
		expect(wrapper.text()).toContain('After selecting a crop, two cards will display key information:')
	})

	//   it('renders the "Revenue Chart" section', () => {
	//     const sectionHeading = wrapper.findAll('h2').at(2)
	//     expect(sectionHeading.text()).toBe('3. Revenue Chart')
	//     expect(wrapper.text()).toContain('If data is available, a chart will display the predicted revenue and past average predicted revenue.')
	//   })

	it('renders the "Interacting with the Chart" section', () => {
		const sectionHeading = wrapper.findAll('h2').at(3)
		expect(sectionHeading.text()).toBe('4. Interacting with the Chart')
		expect(wrapper.text()).toContain(
			'You can interact with the chart by toggling datasets in the legend or hovering over data points for more details.',
		)
	})

	it('renders the "No Fields Message" section', () => {
		const sectionHeading = wrapper.findAll('h2').at(4)
		expect(sectionHeading.text()).toBe('5. No Fields Message')
		expect(wrapper.text()).toContain('If you have no registered fields for the selected crop, a message will inform you:')
	})

	it('renders the "Loading Indicator" section', () => {
		const sectionHeading = wrapper.findAll('h2').at(5)
		expect(sectionHeading.text()).toBe('6. Loading Indicator')
		expect(wrapper.text()).toContain('While the market data is being fetched, a loading spinner and message will appear.')
	})
})
