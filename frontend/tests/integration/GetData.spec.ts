// @vitest-environment nuxt

import { mountSuspended } from '@nuxt/test-utils/runtime'
import { it, expect, describe, vi } from 'vitest'
import { mount, shallowMount } from '@vue/test-utils'
import AccountManage from '~/components/AccountManage.vue'
import Menu from 'primevue/menu';
import OverlayPanel from 'primevue/overlaypanel';

describe("Getting data", async () => {
    it('Overlay Panel opens on click', async () => {
		const email = 'test@example.com';
    
    // Mount the component
    const wrapper = mount(AccountManage, {
      props: {
        email,
      },
      global: {
        stubs: {
          OverlayPanel: true,
          Avatar: true,
          Menu: true
        }
      }
    });

    // Assert email rendering
    expect(wrapper.find('h1').text()).toBe(email);

    // Spy on the toggle method
    const toggleSpy = vi.spyOn(wrapper.vm, 'toggle');

    // Simulate click on the clickable div
    const clickableDiv = wrapper.find('.w-full.flex.flex-row.gap-3.items-center.cursor-pointer');
    expect(clickableDiv.exists()).toBe(true);
    await clickableDiv.trigger('click');

    // Wait for Vue's update cycle
    await nextTick();

    // Check if the toggle function was called
    expect(toggleSpy).toHaveBeenCalledTimes(1);
	})
  });
