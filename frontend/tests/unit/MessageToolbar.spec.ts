// @vitest-environment nuxt
import { mount } from '@vue/test-utils'
import MessageToolbar from '~/components/MessageToolbar.vue'
import { describe, it, expect, beforeEach, vi } from 'vitest'

vi.mock('primevue/usetoast', () => ({
  useToast: () => ({
    add: vi.fn(),
  }),
}))

// Mocking PrimeVue components
vi.mock('primevue/textarea', () => ({
  default: {
    name: 'Textarea',
    props: ['modelValue', 'invalid'],
    template: '<textarea :value="modelValue"></textarea>',
  },
}))

vi.mock('primevue/button', () => ({
  default: {
    name: 'Button',
    props: ['icon', 'severity', 'text', 'size'],
    template: '<button @click="$emit(\'click\')"></button>',
  },
}))

describe('MessageToolbar.vue', () => {
  const fetchUserMock = vi.fn()
  const $fetchMock = vi.fn()

  beforeEach(() => {
    vi.clearAllMocks()
    global.$fetch = $fetchMock
    global.useSupabaseUser = () => ({ value: { id: 'test-user-id' } })
  })

  const mountComponent = () => {
    return mount(MessageToolbar, {
      global: {
        stubs: {
          Textarea: true, // Stubbing the Textarea component
          Button: true, // Stubbing the Button component
        },
      },
    })
  }

  it('component mounts correctly', () => {
    const wrapper = mountComponent()

    expect(wrapper.exists()).toBe(true)
    expect(wrapper.findComponent({ name: 'Textarea' }).exists()).toBe(true)
    expect(wrapper.findComponent({ name: 'Button' }).exists()).toBe(true)
  })
})