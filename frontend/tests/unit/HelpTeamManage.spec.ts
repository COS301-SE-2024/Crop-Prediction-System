// @vitest-environment nuxt
import { mount } from '@vue/test-utils'
import { it, expect, describe, beforeEach, vi } from 'vitest'
import TeamManagementHelp from '~/components/HelpTeamManage.vue'

// Mock the DataTable and Card components
vi.mock('primevue/datatable', () => ({
  default: {
    name: 'DataTable',
    template: '<div><slot /></div>',
    props: ['value', 'responsiveLayout', 'tableStyle', 'columnResizeMode', 'class'],
  },
}))

vi.mock('primevue/card', () => ({
  default: {
    name: 'Card',
    template: '<div><slot name="content" /></div>',
    props: ['class'],
  },
}))

vi.mock('primevue/button', () => ({
  default: {
    name: 'Button',
    template: '<button><slot /></button>',
    props: ['label', 'icon', 'class', 'outlined', 'severity', 'size'],
  },
}))

vi.mock('primevue/dialog', () => ({
  default: {
    name: 'Dialog',
    template: '<div><slot /></div>',
    props: ['header', 'modal', 'modelValue', 'style'],
  },
}))

vi.mock('primevue/inputtext', () => ({
  default: {
    name: 'InputText',
    template: '<input />',
    props: ['id', 'placeholder', 'class'],
  },
}))

vi.mock('primevue/dropdown', () => ({
  default: {
    name: 'Dropdown',
    template: '<select><slot /></select>',
    props: ['options', 'optionLabel', 'placeholder', 'class'],
  },
}))

describe('HelpTeamManage.vue', () => {
  let wrapper

  beforeEach(() => {
    wrapper = mount(TeamManagementHelp, {
      props: { activeIndex: 5 },
    })
  })

  it('mounts the component', () => {
    expect(wrapper.exists()).toBe(true)
  })

  it('renders the main heading', () => {
    const heading = wrapper.find('h1')
    expect(heading.exists()).toBe(true)
    expect(heading.text()).toBe('Team Management Help')
  })

  it('renders the "Viewing Team Members" section', () => {
    const sectionHeading = wrapper.findAll('h2').at(0)
    expect(sectionHeading.text()).toBe('Viewing Team Members')
    expect(wrapper.text()).toContain('The table below displays all the members of your team:')
  })

  it('renders the "Editing Member Roles" section', () => {
    const sectionHeading = wrapper.findAll('h2').at(1)
    expect(sectionHeading.text()).toBe('Editing Member Roles')
    expect(wrapper.text()).toContain('To edit a member\'s role:')
  })

  it('renders the "Inviting New Members" section', () => {
    const sectionHeading = wrapper.findAll('h2').at(2)
    expect(sectionHeading.text()).toBe('Inviting New Members')
    expect(wrapper.text()).toContain('To invite a new member to your team:')
  })

  it('renders the "Removing Members" section', () => {
    const sectionHeading = wrapper.findAll('h2').at(3)
    expect(sectionHeading.text()).toBe('Removing Members')
    expect(wrapper.text()).toContain('To remove a member from your team:')
  })

  it('renders the "Permissions" section', () => {
    const sectionHeading = wrapper.findAll('h2').at(4)
    expect(sectionHeading.text()).toBe('Permissions')
    expect(wrapper.text()).toContain('Only users with the Farm Manager role can perform the following actions:')
  })

  it('renders the "Success Message" section', () => {
    const sectionHeading = wrapper.findAll('h2').at(5)
    expect(sectionHeading.text()).toBe('Success Message')
    expect(wrapper.text()).toContain('After performing an action, a success message will appear confirming that the action has been completed.')
  })
})
