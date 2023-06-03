import Component from "."
import {requiredValidator} from "@validators"
import type {AutocompleteOption} from "@skeletonlabs/skeleton"
import type {Meta} from "@storybook/svelte"
import type {ComponentType} from "svelte"


const meta: Meta<typeof Component> = {
    argTypes: {

        disabled: {
            control: {
                type: "boolean"
            }
        },
        // @ts-ignore-next-line
        label: {
            control: {
                type: "text"
            }
        },
        options: {
            control: {
                type: "object"
            }
        },
        placeholder: {
            control: {
                type: "text"
            }
        },
        validators: {
            control: {
                type: "object"
            }
        },
        value: {
            control: {
                type: "text"
            }
        }
    },
    component: Component as ComponentType,
    decorators: [],
    tags: ["autodocs"]
}

export default meta

const Template = (args: {value: boolean}) => ({
    Component,
    props: args
})

const validators = [requiredValidator()]
const options: AutocompleteOption[] = [
    {label: "Option 1", value: "Value 1"},
    {label: "Option 2", value: "Value 2"},
    {label: "Option 3", value: "Value 3"}
]

export const Disabled = {
    args: {
        disabled: true,
        options
    },
    render: Template
}

export const Example = {
    args: {
        options
    },
    render: Template
}

export const WithValidators = {
    args: {
        options,
        validators,
    },
    render: Template
}

export const WithValue = {
    args: {
        options,
        value: "Value 2"
    },
    render: Template
}
