import type {Meta} from "@storybook/svelte"
import type {ComponentType} from "svelte"
import Component from "."
import {minLengthValidator, requiredValidator} from "@validators"

const meta: Meta<typeof Component> = {
    component: Component as ComponentType,
    tags: ["autodocs"],
    decorators: [],
    argTypes: {
        validators: {
            type: {
                name: "array",
                required: false
            }
        },
        errors: {
            type: {
                name: "array",
                required: false
            }
        }
    } as any
}

export default meta

const Template = (args: {value: boolean}) => ({
    Component,
    props: args
})

const required = requiredValidator()

export const Sticky = {
    render: Template,
    args: {
        validators: [required]
    }
}

export const StickyError = {
    render: Template,
    args: {
        validators: [required],
        errors: [required]
    }
}

const minLength = minLengthValidator({minLen: 5})

export const Multiple = {
    render: Template,
    args: {
        validators: [required, minLength],
        errors: [minLength]
    }
}
