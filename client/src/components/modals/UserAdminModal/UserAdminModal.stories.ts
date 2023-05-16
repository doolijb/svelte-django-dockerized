import {examples} from "@interfaces"
import {ModalDecorator} from "@decorators"
import type {ModalSettings} from "@skeletonlabs/skeleton"
import {ReviewModes} from "@constants"
import Component from "./UserAdminModal.svelte"

const meta = {
    component: ModalDecorator,
    tags: ["autodocs"]
}

export default meta

const Template = (args: {value: boolean}) => ({
    ModalDecorator,
    props: args
})

export const Example = {
    render: Template,
    args: {
        registry: {
            modalComponentOne: {
                // ref: Component,
                // props: {
                //     user: examples.exampleUser,
                // },
                slot: "<p>Skeleton</p>"
            } as Record<string, any>
        },
        settings: {
            // type: 'component',
            title: "Manage User",
            component: "modalComponentOne"
        } as ModalSettings
    }
}
