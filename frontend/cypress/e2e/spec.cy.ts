describe.only('Demo', () => {
	before(() => {
		cy.login('ggu.capstone@gmail.com', 'Testing1234#')
		Cypress.on('uncaught:exception', (err, runnable) => {
			// Check for specific error messages to ignore
			if (
			  err.message.includes('userFields.value.forEach is not a function') ||
			  err.message.includes('Permissions check failed') ||
			  err.message.includes('Cannot read properties of null (reading \'email\')')
			) {
			  return false; // Returning false prevents the test from failing
			}
			// Return true for all other errors to let Cypress handle them
			return true;
		  });
	  
	})

	it('Demo', () => {

		cy.wait(6000)
		cy.get('button[aria-label="Filter"]').click();

		cy.wait(500);
		cy.get('span[class="pi pi-pen-to-square pl-4"]').click();

		cy.wait(3000);
		cy.get('button[aria-label="Train"]').first().click();

		cy.wait(2000);
		cy.get('button[aria-label="Filter"]').click();

		cy.wait(500);
		cy.get('span[class="pi pi-chart-bar pl-4"]').click();

		cy.wait(3000)
		cy.get('svg[data-pc-section="dropdownicon"]').click();

		cy.contains('li', 'Test Field') 
		.scrollIntoView()
		.should('be.visible')
		.click();

		cy.get('svg[data-pc-section="togglericon"]')
		.scrollIntoView()
		.should('be.visible')
		.click();

		cy.wait(2000);
		cy.scrollTo('bottom', { duration: 2000 });
		cy.wait(2000);
		cy.scrollTo('top', { duration: 2000 });

		cy.get('i.pi.pi-comment').click();

		cy.wait(2000);
		cy.get('textarea').type('This is epic!');
		cy.wait(2000);
		cy.get('span[class="pi pi-send mx-0"]').click();

		cy.wait(2000)
		cy.get('i.pi.pi-user').click();

		cy.wait(500);
		cy.get('span[class="pi pi-sun"]').click();

		cy.wait(500);
		cy.get('span[class="pi pi-question-circle"]').click();

		cy.scrollTo('bottom', { duration: 2000 });
		cy.wait(2000);
		cy.scrollTo('top', { duration: 2000 });

		cy.get('button[aria-label="Filter"]').click();
		cy.wait(500);
		cy.get('span[class="pi pi-user"]').click();
		cy.scrollTo('top', { duration: 100 });

		cy.wait(500);
		cy.get('span.pi.pi-sign-out')
		.click();
	})
})
