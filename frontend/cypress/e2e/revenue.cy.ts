describe('Dashboard Page', () => {
	beforeEach(() => {
	  cy.login('ggu.capstone@gmail.com', 'Testing1234#')
      cy.wait(6000)
	    cy.get('button[aria-label="Filter"]').click();
        cy.wait(500);
		cy.get('span[class="pi pi-wallet pl-4"]').click();
	});

    it('should give error message for missing fiels', () => {
		cy.wait(3000);
        cy.get('svg[data-pc-section="dropdownicon"]').click();
        cy.contains('li', 'Sorghum') 
		.scrollIntoView()
		.should('be.visible')
		.click();
		cy.get('h2').should('contain', 'You have no registered Sorghum fields.').click();
	});
});