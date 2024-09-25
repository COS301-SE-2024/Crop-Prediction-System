// @vitest-environment nuxt
import { mountSuspended } from '@nuxt/test-utils/runtime'
import { it, expect, describe } from 'vitest'
import StatsCard from '~/components/StatsCard.vue'
import Chart from 'primevue/chart'

describe('StatsCard', () => {
	const props = {
		title: 'Test Title',
		chartData: {
			labels: ['January', 'February', 'March', 'April'],
			datasets: [
				{
					label: 'Test Data',
					data: [65, 59, 80, 81],
					fill: false,
					borderColor: 'rgb(75, 192, 192)',
					tension: 0.1,
				},
			],
		},
		chartType: 'line',
	}

	it('can mount the component', async () => {
		const component = await mountSuspended(StatsCard, { props })
		expect(component.exists()).toBe(true)
	})

	it('renders title correctly', async () => {
		const component = await mountSuspended(StatsCard, { props })
		const title = component.find('h2')
		expect(title.exists()).toBe(true)
		expect(title.text()).toBe(props.title)
	})

	it('renders chart correctly', async () => {
		const component = await mountSuspended(StatsCard, { props })
		const chart = component.findComponent(Chart)
		expect(chart.exists()).toBe(true)
		expect(chart.props('type')).toBe(props.chartType)
		expect(chart.props('data')).toEqual(props.chartData)
	})

	it('sets chart options correctly', async () => {
		const component = await mountSuspended(StatsCard, { props })
		const chart = component.findComponent(Chart)
		expect(chart.exists()).toBe(true)

		const options = chart.props('options')
		expect(options).toEqual(
			expect.objectContaining({
				maintainAspectRatio: false,
				responsive: true,
				plugins: {
					legend: {
						display: true,
					},
				},
				scales: expect.objectContaining({
					x: expect.objectContaining({
						ticks: expect.objectContaining({
							autoSkip: false,
						}),
						grid: expect.objectContaining({
							color: 'rgba(192, 192, 192, 0.5)',
							display: true,
						}),
					}),
					y: expect.objectContaining({
						beginAtZero: false,
						ticks: expect.objectContaining({
							stepSize: 2,
						}),
						grid: expect.objectContaining({
							color: 'rgba(192, 192, 192, 0.5)',
							display: true,
						}),
					}),
				}),
			}),
		)
	})
})
