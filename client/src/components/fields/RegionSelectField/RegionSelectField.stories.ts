import Component from "."
import baseMeta from "@components/fields/BaseSearchSelectField/BaseSearchSelectField.stories"
import type { Meta } from "@storybook/svelte"
import type { ComponentType } from "svelte"


const meta: Meta<typeof Component> = {
    component: Component as ComponentType,
    tags: ["autodocs"],
    decorators: [],
    argTypes: {
        ...baseMeta.argTypes
    }
}

export default meta

const Template = (args: { value: boolean }) => ({
    Component,
    props: args
})

export const CAProvinces = {
    render: Template,
    args: {
        countryCode: "CA"
    }
}

export const CNProvinces = {
    render: Template,
    args: {
        countryCode: "CN"
    }
}

export const Disabled = {
    render: Template,
    args: {
        countryCode: "US",
        disabled: true
    }
}

export const UAOblasts = {
    render: Template,
    args: {
        countryCode: "UA"
    }
}

export const UMIslands = {
    render: Template,
    args: {
        countryCode: "UM"
    }
}

export const USStates = {
    render: Template,
    args: {
        countryCode: "US"
    }
}

export const WithValue = {
    render: Template,
    args: {
        countryCode: "US",
        value: "US-CA"
    }
}
