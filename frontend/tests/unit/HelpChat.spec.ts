// @vitest-environment nuxt
import { mount } from '@vue/test-utils'
import { it, expect, describe, beforeEach, vi } from 'vitest'
import HelpChat from '~/components/HelpChat.vue'

// Mocking required components
vi.mock('primevue/card', () => ({
  default: {
    name: 'Card',
    template: '<div><slot name="content" /></div>',
    props: ['class'],
  },
}))

vi.mock('primevue/tag', () => ({
  default: {
    name: 'Tag',
    template: '<span><slot /></span>',
    props: ['severity', 'class'],
  },
}))

vi.mock('primevue/textarea', () => ({
  default: {
    name: 'Textarea',
    template: '<textarea />',
    props: ['placeholder', 'class'],
  },
}))

vi.mock('primevue/button', () => ({
  default: {
    name: 'Button',
    template: '<button><slot /></button>',
    props: ['icon', 'severity', 'text', 'size'],
  },
}))

describe('HelpChat', () => {
  let wrapper

  beforeEach(() => {
    wrapper = mount(HelpChat, {
      props: { activeIndex: 6 },
    })
  })

  it('mounts the component', () => {
    expect(wrapper.exists()).toBe(true)
  })

  it('renders the main heading', () => {
    const heading = wrapper.find('h1')
    expect(heading.exists()).toBe(true)
    expect(heading.text()).toBe('Chat Help')
  })

  it('renders the "Chat Layout" section', () => {
    const sectionHeading = wrapper.findAll('h2').at(0)
    expect(sectionHeading.text()).toBe('Chat Layout')
    expect(wrapper.text()).toContain('The chat page is divided into three main sections:')
  })

  it('renders the "Viewing Messages" section', () => {
    const sectionHeading = wrapper.findAll('h2').at(1)
    expect(sectionHeading.text()).toBe('Viewing Messages')
    expect(wrapper.text()).toContain('The messages area displays all the messages from your team:')
  })

  it('renders the message input example', () => {
    expect(wrapper.text()).toContain('Type your message in the message input area')
    expect(wrapper.find('textarea').exists()).toBe(true)
  })

  it('renders the "Sending Messages" section', () => {
    const sectionHeading = wrapper.findAll('h2').at(2)
    expect(sectionHeading.text()).toBe('Sending Messages')
    expect(wrapper.text()).toContain('To send a message to your team:')
  })

  it('renders a date tag', () => {
    expect(wrapper.text()).toContain('16 August 2024')
    expect(wrapper.text()).toContain('17 August 2024')
  })
})
