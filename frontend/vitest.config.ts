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
			exclude: [
				'presets/**/*',
				'nuxt.config.ts',
				'tailwind.config.js',
				'frontend/.nuxt',
				'plugins/**/*',
				'.nuxt/**/*',
				'server/api/**/*',
				'components/LogsView.vue',
				'layouts/**/*',
			],
			reportsDirectory: 'coverage',
			reporter: ['text', 'html', 'json'],
		},
	},
})
