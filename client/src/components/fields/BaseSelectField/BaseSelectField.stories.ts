import type {Meta} from "@storybook/svelte"
import type {ComponentType} from "svelte"
import Component from "."

const meta: Meta<typeof Component> = {
    component: Component as ComponentType,
    tags: ["autodocs"],
    decorators: [],
    argTypes: {}
}

export default meta

const Template = (args: {value: boolean}) => ({
    Component,
    props: args
})

export const Example = {
    render: Template,
    args: {
        // Component Props Here
    }
}
