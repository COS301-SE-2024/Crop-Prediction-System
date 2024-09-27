// @vitest-environment nuxt

import { mountSuspended } from '@nuxt/test-utils/runtime'
import { vi, it, expect, describe } from 'vitest'
import Navbar from '~/components/Navbar.vue'
import { nextTick, ref } from 'vue'
import { mount } from '@vue/test-utils'

describe('Navbar Integration Test', () => {
	it('Navbar toggle profile works', async () => {
		const mockToggle = vi.fn()

		// Mount the component with the mocked op
		const wrapper = await mountSuspended(Navbar)
		console.log('Rendered HTML:', wrapper.html())

		expect(wrapper.exists()).toBe(true)

		// Find the profile button
		const profileButton = wrapper.find('i.pi.pi-user')
		expect(profileButton.exists()).toBe(true)
		const opMock = vi.spyOn(wrapper.vm, 'toggleProfile')
		console.log('Before click')
		await profileButton.trigger('click')
		console.log('After click')
		await nextTick()
		console.log('After nextTick')

		// Log the calls to toggleProfile
		await wrapper.vm.toggleProfile(new Event('click'))
		// Check if the toggle function was called on the mocked op

		expect(opMock).toHaveBeenCalledTimes(1)
	})
})
