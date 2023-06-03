import type {Meta} from "@storybook/svelte"
import type {ComponentType} from "svelte"
import Component from "."
import {requiredValidator} from "@validators"
import type {AutocompleteOption} from "@skeletonlabs/skeleton"

const meta: Meta<typeof Component> = {
    component: Component as ComponentType,
    tags: ["autodocs"],
    decorators: [],
    argTypes: {
        // @ts-ignore-next-line
        label: {
            control: {
                type: "text"
            }
        },
        placeholder: {
            control: {
                type: "text"
            }
        },
        value: {
            control: {
                type: "text"
            }
        },
        validators: {
            control: {
                type: "object"
            }
        },
        options: {
            control: {
                type: "object"
            }
        },
        disabled: {
            control: {
                type: "boolean"
            }
        }
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
        options: [
            {label: "Option 1", value: "Value 1"},
            {label: "Option 2", value: "Value 2"},
            {label: "Option 3", value: "Value 3"}
        ] as AutocompleteOption[]
    }
}

export const WithValidators = {
    render: Template,
    args: {
        options: Example.args.options,
        validators: [requiredValidator()]
    }
}

export const WithValue = {
    render: Template,
    args: {
        ...WithValidators.args,
        value: "Value 2"
    }
}

export const Disabled = {
    render: Template,
    args: {
        ...WithValidators.args,
        disabled: true
    }
}
