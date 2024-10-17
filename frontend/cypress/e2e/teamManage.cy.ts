describe('Manage Team Page', () => {
	beforeEach(() => {
		cy.login('ggu.capstone@gmail.com', 'Testing1234#')
		cy.wait(6000)
		cy.get('button[aria-label="Filter"]').click()
		cy.wait(500)
		cy.get('span[class="pi pi-users pl-4"]').click()
	})

	it('can invite a member', () => {
		cy.wait(3000)
		cy.get('button[aria-label="Invite Member"]').click()

		cy.wait(500)
		cy.get('#newUserEmail').clear().type('example@gmail.com')

		cy.wait(200)
		cy.get('svg[data-pc-section="dropdownicon"]').eq(1).click()
		cy.contains('li', 'Farmer').scrollIntoView().should('be.visible').click()

		cy.wait(500)
		cy.get('button[aria-label="Send Invite"]').click()
	})

	it.only('can edit roles', () => {
		cy.wait(3000)
		cy.get('span[class="pi pi-pencil mx-0"]').click()
		cy.wait(200)
		cy.get('svg[data-pc-section="dropdownicon"]').eq(0).click()
		cy.contains('li', 'Farmer').scrollIntoView().should('be.visible').click()

		cy.get('span[aria-label="Farmer"]').should('be.visible')
	})
})
