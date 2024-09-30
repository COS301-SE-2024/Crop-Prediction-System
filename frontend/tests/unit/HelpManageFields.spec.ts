// @vitest-environment nuxt
import { mount } from '@vue/test-utils'
import { it, expect, describe, beforeEach } from 'vitest'
import HelpManageFields from '~/components/HelpManageFields.vue'
import { vi } from 'vitest'

// Mocking required components
vi.mock('primevue/card', () => ({
  default: {
    name: 'Card',
    template: '<div><slot name="content" /></div>',
    props: ['class'],
  },
}))

vi.mock('primevue/inputtext', () => ({
  default: {
    name: 'InputText',
    template: '<input />',
    props: ['placeholder', 'class'],
  },
}))

vi.mock('primevue/dropdown', () => ({
  default: {
    name: 'Dropdown',
    template: '<select><slot /></select>',
    props: ['options', 'optionLabel', 'placeholder', 'class', 'showClear'],
  },
}))

vi.mock('primevue/button', () => ({
  default: {
    name: 'Button',
    template: '<button><slot /></button>',
    props: ['label', 'icon', 'size', 'severity', 'outlined'],
  },
}))

vi.mock('primevue/progressspinner', () => ({
  default: {
    name: 'ProgressSpinner',
    template: '<div>Loading...</div>',
  },
}))

describe('HelpManageFields', () => {
  let wrapper

  beforeEach(() => {
    wrapper = mount(HelpManageFields, {
      props: { activeIndex: 2 },
    })
  })

  it('mounts the component', () => {
    expect(wrapper.exists()).toBe(true)
  })

  it('renders the main heading', () => {
    const heading = wrapper.find('h1')
    expect(heading.exists()).toBe(true)
    expect(heading.text()).toBe('Manage Fields Help')
  })

  it('renders the "Searching and Filtering Fields" section', () => {
    const sectionHeading = wrapper.findAll('h2').at(0)
    expect(sectionHeading.text()).toBe('1. Searching and Filtering Fields')
    expect(wrapper.text()).toContain('Use the search bar to find fields by name.')
  })

  it('renders the "Training Fields" section', () => {
    const sectionHeading = wrapper.findAll('h2').at(1)
    expect(sectionHeading.text()).toBe('2. Training Fields')
    expect(wrapper.text()).toContain('You can train individual fields or all fields at once:')
  })

  it('renders the "Viewing Field Details" section', () => {
    const sectionHeading = wrapper.findAll('h2').at(2)
    expect(sectionHeading.text()).toBe('3. Viewing Field Details')
    expect(wrapper.text()).toContain('Each field is displayed as a card containing key information:')
  })
 
  it('renders the "Loading Indicators" section', () => {
    const sectionHeading = wrapper.findAll('h2').at(5)
    expect(sectionHeading.text()).toBe('6. Loading Indicators')
    expect(wrapper.text()).toContain('While fields are being fetched or actions are being performed, loading indicators and messages will appear.')
  })
})
