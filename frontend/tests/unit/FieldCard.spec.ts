// @vitest-environment nuxt
import { mount } from '@vue/test-utils'
import FieldCard from '~/components/FieldCard.vue'
import { describe, it, expect, vi } from 'vitest'

// Mock PrimeVue components
vi.mock('primevue/dropdown', () => ({
  default: {
    props: ['modelValue', 'options', 'optionLabel', 'placeholder', 'checkmark', 'highlightOnSelect'],
    emits: ['update:modelValue'],
    template: '<div @click="$emit(\'update:modelValue\', options[0])"></div>', // Emit the first option when clicked
  },
}))

vi.mock('primevue/card', () => ({
  default: {
    template: '<div><slot></slot></div>', // Mock Card component
  },
}))

vi.mock('primevue/chart', () => ({
  default: {
    props: ['type', 'data', 'options'],
    template: '<div class="chart-mock"></div>', // Mock Chart component
  },
}))

vi.mock('primevue/tag', () => ({
  default: {
    props: ['value', 'severity'],
    template: '<div class="tag-mock">{{ value }} - {{ severity }}</div>', // Mock Tag component
  },
}))

const mockFields = [
  { id: 1, name: 'Field 1', avgYield: 5.5 },
  { id: 2, name: 'Field 2', avgYield: 6.0 },
]

// Mock data for fields
const mockField = {
  id: 1,
  created_at: '2024-01-01T00:00:00Z',
  field_area: [[25.746, 28.228] as [number, number]],
  field_name: 'Field 1',
  field_tph: 50,
  field_health: 60,
  crop_type: 'Wheat',
  team_id: 'Team 1',
  updated_at: '2024-01-01T00:00:00Z',
  hectare: 100,
  pastYieldAvg: 5.5,
  data: {
    date: ['08-10', '08-11'],
    health: [50, 60],
    rain: [10, 20],
    sprayability: [60, 70],
    yield: [5, 6],
    summary: ['Good weather', 'Excellent conditions'],
  },
}

// Mock internalSelectedField to avoid undefined errors
const mockSelectedField = {
  ...mockField,
  pastYieldAvg: 5.5,
}

describe('FieldCard', () => {
  it('can mount the component', () => {
    const wrapper = mount(FieldCard, {
      props: {
        modelValue: mockField,
        fields: [mockField],
      },
      data() {
        return {
          internalSelectedField: mockSelectedField,
        }
      },
    })

    expect(wrapper.exists()).toBe(true)
  })
})