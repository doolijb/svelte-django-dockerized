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
        // @ts-ignore - Works as is
        text: {
            description: "The text to display",
            options: [true, false, null],
            control: {
                type: "text"
            }
        },
        copy: {
            description:
                "Content that will be copied to the clipboard, i.e. if text is truncated",
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

export const Empty = {
    render: Template,
    args: {
        text: ""
    }
}

export const NormalText = {
    render: Template,
    args: {
        text: faker.internet.email()
    }
}

export const TruncatedCopy = {
    render: Template,
    args: {
        text: 12345,
        copy: 1234567890
    }
}
