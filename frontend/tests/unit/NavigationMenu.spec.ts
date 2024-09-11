// @vitest-environment nuxt

import { mountSuspended } from '@nuxt/test-utils/runtime'
import { it, expect, describe } from 'vitest'
import NavigationMenu from '~/components/NavigationMenu.vue'
import PrimeVue from 'primevue/config'
import Menu from 'primevue/menu'

describe('NavigationMenu', () => {
	it('can mount the component', async () => {
		const component = await mountSuspended(NavigationMenu, {
			global: {
				plugins: [PrimeVue],
				components: { Menu },
				stubs: {
					RouterLink: true,
				},
			},
		})
		expect(component.exists()).toBe(true)
	})

	it('renders the correct number of labels', async () => {
		const component = await mountSuspended(NavigationMenu, {
			global: {
				plugins: [PrimeVue],
				components: { Menu },
				stubs: {
					RouterLink: true,
				},
			},
		})

		const menuItemLabels = component.findAll('.p-menuitem')
		expect(menuItemLabels.length).toBe(6)
	})

	it('generates router links correctly', async () => {
		const component = await mountSuspended(NavigationMenu, {
			global: {
				plugins: [PrimeVue],
				components: { Menu },
				stubs: {
					RouterLink: {
						template: '<a :href="to"><slot /></a>',
						props: ['to'],
					},
				},
			},
		})

		const links = component.findAll('a')
		expect(links.length).toBe(12)

		const urls = links.map((link) => link.attributes('href'))
		expect(urls).toContain('/')
		expect(urls).toContain('/inputs/add-field-data')
		expect(urls).toContain('/inputs/manage-fields')
		expect(urls).toContain('/log-data/view-logs')
		expect(urls).toContain('/team/manage')
	})
})