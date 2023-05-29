import type {Meta} from "@storybook/svelte"
import Component from "."
import type {ComponentType} from "svelte"
import {
    requiredValidator,
    minLengthValidator,
    maxLengthValidator,
    specialCharValidator
} from "@validators"

const meta: Meta<typeof Component> = {
    component: Component as ComponentType,
    tags: ["autodocs"],
    decorators: [],
    argTypes: {
        label: {
            type: {
                name: "string",
                required: false
            }
        },
        type: {
            type: {
                name: "string",
                required: false
            },
            control: {
                type: "select",
                options: ["text", "password", "email", "number"]
            }
        },
        validators: {
            type: {
                name: "array",
                required: false
            }
        },
        value: {
            type: {
                name: "string",
                required: false
            }
        },
        placeholder: {
            type: {
                name: "string",
                required: false
            }
        },
        disabled: {
            type: {
                name: "boolean",
                required: false
            }
        },
        errors: {
            type: {
                name: "array",
                required: false
            }
        },
        onInput: {
            action: "onInput",
            table: {
                disable: true
            }
        },
        onFocus: {
            action: "onFocus",
            table: {
                disable: true
            }
        },
        onBlur: {
            action: "onBlur",
            table: {
                disable: true
            }
        }
    } as any
}

export default meta

const Template = (args: {value: boolean}) => ({
    Component,
    props: args
})

export const Empty = {
    render: Template,
    args: {
        // Component Props Here
    }
}

export const Filled = {
    render: Template,
    args: {
        value: "Hello World"
    }
}

export const Disabled = {
    render: Template,
    args: {
        value: "Hello World",
        disabled: true
    }
}

export const WithPlaceholder = {
    render: Template,
    args: {
        placeholder: "Enter your name"
    }
}

export const WithValidators = {
    render: Template,
    args: {
        validators: [
            requiredValidator(),
            minLengthValidator(),
            maxLengthValidator(),
            specialCharValidator()
        ]
    }
}

export const FilledWithValidators = {
    render: Template,
    args: {
        value: "Hello World",
        validators: [
            requiredValidator(),
            minLengthValidator(),
            maxLengthValidator(),
            specialCharValidator()
        ]
    }
}
