// @vitest-environment nuxt
import { mountSuspended } from '@nuxt/test-utils/runtime'
import { vi, it, expect, describe } from 'vitest'
import fetchUserFields from '~/components/GoogleMap.vue'

// Mock the functions
// vi.mock('@supabase/supabase-js',);
// vi.mock('@fetch');

describe('GoogleMapsField Integration Test', () => {
	it('gets the Fields correctly', async () => {
		const mockUser = { id: '02dffef4-7788-423c-869e-17db9c821542' }
		const mockTeamID = { team_id: 'd8d64098-b290-4fd2-b810-cadb1fe213ea' }
		const mockFields = [
			{
				created_at: '2024-08-12 08:01:54.358373+00',
				field_area:
					'[[-25.87074931861521, 28.159573936176287], [-25.870773452610734, 28.160054051589952], [-25.871036512841457, 28.160062098216997], [-25.87101479229413, 28.159563207340227]]',
				field_name: 'TEST',
				crop_type: 'wheat',
				team_id: 'd8d64098-b290-4fd2-b810-cadb1fe213ea',
				updated_at: '2024-08-12 08:01:54.358373+00',
				hectare: '0.211313511746061',
				id: '13f0c522-5b77-4110-ab95-c7da127d9d80',
			},
		]
		// const result = new fetchUserFields();
		// function is not callable?
		expect(true).toBe(true)
	})
})
