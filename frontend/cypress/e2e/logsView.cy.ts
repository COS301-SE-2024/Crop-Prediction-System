describe('Manage Fields Page', () => {
	beforeEach(() => {
	  cy.login('ggu.capstone@gmail.com', 'Testing1234#')
      cy.wait(6000)
	    cy.get('button[aria-label="Filter"]').click();
        cy.wait(500);
		cy.get('span[class="pi pi-list pl-4"]').click();
	});

    it('can sort based on attributes', () => {
		cy.wait(6000);
		cy.contains('span[data-pc-section="headertitle"]', 'Min Temp (°C)').click();
        cy.get('tbody tr:first-child td:nth-child(6)')
        .should('contain', '9.19')
        .and('be.visible');
	});

    it('can edit field data', () => {
		cy.wait(6000);
		cy.contains('span[data-pc-section="headertitle"]', 'Min Temp (°C)').click();
        cy.get('tbody tr:first-child td:nth-child(6)')
        .should('contain', '9.19')
        .and('be.visible');

        cy.wait(500)
        cy.get('tbody tr:first-child td:nth-child(6)')
        .click()
        .type('{selectAll}{backspace}')
        .type('9.10{enter}');
	});

    it('can generate Field Report', () => {
		cy.wait(6000);
		// cy.contains('button[aria-label="Generate Field Report"]').click();
        cy.get('span[class="pi pi-chart-line mx-0 mr-2"]').click();

        cy.wait(500);
		cy.get('svg[data-pc-section="dropdownicon"]').eq(1).click();
        cy.contains('li',  'Test Field') 
		.scrollIntoView()
		.should('be.visible')
		.click();

        cy.wait(500);
        cy.contains('span[data-pc-section="label"]', 'Print').parents('button').click();
	});


});