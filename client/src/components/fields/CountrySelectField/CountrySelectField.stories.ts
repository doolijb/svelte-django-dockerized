import type {Meta} from "@storybook/svelte"
import type {ComponentType} from "svelte"
import Component from "."
import baseMeta from "@components/fields/BaseSearchSelectField/BaseSearchSelectField.stories"

const meta: Meta<typeof Component> = {
    component: Component as ComponentType,
    tags: ["autodocs"],
    decorators: [],
    argTypes: {
        ...baseMeta.argTypes
    }
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

export const WithValue = {
    render: Template,
    args: {
        value: "US"
    }
}
