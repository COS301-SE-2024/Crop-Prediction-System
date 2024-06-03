// @vitest-environment nuxt
import { mountSuspended } from '@nuxt/test-utils/runtime'
import { it, expect, describe } from 'vitest'
import NavigationMenu from '~/components/NavigationMenu.vue'

describe('NavigationMenu', () => {
    it('can mount the component', async () => {
        const component = await mountSuspended(NavigationMenu)
        expect(component.exists()).toBe(true)
    })
})