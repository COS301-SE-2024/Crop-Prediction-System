describe('Signup Page', () => {
	beforeEach(() => {
		cy.visit('/signup')
	})

	it('should display the signup form', () => {
		cy.get('h1').should('contain', 'Sign up')
		cy.get('#email').should('be.visible')
		cy.get('input[type="password"]').should('have.length', 2)
	})

	it('should enable the sign up button when passwords match', () => {
		const email = `test${Date.now()}@example.com`
		const password = 'Password123!'

		cy.get('#email').clear().type(email)

		// Ensure the first password input is visible and not obstructed
		cy.get('input[type="password"]').first().should('be.visible').clear().type(password)

		// Click outside to remove any covering elements
		cy.get('body').click(0, 0)

		// Ensure the second password input is visible and not obstructed
		cy.get('input[type="password"]').last().should('be.visible').clear().type(password)
		cy.get('button').contains('Sign up').should('not.be.disabled')
	})

	it('should sign up successfully', () => {
		const email = `test${Date.now()}@example.com`
		const password = 'Password123!'

		cy.get('#email').clear().type(email)

		// Ensure the first password input is visible and not obstructed
		cy.get('input[type="password"]').first().should('be.visible').clear().type(password)

		// Click outside to remove any covering elements
		cy.get('body').click(0, 0)
		cy.get('body').click(0, 0)

		// Ensure the second password input is visible and not obstructed
		cy.get('input[type="password"]').last().should('be.visible').clear().type(password)

		cy.get('button').contains('Sign up').click()

		cy.get('small').contains('Check your email to confirm your account.').should('be.visible')
	})

	it('should sign in with Google OAuth', () => {
		cy.get('button') // Use a more specific selector if necessary
			.find('span.pi.pi-google') // Find the icon
			.should('be.visible') // Ensure the icon is visible
			.click({ force: true })
	})

	it('should navigate to the login page', () => {
		cy.get('small')
			.contains('Already have an account?')
			.find('a') // Find the link element
			.should('have.attr', 'href', '/login') // Check that the href attribute is correct
			.click() // Click the link
		cy.url().should('include', '/login') // Verify that the URL includes /login
	})
})
