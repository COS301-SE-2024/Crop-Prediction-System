// @vitest-environment nuxt
import { mount } from '@vue/test-utils'
import FieldStatsPanel from '~/components/FieldStatsPanel.vue'
import StatsCard from '~/components/StatsCard.vue'
import { describe, it, expect } from 'vitest'

describe('FieldStatsPanel.vue', () => {
  it('renders correctly with props', () => {
    const props = {
      selectedField: { name: 'Field 1' },
      filter: { value: 0 },
      filterOptions: [
        { name: 'Option 1', value: 0 },
        { name: 'Option 2', value: 30 },
      ],
      chartData: {
        soilMoisture: [1, 2, 3],
        temperature: [20, 21, 22],
      },
    }

    const wrapper = mount(FieldStatsPanel, {
      props,
    })

    expect(wrapper.text()).toContain('More Field Stats')
    expect(wrapper.findAllComponents(StatsCard).length).toBe(2) // Adjust if more cards are added in future
  })

  it('emits update:filter event when SelectButton is changed', async () => {
    const props = {
      selectedField: { name: 'Field 1' },
      filter: { value: 0 },
      filterOptions: [
        { name: 'Option 1', value: 0 },
        { name: 'Option 2', value: 30 },
      ],
      chartData: {},
    }

    const wrapper = mount(FieldStatsPanel, {
      props,
    })

    // Use findComponent to locate SelectButton
    const selectButton = wrapper.findComponent({ name: 'SelectButton' })

    // Emit the update:modelValue event
    await selectButton.vm.$emit('update:modelValue', { value: 30 })

    // Check if the emitted event contains the correct data
    expect(wrapper.emitted()['update:filter']).toBeTruthy()
    expect(wrapper.emitted()['update:filter'][0]).toEqual([{ value: 30 }])
  })

  it('displays Skeleton when no selectedField is provided', () => {
    const props = {
      selectedField: null,
      filter: { value: 0 },
      filterOptions: [{ name: 'Option 1', value: 0 }],
      chartData: {},
    }

    const wrapper = mount(FieldStatsPanel, {
      props,
    })

    expect(wrapper.findComponent({ name: 'Skeleton' }).exists()).toBe(true)
  })

  it('renders correct number of StatsCard based on chartData', () => {
    const props = {
      selectedField: { name: 'Field 1' },
      filter: { value: 0 },
      filterOptions: [{ name: 'Option 1', value: 0 }],
      chartData: {
        soilMoisture: [1, 2, 3],
        temperature: [20, 21, 22],
      },
    }

    const wrapper = mount(FieldStatsPanel, {
      props,
    })

    // Adjust according to the number of keys in chartData
    expect(wrapper.findAllComponents(StatsCard).length).toBe(2)
  })
})
