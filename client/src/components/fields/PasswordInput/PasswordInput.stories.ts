import Component from "."
import baseTextInputMeta from "@components/fields/BaseTextInput/BaseTextInput.stories"
import {faker} from "@faker-js/faker"
import type {Meta} from "@storybook/svelte"
import type {ComponentType} from "svelte"


const meta: Meta<typeof Component> = {
    ...baseTextInputMeta,
    component: Component as ComponentType
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
