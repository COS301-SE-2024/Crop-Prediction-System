// @vitest-environment nuxt
import { mount } from '@vue/test-utils'
import MarketDataCard from '~/components/MarketDataCard.vue'
import { describe, it, expect } from 'vitest'

describe('MarketDataCard.vue', () => {
  it('renders correctly with required props', () => {
    const props = {
      title: 'Test Title',
      footer: 'Test Footer',
    }

    const wrapper = mount(MarketDataCard, {
      props,
    })

    expect(wrapper.text()).toContain('Test Title')
    expect(wrapper.text()).toContain('Test Footer')
  })

  it('displays the tph value when it is not zero', () => {
    const props = {
      title: 'Test Title',
      tph: 10,
      footer: 'Test Footer',
    }

    const wrapper = mount(MarketDataCard, {
      props,
    })

    expect(wrapper.text()).toContain('10 t/ha')
  })

  it('displays "N/A" when tph is zero', () => {
    const props = {
      title: 'Test Title',
      tph: 0,
      footer: 'Test Footer',
    }

    const wrapper = mount(MarketDataCard, {
      props,
    })

    expect(wrapper.text()).toContain('N/A')
  })

  it('applies the correct classes for dark mode', () => {
    const props = {
      title: 'Test Title',
      tph: 10,
      footer: 'Test Footer',
    }

    const wrapper = mount(MarketDataCard, {
      props,
      global: {
        provide: {
          dark: true, // Simulating dark mode
        },
      },
    })

    expect(wrapper.classes()).toContain('dark:bg-surface-800')
    expect(wrapper.find('span.text-surface-600').classes()).toContain('dark:text-surface-0/60')
  })
})
