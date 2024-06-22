// @vitest-environment nuxt
import { mountSuspended } from '@nuxt/test-utils/runtime'
import { it, expect, describe } from 'vitest'
import StatPanel from '~/components/StatPanel.vue'
import Chart from 'primevue/chart'
import Tag from 'primevue/tag'

describe('StatPanel', () => {

    //Mock Props
    const props = {
        title: 'Test Title',
        chartInput: [100, 120, 130, 90, 80, 70],
        chartType: 'line',
    }

    it('can mount the component', async () => {
        const component = await mountSuspended(StatPanel, { props })
        expect(component.exists()).toBe(true)
    })

    it('renders title correctly', async () => {
        const component = await mountSuspended(StatPanel, { props })
        const title = component.find('p.text-lg')
        expect(title.exists()).toBe(true)
        expect(title.text()).toBe(props.title)
    })

    it('renders chart correctly', async () => {
        const component = await mountSuspended(StatPanel, { props })
        const chart = component.findComponent(Chart)
        expect(chart.exists()).toBe(true)
        expect(typeof props.chartType).toBe('string')
    })

    it('renders tag correctly', async () => {
        const component = await mountSuspended(StatPanel, { props })
        const tag = component.findComponent(Tag)
        expect(tag.exists()).toBe(true)

        const severityProp = tag.props('severity')
        const valueProp = tag.props('value')

        expect(severityProp).toMatch(/danger|warning|success/)
        expect(['Severe', 'Moderate', 'Healthy']).toContain(valueProp)
    })
})
