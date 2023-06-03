import Component from "."
import {ReviewModes} from "@constants"
import {examples} from "@interfaces"
import type {Meta} from "@storybook/svelte"


const meta: Meta<typeof Component> = {
    // Automatically generate the component name as "Table cells/BoolCell"
    component: Component as any,
    tags: ["autodocs"],
    decorators: [],
    argTypes: {
        // @ts-ignore - Works as is
        user: {
            description: "User object",
            control: {
                type: "object"
            },
            mode: {
                description: "Review mode",
                control: {
                    type: "select",
                    options: Object.values(ReviewModes)
                }
            }
        }
    }
}

export default meta

const Template = (args: any) => ({
    Component,
    props: args
})

export const Create = {
    render: Template,
    args: {
        value: ReviewModes.CREATE
    }
}

export const Edit = {
    render: Template,
    args: {
        user: examples.exampleUser,
        value: ReviewModes.EDIT
    }
}

export const View = {
    render: Template,
    args: {
        user: examples.exampleUser,
        mode: ReviewModes.VIEW
    }
}
