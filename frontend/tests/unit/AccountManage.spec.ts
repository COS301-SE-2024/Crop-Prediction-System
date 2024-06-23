// @vitest-environment nuxt
import { mountSuspended } from '@nuxt/test-utils/runtime'
import { it, expect, describe } from 'vitest'
import AccountManage from '~/components/AccountManage.vue'
import { shallowMount,mount } from '@vue/test-utils'
import { vi } from 'vitest'
import { resolve } from 'chart.js/helpers'

describe('AccountManage', () => {
    it('can mount the component', async () => {
        const component = await mountSuspended(AccountManage)
        expect(component.exists()).toBe(true)
    })
    it('renders the div for toggling', async () => {
        const wrapper = await mountSuspended(AccountManage)
        const onCLickToggle = wrapper.find('div[class="w-full flex flex-row gap-3 items-center dark:hover:bg-surface-400/10 hover:bg-surface-100 cursor-pointer p-2 rounded-lg"]')
        expect(onCLickToggle.exists()).toBe(true)
    })
    
})

