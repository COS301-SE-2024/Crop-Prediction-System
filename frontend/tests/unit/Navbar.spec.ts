// @vitest-environment nuxt
import { mountSuspended } from '@nuxt/test-utils/runtime'
import { it, expect, describe } from 'vitest'
import Navbar from '~/components/Navbar.vue'
import Sidebar from '~/components/Sidebar.vue'
import Button from 'primevue/button'
import Menu from 'primevue/menu'

describe('Navbar', () => {
	it('can mount the component', async () => {
		const component = await mountSuspended(Navbar)
		expect(component.exists()).toBe(true)
	})

	it('renders the logo correctly', async () => {
		const component = await mountSuspended(Navbar)
		const logoLight = component.find('img[alt="Logo"]')
		const logoDark = component.find('img[alt="Logo"]')
		expect(logoLight.exists()).toBe(true)
		expect(logoDark.exists()).toBe(true)
	})

	it('renders the Sidebar component', async () => {
		const component = await mountSuspended(Navbar, {
			stubs: {
				Sidebar,
			},
		})
		const sidebar = component.findComponent(Sidebar)
		expect(sidebar.exists()).toBe(true)
	})

	it('renders the logout button', async () => {
		const component = await mountSuspended(Navbar)
		const logoutButton = component.findComponent(Button)
		expect(logoutButton.exists()).toBe(true)
		expect(logoutButton.text()).toBe('')
	})
})
