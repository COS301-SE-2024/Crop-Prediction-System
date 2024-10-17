// @vitest-environment nuxt
import { mount } from '@vue/test-utils'
import Navbar from '../components/Navbar.vue'
import PrimeVue from 'primevue/config'
import OverlayPanel from 'primevue/overlaypanel'
import Menu from 'primevue/menu'
import Toast from 'primevue/toast'
import { describe, it, expect, vi } from 'vitest'

// Mock necessary composables or services
vi.mock('primevue/usetoast', () => ({
	useToast: vi.fn().mockReturnValue({
		add: vi.fn(),
	}),
}))

vi.mock('@supabase/supabase-js', () => ({
	useSupabaseUser: vi.fn().mockReturnValue({
		value: {
			email: 'test@example.com',
			team_id: '1',
		},
	}),
	useSupabaseClient: vi.fn().mockReturnValue({
		auth: {
			signOut: vi.fn().mockResolvedValue({ error: null }),
		},
		channel: vi.fn().mockReturnThis(),
		removeChannel: vi.fn(),
	}),
}))

vi.mock('vue-router', () => ({
	useRoute: vi.fn().mockReturnValue({
		path: '/some-path',
	}),
	useRouter: vi.fn().mockReturnValue({
		push: vi.fn(),
	}),
	navigateTo: vi.fn(),
}))

// PARTIAL MOCK of vue to retain defineComponent while mocking other composables
vi.mock('vue', async (importOriginal) => {
	const actual = await importOriginal()
	return {
		...actual,
		useState: vi.fn().mockReturnValue({ value: 0 }),
		onMounted: vi.fn(),
		onUnmounted: vi.fn(),
		useColorMode: vi.fn().mockReturnValue({
			preference: 'light',
		}),
	}
})

describe('Navbar', () => {
	it('mounts successfully', () => {
		const wrapper = mount(Navbar, {
			global: {
				plugins: [PrimeVue],
				components: {
					OverlayPanel,
					Menu,
					Toast,
				},
			},
		})

		// Check if the component mounted
		expect(wrapper.exists()).toBe(true)
	})

	it('renders correctly', async () => {
		const wrapper = mount(Navbar, {
			global: {
				plugins: [PrimeVue],
				components: {
					OverlayPanel,
					Menu,
					Toast,
				},
			},
		})

		expect(wrapper.exists()).toBe(true)
	})
})
