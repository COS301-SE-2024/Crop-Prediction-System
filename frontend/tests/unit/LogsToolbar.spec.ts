// @vitest-environment nuxt
import { mountSuspended } from '@nuxt/test-utils/runtime'
import { it, expect, describe } from 'vitest'
import LogsToolbar from '~/components/LogsToolbar.vue'

describe('LogsToolbar', () => {
    it('can mount the component', async () => {
        const component = await mountSuspended(LogsToolbar)
        expect(component.exists()).toBe(true)
    })
})