// @vitest-environment nuxt
import { mountSuspended } from '@nuxt/test-utils/runtime'
import { it, expect, describe,vi } from 'vitest'
import AccountManage from '~/components/AccountManage.vue'
import { shallowMount,mount } from '@vue/test-utils'
import { resolve } from 'chart.js/helpers'
import auth from '~/middleware/auth'

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
    it('calls the toggle function on click', async () => {
        const email = "test@example.com";
        const wrapper = shallowMount(AccountManage, {
            props: {
                email,
            },
        });

        // Assert email rendering
        expect(wrapper.find('h1').text()).toBe(email);
        const toggle = vi.fn();
        const toggleSpy = vi.spyOn(wrapper.vm, 'toggle').withImplementation(() => toggle(), () => toggle()); 
        // Simulate click on the clickable div
        await wrapper.find('.w-full.flex.flex-row.gap-3.items-center h1').trigger('click');
        // check if the toggle function was called
        expect(toggleSpy).toHaveBeenCalled();
    })
    it('renders the email correctly', async () => {
        const email = "test@exmaple.com";
        const wrapper = shallowMount(AccountManage, {
            props: {
            email,
            },
        });
        // Assert email rendering
        expect(wrapper.find('h1').text()).toBe(email);
    })
    it('test signout function', async () => {
        const wrapper = shallowMount(AccountManage);
        const signOut = vi.fn();
        const signOutSpy = vi.spyOn(wrapper.vm, 'signOut').withImplementation(() => signOut(), () => signOut());
        await wrapper.vm.signOut();
        expect(signOutSpy).toHaveBeenCalled();
    })
})

