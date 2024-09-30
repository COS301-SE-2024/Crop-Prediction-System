describe('Dashboard Page', () => {
	beforeEach(() => {
	  cy.login('ggu.capstone@gmail.com', 'Testing1234#')
      cy.wait(6000)
	    cy.get('button[aria-label="Filter"]').click();
        cy.wait(500);
		cy.get('span[class="pi pi-comment pl-4"]').click();
	});

    it('can send a message', () => {
		cy.wait(3000);
		cy.wait(2000);
		cy.get('textarea').type('This is a Test.');
		cy.wait(2000);
		cy.get('span[class="pi pi-send mx-0"]').click();
	});
})