import withNuxt from './.nuxt/eslint.config.mjs'

export default withNuxt({
	files: ['**/*.{js,ts,vue}'],
	rules: {
		'no-dupe-keys': 'off',
		'no-unused-vars': 'off',
		'vue/multi-word-component-names': 'off',
		'vue/html-self-closing': 'off',
		'vue/no-reserved-component-names': 'off',
		'vue/attribute-hyphenation': 'off',
		'vue/v-on-event-hyphenation': 'off',
		'vue/attributes-order': 'off',
		'@typescript-eslint/no-unused-vars': 'off',
		'vue/no-multiple-template-root': 'off',
		'@typescript-eslint/no-explicit-any': 'off',
		'prefer-const': 'off',
		'@typescript-eslint/no-extraneous-class': 'off',
	},
})
