// @vitest-environment nuxt
import { mountSuspended } from '@nuxt/test-utils/runtime'
import { it, expect, describe } from 'vitest'
import StatPanel from '~/components/StatPanel.vue'

describe('StatPanel', () => {
    it('can mount the component', async () => {
        const component = await mountSuspended(StatPanel)
        expect(component.exists()).toBe(true)
    })
})