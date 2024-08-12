// @vitest-environment nuxt
import { mount } from '@vue/test-utils';
import { vi, it, expect, describe } from 'vitest'
import FieldData from '~/components/FieldData.vue'

vi.mock('$fetch', () => vi.fn());

describe('check the field data', () => {
    it('the api call should occur when the component is mounted', async () => {
        const userIDcommon = "02dffef4-7788-423c-869e-17db9c821542";
        const fetchSpy = vi.spyOn(globalThis, '$fetch').mockResolvedValue(userIDcommon);
        const userID = "02dffef4-7788-423c-869e-17db9c821542";
        const wrapper = mount(FieldData, {
            global:{
                stubs: {
                    FieldData: true,
                },
            },
            props:{
                userID,
            },
        });
        await wrapper.vm.$nextTick();

        expect($fetch).toHaveBeenCalledWith('/api/getUserFields',
            // undefined since the user isnt logged in
            expect.objectContaining({params: {userid: undefined}}),
        );
    })

    it("gets the field data correctly", async () => {
        const mockFieldData = {
            field_name: 'test',
            crop_type: 'wheat',
            hectare: '0.211313511746061',
            field_area: '[[25.746, 28.228], [25.748, 28.230], [25.749, 28.231], [25.746, 28.228]]',
        };
        vi.spyOn(globalThis, '$fetch').mockResolvedValue(mockFieldData);
        let userID = '02dffef4-7788-423c-869e-17db9c821542';
        // fetch('/api/getUserFields', {
        //     params: { userid: userID },
        //   })
        //     .then((response) => response.json())
        
    })
})