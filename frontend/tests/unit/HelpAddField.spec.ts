// @vitest-environment nuxt
import { mount } from '@vue/test-utils'
import { it, expect, describe, beforeEach, vi } from 'vitest'
import HelpAddField from '~/components/HelpAddField.vue'

// Mocking required components
vi.mock('primevue/card', () => ({
	default: {
		name: 'Card',
		template: '<div><slot name="content" /></div>',
		props: ['class'],
	},
}))

vi.mock('primevue/inputtext', () => ({
	default: {
		name: 'InputText',
		template: '<input />',
		props: ['placeholder', 'class'],
	},
}))

vi.mock('primevue/dropdown', () => ({
	default: {
		name: 'Dropdown',
		template: '<select><slot /></select>',
		props: ['options', 'optionLabel', 'placeholder', 'class', 'showClear'],
	},
}))

vi.mock('primevue/button', () => ({
	default: {
		name: 'Button',
		template: '<button><slot /></button>',
		props: ['label', 'icon', 'size', 'severity', 'outlined'],
	},
}))

describe('HelpAddField', () => {
	let wrapper

	beforeEach(() => {
		wrapper = mount(HelpAddField, {
			props: { activeIndex: 3 },
		})
	})

	it('mounts the component', () => {
		expect(wrapper.exists()).toBe(true)
	})

	it('renders the main heading', () => {
		const heading = wrapper.find('h1')
		expect(heading.exists()).toBe(true)
		expect(heading.text()).toBe('Add Field Help')
	})

	it('renders the "Field Info" section', () => {
		const sectionHeading = wrapper.findAll('h2').at(0)
		expect(sectionHeading.text()).toBe('1. Field Info')
		expect(wrapper.text()).toContain('In this step, you provide basic information about your new field:')
	})

	it('renders the "Field Map" section', () => {
		const sectionHeading = wrapper.findAll('h2').at(1)
		expect(sectionHeading.text()).toBe('2. Field Map')
		expect(wrapper.text()).toContain('In this step, you draw the boundaries of your field on the map:')
	})

	it('renders the "Confirm" section', () => {
		const sectionHeading = wrapper.findAll('h2').at(2)
		expect(sectionHeading.text()).toBe('3. Confirm')
		expect(wrapper.text()).toContain('In the final step, review the information you have entered:')
	})

	it('renders the "Loading Indicators" section', () => {
		const sectionHeading = wrapper.findAll('h2').at(4)
		expect(sectionHeading.text()).toBe('Loading Indicators')
		expect(wrapper.text()).toContain('When saving the field, a loading indicator will appear')
	})

	it('renders the "Success Message" section', () => {
		const sectionHeading = wrapper.findAll('h2').at(5)
		expect(sectionHeading.text()).toBe('Success Message')
		expect(wrapper.text()).toContain('Field saved successfully!')
	})
})
