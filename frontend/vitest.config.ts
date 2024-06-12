import { defineVitestConfig } from '@nuxt/test-utils/config'

export default defineVitestConfig({
	test: {
		environmentOptions: {
			nuxt: {
				mock: {
					intersectionObserver: true,
					indexedDb: true,
				},
			},
		},
		testTimeout: 10000,
		coverage: {
			enabled: true,
			provider: 'v8',
			exclude: ['presets/**/*'],
			reportsDirectory: 'coverage',
			reporter: ['text', 'html', 'json'],
		},
	},
})
