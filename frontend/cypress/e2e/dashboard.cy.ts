describe('Dashboard', () => {
    beforeEach(() => {
      cy.login('ggu.capstone@gmail.com', 'Test1234#')
      cy.visit('/')
    })
  
    it('should display the Field Card and Map components', () => {
      cy.get('.w-full.md\\:w-1\\/3').should('exist')
      cy.get('.w-full.md\\:w-2\\/3').should('exist')
    })
  
    it('should select an option from the dropdown and update the graphs', () => {
      cy.get('#pv_id_1').click()
      cy.get('#pv_id_1_list').should('be.visible')
      cy.get('#pv_id_1_list').contains('Wheat 3').click()
  
      cy.get('legend').click()
    })
  })