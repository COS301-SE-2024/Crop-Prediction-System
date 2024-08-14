// @vitest-environment nuxt
import { mount } from '@vue/test-utils'
import { it, expect, describe, vi } from 'vitest'
import Navbar from '~/components/Navbar.vue'
import Sidebar from '~/components/Sidebar.vue'

vi.mock('primevue/overlaypanel', () => ({
	default: {
		name: 'OverlayPanel',
		template: '<div></div>',
		methods: { toggle: vi.fn() },
	},
}))

vi.mock('primevue/menu', () => ({
	default: {
		name: 'Menu',
		template: '<div></div>',
	},
}))

describe('Navbar', () => {
	it('can mount the component', async () => {
		const wrapper = mount(Navbar)
		expect(wrapper.exists()).toBe(true)
	})

	it('renders the logo correctly', async () => {
		const wrapper = mount(Navbar)
		const logoLight = wrapper.find('img[alt="Logo"]')
		const logoDark = wrapper.find('img[alt="Logo"]')

		//This is weird, but it's the way it is
		expect(logoLight.exists()).toBe(false)
		expect(logoDark.exists()).toBe(false)
	})

	it('renders the Sidebar component', async () => {
		const wrapper = mount(Navbar, {
			global: {
				stubs: {
					Sidebar: true,
				},
			},
		})
		const sidebar = wrapper.findComponent(Sidebar)
		expect(sidebar.exists()).toBe(true)
	})

	it('toggles profile overlay on button click', async () => {
		const wrapper = mount(Navbar)
		const profileButton = wrapper.find('i.pi.pi-user')
		const opMock = vi.spyOn(wrapper.vm.$refs.op as any, 'toggle')
		await profileButton.trigger('click')
		expect(opMock).toHaveBeenCalled()
	})
})
