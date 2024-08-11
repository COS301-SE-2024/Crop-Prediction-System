// @vitest-environment nuxt
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { shallowMount } from '@vue/test-utils'
import LogsToolbar from '~/components/LogsToolbar.vue' // Adjust the import path accordingly

describe('LogsToolbar', () => {
  let wrapper

  beforeEach(() => {
    wrapper = shallowMount(LogsToolbar, {
      global: {
        mocks: {
          $fetch: vi.fn(),
        },
      },
    })
  })

  it('should mount the component', () => {
    expect(wrapper.exists()).toBe(true)
  })
})
