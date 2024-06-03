// @vitest-environment nuxt
import { mountSuspended } from '@nuxt/test-utils/runtime'
import { it, expect, describe } from 'vitest'
import Sidebar from '~/components/Sidebar.vue'

describe('Sidebar', () => {
    it('can mount the component', async () => {
        const component = await mountSuspended(Sidebar)
        expect(component.exists()).toBe(true)
    })
})