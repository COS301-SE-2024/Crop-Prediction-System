describe('Login Page', () => {
	beforeEach(() => {
		cy.visit('/login')
	})

	it('should display the login form', () => {
		cy.get('h1').should('contain', 'Log in')
		cy.get('#email').should('be.visible')
		cy.get('input[type="password"]').should('be.visible')
		cy.get('button').contains('Login').should('be.visible')
	})

	it('should show error message with incorrect login', () => {
		const email = 'ggu.capstone@gmail.com'
		const password = 'WrongPassword'

		cy.get('#email').clear().type(email)
		cy.get('input[type="password"]').clear().type(password)
		cy.get('button').contains('Login').click()

		cy.get('small').contains('Invalid login credentials').should('be.visible')
	})

	it('should login successfully', () => {
		const email = 'ggu.capstone@gmail.com'
		const password = 'Test1234#'

		cy.wait(500)
		cy.get('#email').clear().type(email)
		cy.get('input[type="password"]').clear().type(password)
		cy.get('button').contains('Login').click()

		cy.url().should('include', '/confirm')
	})
})
