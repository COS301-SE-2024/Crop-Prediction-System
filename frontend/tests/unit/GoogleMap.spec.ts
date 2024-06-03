// @vitest-environment nuxt
import { mountSuspended } from '@nuxt/test-utils/runtime'
import { it, expect, describe } from 'vitest'
import GoogleMap from '~/components/GoogleMap.vue'

describe('GoogleMap', () => {
    it('can mount the component', async () => {
        const component = await mountSuspended(GoogleMap)
        expect(component.exists()).toBe(true)
    })
})