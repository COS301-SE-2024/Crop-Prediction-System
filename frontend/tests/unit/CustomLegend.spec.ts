// @vitest-environment nuxt
import { mountSuspended } from '@nuxt/test-utils/runtime'
import { flushPromises } from '@vue/test-utils'
import { describe, it, expect, beforeEach } from 'vitest'
import CustomLegend from '@/components/CustomLegend.vue'

describe('CustomLegend', () => {
	let wrapper: ReturnType<typeof mountSuspended>

	beforeEach(async () => {
		wrapper = await mountSuspended(CustomLegend)
		await flushPromises()
	})

	it('can mount the component', () => {
		expect(wrapper.exists()).toBe(true)
	})

	it('renders legend colors correctly', () => {
		// Check if legend colors are rendered
		const greenColor = wrapper.find('.green-legend-color')
		const orangeColor = wrapper.find('.orange-legend-color')
		const defaultColor = wrapper.find('.legend-color')

		expect(greenColor.exists()).toBe(true)
		expect(orangeColor.exists()).toBe(true)
		expect(defaultColor.exists()).toBe(true)
	})

	it('renders legend labels correctly', () => {
		// Check if legend labels are rendered
		const labels = wrapper.findAll('small')

		expect(labels.length).toBe(2) // We expect two labels
		expect(labels[0].text()).toBe('Suitable')
		expect(labels[1].text()).toBe('Not Suitable')
	})
})
