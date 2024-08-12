describe('Visit Signup Page', () => {
  it('successfully loads', () => {
    cy.visit('/signup')
    cy.contains('Sign up')  // Adjust according to your actual page content
  })
})
