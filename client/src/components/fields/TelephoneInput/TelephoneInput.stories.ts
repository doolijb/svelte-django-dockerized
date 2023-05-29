import type {Meta} from "@storybook/svelte"
import Component from "."
import type {ComponentType} from "svelte"
import baseTextInputMeta from "@components/fields/BaseTextInput/BaseTextInput.stories"
import {faker} from "@faker-js/faker"
// get country codes from phone number lib
import {CountryCodes} from "@constants"

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
                options: Object.keys(CountryCodes)
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
    args: {}
}

export const Filled = {
    render: Template,
    args: {
        value: faker.phone.number("##########")
    }
}
