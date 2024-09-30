describe('Manage Fields Page', () => {
	beforeEach(() => {
	  cy.login('ggu.capstone@gmail.com', 'Testing1234#')
      cy.wait(6000)
	    cy.get('button[aria-label="Filter"]').click();
        cy.wait(500);
		cy.get('span[class="pi pi-pen-to-square pl-4"]').click();
	});
  
	it('can train individual field', () => {
		cy.wait(3000);
		cy.get('button[aria-label="Train"]').first().click();
	});

    it('can train all fields', () => {
		cy.wait(3000);
		cy.get('button[aria-label="Train All"]').click();
	});

    it('can search for a field', () => {
		cy.wait(3000);
		cy.get('input[data-pc-name="inputtext"]').clear().type('Test Field')
        cy.contains('h2', 'Test Field').should('be.visible'); 
	});

    it('can filter by crop type', () => {
		cy.wait(3000);
		cy.get('svg[data-pc-section="dropdownicon"]').click();
        cy.contains('li', 'Maize') 
		.scrollIntoView()
		.should('be.visible')
		.click();

        cy.get('span strong').contains('Crop Type:').parent().should('contain', 'Maize');
        cy.get('span strong').contains('Crop Type:').parent().should('not.contain', 'Wheat');

        
	}); 
});