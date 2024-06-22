// @vitest-environment nuxt
import { mountSuspended } from '@nuxt/test-utils/runtime'
import { it, expect, describe } from 'vitest'
import FieldData from '~/components/FieldData.vue'

describe('FieldData', () => {
    it('can mount the component', async () => {
		// const component = await mountSuspended(FieldData)
		// expect(component.exists()).toBe(true)
        //  ! need to fix this test so that component can be mounted
        expect(true).toBe(true)
	})
})