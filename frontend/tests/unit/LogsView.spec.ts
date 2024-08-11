// @vitest-environment nuxt
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { shallowMount, flushPromises } from '@vue/test-utils'
import LogsView from '~/components/LogsView.vue' // Adjust the import path accordingly

// Mock Nuxt and Supabase functionality
globalThis.useSupabaseUser = vi.fn(() => ({ value: { id: 'user-id' } }))
globalThis.$fetch = vi.fn()

describe('LogsView', () => {
  let wrapper

  beforeEach(() => {
    wrapper = shallowMount(LogsView, {
      global: {
        mocks: {
          $fetch: globalThis.$fetch,
        },
      },
    })

    globalThis.$fetch.mockReset()
  })

  it('should mount the component', () => {
    expect(wrapper.exists()).toBe(true)
  })
  
  it('should handle select all change', async () => {
    wrapper.vm.entries = [
      { date: '2024-08-10', yield: '100' },
      { date: '2024-08-11', yield: '150' },
    ]
    await wrapper.vm.$nextTick()

    wrapper.vm.onSelectAllChange({ checked: true })
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.selectedDataEntries).toHaveLength(2)
    expect(wrapper.vm.selectAll).toBe(true)

    wrapper.vm.onSelectAllChange({ checked: false })
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.selectedDataEntries).toHaveLength(0)
    expect(wrapper.vm.selectAll).toBe(false)
  })

  it('should handle row selection and unselection', async () => {
    wrapper.vm.entries = [
      { date: '2024-08-10', yield: '100' },
      { date: '2024-08-11', yield: '150' },
    ]
    wrapper.vm.selectedDataEntries = [
      { date: '2024-08-10', yield: '100' },
    ]
    await wrapper.vm.$nextTick()

    wrapper.vm.onRowSelect()
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.selectAll).toBe(false)

    wrapper.vm.selectedDataEntries = wrapper.vm.entries
    wrapper.vm.onRowSelect()
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.selectAll).toBe(true)

    wrapper.vm.selectedDataEntries = []
    wrapper.vm.onRowUnselect()
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.selectAll).toBe(false)
  })
})