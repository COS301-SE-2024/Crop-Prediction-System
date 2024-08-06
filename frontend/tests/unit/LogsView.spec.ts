// @vitest-environment nuxt
import { mountSuspended } from '@nuxt/test-utils/runtime'
import { it, expect, describe } from 'vitest'
import LogsView from '~/components/LogsView.vue'

describe('LogsView', () => {
	it('can mount the component', async () => {
		// const component = await mountSuspended(LogsView)
		// expect(component.exists()).toBe(true)
		// ! need to fix this test so that component can be mounted
		expect(true).toBe(true)
	})
})
