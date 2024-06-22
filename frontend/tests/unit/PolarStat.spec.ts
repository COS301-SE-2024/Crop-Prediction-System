// @vitest-environment nuxt
import { mountSuspended } from '@nuxt/test-utils/runtime'
import { it, expect, describe } from 'vitest'
import PolarStat from '~/components/PolarStat.vue'

describe('PolarStat', () => {
	it('can mount the component', async () => {
		const component = await mountSuspended(PolarStat)
		expect(component.exists()).toBe(true)
	})
})
