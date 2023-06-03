import Component from "."
import baseTextInputMeta from "@components/fields/BaseTextInput/BaseTextInput.stories"
// get country codes from phone number lib
import { countries } from "@data"
import { faker } from "@faker-js/faker"
import type { Meta } from "@storybook/svelte"
import type { ComponentType } from "svelte"


const meta: Meta<typeof Component> = {
    ...baseTextInputMeta,
    component: Component as ComponentType,
    argTypes: {
        ...baseTextInputMeta.argTypes,
        country: {
            type: {
                name: "string",
                required: false
            },
            control: {
                type: "select",
                options: Object.keys(countries)
            }
        },
        readonlyCountry: {
            type: {
                name: "boolean",
                required: false
            },
            control: {
                type: "boolean"
            }
        }
    } as any
}

export default meta

const Template = (args: { value: boolean }) => ({
    Component,
    props: args
})

export const Disabled = {
    render: Template,
    args: {
        value: faker.phone.number("##########"),
        disabled: true
    }
}

export const Empty = {
    render: Template,
    args: {}
}

export const Filled = {
    render: Template,
    args: {
        value: faker.phone.number("##########")
    }
}

export const ReadOnlyCountry = {
    render: Template,
    args: {
        value: faker.phone.number("##########"),
        country: "US",
        readonlyCountry: true
    }
}
