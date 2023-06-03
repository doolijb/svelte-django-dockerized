import Component from "."
import {TableDataDecorator} from "@decorators"
import {faker} from "@faker-js/faker"
import type {Meta} from "@storybook/svelte"


const meta: Meta<typeof Component> = {
    // Automatically generate the component name as "Table cells/BoolCell"

    component: Component as any,
    tags: ["autodocs"],
    decorators: [() => TableDataDecorator as any],
    argTypes: {
        // @ts-ignore
        title: {
            description: "The text to display on hover",
            controls: {
                type: "text"
            }
        },
        onClick: {
            description: "The function to call when the button is clicked",
            action: "clicked"
        },
        disabled: {
            description: "Whether the button is disabled",
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
    args: {}
}
