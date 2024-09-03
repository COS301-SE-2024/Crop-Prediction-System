// @vitest-environment nuxt

import { mountSuspended } from '@nuxt/test-utils/runtime'
import { it, expect, describe, vi } from 'vitest'
import { mount, shallowMount } from '@vue/test-utils'
import SidebarVue from '~/components/Sidebar.vue'
import { nextTick } from 'vue';


// check that if the button is clicked, the sidebar is toggled
describe("Sidebar", async () => {
    it('Sidebar opens on click', async () => {
        const wrapper = await mountSuspended(SidebarVue);

        const button = wrapper.find('[data-test="filter-button"]');
        expect(button.exists()).toBe(true);

        const sidebar = wrapper.findComponent({ name: 'Sidebar' });
        expect(sidebar.exists()).toBe(true);
        let visible = wrapper.vm.getVisible();
        expect(visible).toBe(false);

        await button.trigger('click');
        visible = wrapper.vm.getVisible();
        expect(visible).toBe(true);
    });
});
