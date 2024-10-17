// @vitest-environment nuxt
import { mount } from '@vue/test-utils'
import MarketHectareCard from '~/components/MarketHectareCard.vue'
import { describe, it, expect } from 'vitest'

describe('MarketHectareCard.vue', () => {
	it('renders correctly with required props', () => {
		const props = {
			title: 'Test Title',
			footer: 'Test Footer',
		}

		const wrapper = mount(MarketHectareCard, {
			props,
		})

		expect(wrapper.text()).toContain('Test Title')
		expect(wrapper.text()).toContain('Test Footer')
	})

	it('displays the hectare value when it is not zero', () => {
		const props = {
			title: 'Test Title',
			hectare: 5,
			footer: 'Test Footer',
		}

		const wrapper = mount(MarketHectareCard, {
			props,
		})

		expect(wrapper.text()).toContain('5 ha')
	})

	it('displays "N/A" when hectare is zero', () => {
		const props = {
			title: 'Test Title',
			hectare: 0,
			footer: 'Test Footer',
		}

		const wrapper = mount(MarketHectareCard, {
			props,
		})

		expect(wrapper.text()).toContain('N/A')
	})

	it('applies the correct classes for dark mode', () => {
		const props = {
			title: 'Test Title',
			hectare: 5,
			footer: 'Test Footer',
		}

		const wrapper = mount(MarketHectareCard, {
			props,
			global: {
				provide: {
					dark: true, // Simulating dark mode
				},
			},
		})

		expect(wrapper.classes()).toContain('dark:bg-surface-800')
		expect(wrapper.find('span.text-surface-600').classes()).toContain('dark:text-surface-0/60')
	})
})
