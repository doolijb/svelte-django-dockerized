import Component from "."
import {TableDataDecorator} from "@decorators"
import type {Meta} from "@storybook/svelte"


const meta: Meta<typeof Component> = {
    // Automatically generate the component name as "Table cells/BoolCell"

    component: Component as any,
    tags: ["autodocs"],
    decorators: [() => TableDataDecorator as any],
    argTypes: {
        // @ts-ignore - Works as is
        value: {
            description: "The value to display",
            options: [true, false, null],
            control: {
                type: "select"
            }
        },
        title: {
            description:
                "The title to display when hovering, defaults to value",
            control: {
                type: "text"
            }
        }
    }
}

export default meta

const Template = (args: {value: boolean}) => ({
    Component,
    props: args
})

export const False = {
    render: Template,
    args: {
        value: false
    }
}

export const Null = {
    render: Template,
    args: {
        value: null
    }
}

export const True = {
    render: Template,
    args: {
        value: true
    }
}
