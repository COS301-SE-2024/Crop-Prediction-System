describe.only('Demo', () => {
	before(() => {
		cy.login('ggu.capstone@gmail.com', 'Test1234#')
		cy.visit('/')
	})

	it('Demo', () => {
		cy.get('.w-full.md\\:w-1\\/3').should('exist')
		cy.get('.w-full.md\\:w-2\\/3').should('exist')

		cy.get('#pv_id_1').click()
		cy.get('#pv_id_1_list').should('be.visible')
		cy.get('#pv_id_1_list').contains('Wheat 3').click()
		cy.get('legend').click()

		cy.get('i.pi.pi-user').click()
		cy.get('#pv_id_5_3').click()
		cy.get('#pv_id_5_3').click()
		cy.get('#pv_id_5_6').click()
	})
})
