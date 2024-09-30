describe('Dashboard Page', () => {
	beforeEach(() => {
	  cy.login('ggu.capstone@gmail.com', 'Testing1234#')
	});
  
	it('displays related charts when field is selected', () => {
		cy.wait(5000)
		cy.get('svg[data-pc-section="dropdownicon"]').click();

		cy.contains('li', 'Test Field') 
		.scrollIntoView()
		.should('be.visible')
		.click();
	});

	it('displays additional charts when slected', () => {
		cy.wait(5000)
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
	});

	it('toggles sidebar', () => {
		cy.wait(5000)
		cy.get('button[aria-label="Filter"]').click();

		cy.get('div[data-pc-name="sidebar"]').should('exist').and('be.visible');
	});

	it('toggles navbar menu', () => {
		cy.wait(5000)
		cy.get('i.pi.pi-user').click();

		cy.get('div[data-pc-name="menu"]').should('exist').and('be.visible');
	});

	it('redirects to team chat', () => {
		cy.wait(500)
		cy.get('i.pi.pi-comment').click();

		cy.url().should('include', '/team/chat')
	});
  });
  