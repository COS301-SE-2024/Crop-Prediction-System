// @vitest-environment nuxt
import { flushPromises, mount } from '@vue/test-utils'
import { describe, it, expect, vi } from 'vitest'
import GoogleMapsField from '@/components/GoogleMapsField.vue'

// Mock the mapsLoader module
vi.mock('@/plugins/mapsLoader', () => ({
	load: vi.fn(() => Promise.resolve()),
}))

const mockFieldData = [
	{
		id: 1,
		field_area: [
			[25.746, 28.228],
			[25.748, 28.23],
			[25.749, 28.231],
			[25.746, 28.228],
		],
	},
	{
		id: 2,
		field_area: [
			[25.75, 28.232],
			[25.751, 28.233],
			[25.752, 28.234],
			[25.75, 28.232],
		],
	},
]

const mockSelectedField = {
	id: 1,
	field_area: [
		[25.746, 28.228],
		[25.748, 28.23],
		[25.749, 28.231],
		[25.746, 28.228],
	],
}

describe('GoogleMapsField', () => {
	it('can mount the component', async () => {
		const wrapper = mount(GoogleMapsField, {
			props: {
				fields: mockFieldData,
				selectedField: mockSelectedField,
			},
		})
		await flushPromises()
		expect(wrapper.vm).toBeTruthy()
	})

	// it('draws polygons correctly', async () => {
	//   const wrapper = mount(GoogleMapsField, {
	//     props: {
	//       fields: mockFieldData,
	//       selectedField: mockSelectedField,
	//     },
	//   })
	//   await flushPromises()
	//   expect(wrapper.vm.polygons.length).toBe(mockFieldData.length)
	// })

	it('updates the selected field correctly', async () => {
		const wrapper = mount(GoogleMapsField, {
			props: {
				fields: mockFieldData,
				selectedField: null,
			},
		})
		await flushPromises()

		await wrapper.setProps({ selectedField: mockSelectedField })
		await flushPromises()

		expect(wrapper.vm.selectedField.id).toBe(mockSelectedField.id)
	})
})
