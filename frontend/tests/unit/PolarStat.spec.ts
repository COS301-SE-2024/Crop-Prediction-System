// @vitest-environment nuxt
import { mountSuspended } from '@nuxt/test-utils/runtime'
import { it, expect, describe } from 'vitest'
import PolarStat from '~/components/PolarStat.vue'
import Chart from 'primevue/chart'

describe('PolarStat', () => {
	it('can mount the component', async () => {
		const component = await mountSuspended(PolarStat, {
			props: {
				chartInput: [0.5, 0.3, 0.8, 0.4, 0.6],
			},
		})
		expect(component.exists()).toBe(true)
	})

	it('renders the Chart component', async () => {
		const chartInput = [0.5, 0.3, 0.8, 0.4, 0.6]
		const component = await mountSuspended(PolarStat, {
			props: {
				chartInput,
			},
		})

		const chartComponent = component.findComponent(Chart)
		expect(chartComponent.exists()).toBe(true)
	})
})
