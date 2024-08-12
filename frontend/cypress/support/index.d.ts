// cypress/support/index.d.ts

if (process.env.NODE_ENV === 'test') {
	window.__VUE_DEVTOOLS_GLOBAL_HOOK__ = {
		Vue: null,
	}
}

declare namespace Cypress {
	interface Chainable {
		login(email: string, password: string): Chainable<void>
	}
}
