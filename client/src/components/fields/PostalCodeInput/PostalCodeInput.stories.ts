import type { Meta } from "@storybook/svelte"
import Component from "."
import type { ComponentType } from "svelte"
import baseTextInputMeta from "@components/fields/BaseTextInput/BaseTextInput.stories"
import { faker } from "@faker-js/faker"

const meta: Meta<typeof Component> = {
    component: Component as ComponentType,
    argTypes: {
        ...baseTextInputMeta.argTypes,
        countryCode: {
            type: {
                name: "string",
                required: false
            },
        }
    } as any
}

export default meta

const Template = (args: { value: boolean }) => ({
    Component,
    props: args
})


export const Example = {
    render: Template,
}

export const USFilled = {
    render: Template,
    args: {
        // fake postal code
        value: faker.address.zipCode("#####"),
        countryCode: "US"
    }
}

export const USFilledLong = {
    render: Template,
    args: {
        value: faker.address.zipCode("#########"),
        countryCode: "US"
    }
}


export const CAFilled = {
    render: Template,
    args: {
        value: faker.address.zipCode("A#A #A#"),
        countryCode: "CA"
    }
}

export const CAFilledLong = {
    render: Template,
    args: {
        value: faker.address.zipCode("A#A #A#A"),
        countryCode: "CA"
    }
}

export const Invalid = {
    render: Template,
    args: {
        value: "12345",
        countryCode: "CA"
    }
}

export const disabled = {
    render: Template,
    args: {
        value: faker.address.zipCode("A#A #A#A"),
        countryCode: "CA",
        disabled: true
    }
}
