// @vitest-environment nuxt

import { mountSuspended } from '@nuxt/test-utils/runtime'
import { it, expect, describe, vi } from 'vitest'
import SidebarVue from '~/components/Sidebar.vue'
import { nextTick } from 'vue'

// Mock the PrimeVue Sidebar component
vi.mock('primevue/sidebar', () => ({
    default: {
        name: 'Sidebar',
        template: '<div></div>', // provide a simple template
    }
}));

// Check that if the button is clicked, the sidebar is toggled
describe("Sidebar", async () => {
    it('Sidebar opens on click', async () => {
        const wrapper = await mountSuspended(SidebarVue);

        // Find the button
        const button = wrapper.find('[aria-label="Filter"]');
        expect(button.exists()).toBe(true);

        // Check if the Sidebar component is present
        const sidebar = wrapper.findComponent({ name: 'Sidebar' });
        expect(sidebar.exists()).toBe(true);

        // Trigger button click
        await button.trigger('click');

        // Wait for the DOM update
        await nextTick();

        // Check visibility after the button click
        expect(wrapper.vm.visible.value).toBe(true);
    });
});
