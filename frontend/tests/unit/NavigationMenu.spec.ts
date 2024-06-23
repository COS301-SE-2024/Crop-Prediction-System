// @vitest-environment nuxt
import { mountSuspended } from '@nuxt/test-utils/runtime'
import { it, expect, describe } from 'vitest'
import NavigationMenu from '~/components/NavigationMenu.vue'
import PrimeVue from 'primevue/config'
import Menu from 'primevue/menu'
import { createRouter, createMemoryHistory } from 'vue-router'

const router = createRouter({
  history: createMemoryHistory(),
  routes: [
    { path: '/', component: { template: '<div>Home</div>' } },
    { path: '/inputs/add-field-data', component: { template: '<div>Add Field Data</div>' } },
    { path: '/inputs/manage-fields', component: { template: '<div>Manage Fields</div>' } },
    { path: '/log-data/view-logs', component: { template: '<div>View Logs</div>' } },
    { path: '/model-training/manage-model', component: { template: '<div>Manage Model</div>' } },
    { path: '/analytics/crop-yield-data', component: { template: '<div>Crop Yield Data</div>' } },
    { path: '/team/manage', component: { template: '<div>Manage Team</div>' } },
    { path: '/team/join', component: { template: '<div>Join Team</div>' } },
  ],
})

describe('NavigationMenu', () => {
  it('can mount the component', async () => {
    const component = await mountSuspended(NavigationMenu, {
      global: {
        plugins: [PrimeVue, router],
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
        plugins: [PrimeVue, router],
        components: { Menu },
        stubs: {
          RouterLink: true,
        },
      },
    })
    
    const menuItemLabels = component.findAll('.p-menuitem')
    expect(menuItemLabels.length).toBe(8) 
  })

  it('generates router links correctly', async () => {
    const component = await mountSuspended(NavigationMenu, {
      global: {
        plugins: [PrimeVue, router],
        components: { Menu },
        stubs: {
          RouterLink: {
            template: '<a :href="to"><slot /></a>',
            props: ['to']
          }
        },
      },
    })

    const links = component.findAll('a')
    expect(links.length).toBe(16)

    const urls = links.map(link => link.attributes('href'))
    expect(urls).toContain('/')
    expect(urls).toContain('/inputs/add-field-data')
    expect(urls).toContain('/inputs/manage-fields')
    expect(urls).toContain('/log-data/view-logs')
    expect(urls).toContain('/model-training/manage-model')
    expect(urls).toContain('/analytics/crop-yield-data')
    expect(urls).toContain('/team/manage')
    expect(urls).toContain('/team/join')
  })
})
