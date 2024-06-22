// @vitest-environment nuxt
import { mountSuspended } from '@nuxt/test-utils/runtime'
import { it, expect, describe } from 'vitest'
import AccountManage from '~/components/AccountManage.vue'
import { shallowMount } from '@vue/test-utils'
import { vi } from 'vitest'

describe('AccountManage', () => {
    it('can mount the component', async () => {
        const component = await mountSuspended(AccountManage)
        expect(component.exists()).toBe(true)
    })
})

