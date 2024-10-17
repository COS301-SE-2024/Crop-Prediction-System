// @vitest-environment nuxt
import { mount } from '@vue/test-utils'
import { it, expect, describe, beforeEach, vi } from 'vitest'
import HelpFieldDashboard from '~/components/HelpFieldDashboard.vue'
import Dropdown from 'primevue/dropdown' // Import the Dropdown component to mock it

// Mocking the Dropdown component
vi.mock('primevue/dropdown', () => ({
  default: {
    name: 'Dropdown',
    template: '<div><slot></slot></div>',
    props: ['modelValue', 'options', 'optionLabel', 'placeholder', 'class'],
  },
}))

describe('HelpFieldDashboard.vue', () => {
  let wrapper
  beforeEach(() => {
    // Clear all mocks before each test
    vi.clearAllMocks()
    wrapper = mount(HelpFieldDashboard, {
      props: { activeIndex: 0 },
    })
  })

  it('mounts the component', () => {
    expect(wrapper.exists()).toBe(true)
  })

  it('renders the component when activeIndex is 0', () => {
    const card = wrapper.findComponent({ name: 'Card' })
    expect(card.exists()).toBe(true)
    expect(wrapper.text()).toContain('Field Dashboard Help')
  })

  it('renders the main heading', () => {
    const heading = wrapper.find('h1')
    expect(heading.exists()).toBe(true)
    expect(heading.text()).toBe('Field Dashboard Help')
  })

  it('renders the "Selecting a Field" section', () => {
    const sectionHeading = wrapper.findAll('h2').at(0) 
    expect(sectionHeading.text()).toMatch(/1\. Selecting a Field/)
    expect(wrapper.text()).toContain('Use the dropdown at the top of the FieldCard to select the field you\'re interested in.')
  })

  it('renders the "Field Information" section', () => {
    const sectionHeading = wrapper.findAll('h2').at(1) 
    expect(sectionHeading.text()).toMatch(/2\. Field Information/)
    expect(wrapper.text()).toContain('After selecting a field, the FieldCard displays key information about the field, including:')
  })

  it('renders the "Maps Interface" section', () => {
    const sectionHeading = wrapper.findAll('h2').at(2) 
    expect(sectionHeading.text()).toMatch(/3\. Maps Interface/)
    expect(wrapper.text()).toContain('The GoogleMapsField component shows your fields on an interactive map.')
  })

  it('renders the "Viewing Statistics" section', () => {
    const sectionHeading = wrapper.findAll('h2').at(4) 
    expect(sectionHeading.text()).toMatch(/5\. Viewing Statistics/)
    expect(wrapper.text()).toContain('The Advanced Statistics panel displays several charts using the StatsCard component, including:')
  })

  it('renders the "Loading Indicator" section', () => {
    const sectionHeading = wrapper.findAll('h2').at(6) 
    expect(sectionHeading.text()).toMatch(/6\. Loading Indicator/)
    expect(wrapper.text()).toContain('While the field data is being fetched, a loading spinner and message will appear.')
  })
})
