// @vitest-environment nuxt
import { mountSuspended } from '@nuxt/test-utils/runtime'
import { it, expect, describe } from 'vitest'
import FieldData from '~/components/FieldData.vue'


describe('FieldData', () => {
    it('can mount the component', async () => {
        const component = await mountSuspended(FieldData)
        expect(component.exists()).toBe(true)
    })
    // further tests can be added here
    // it('render correctly'), async () => {
    //     const component = await mountSuspended(FieldData)
    //     expect(component.html()).toContain('Field Data')
    // }

    // it('fetches data correctly'), async () => {
    //     const component = await mountSuspended(FieldData)
    //     expect(component.vm.data).toBe('data')
    // }
})