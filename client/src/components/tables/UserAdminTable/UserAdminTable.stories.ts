import Component from "."
import {faker} from "@faker-js/faker"
import type {Meta} from "@storybook/svelte"
import type {IUser} from "src/interfaces"


const meta: Meta<typeof Component> = {
    component: Component as any,
    tags: ["autodocs"],
    argTypes: {}
}

export default meta

const Template = ({...args}) => ({
    Component,
    props: args
})

export const Default = Template.bind({})

Default.args = {
    users: new Map<string, IUser>(),
    pageCount: 10
}

// for range of 10, lets add examples.example to emailAddresses with fake ids
for (let i = 0; i < 10; i++) {
    const id = faker.datatype.uuid()
    Default.args.users.set(id, {
        id: id,
        username: faker.internet.userName(),
        isAdmin: faker.datatype.boolean(),
        created_at: faker.date.past().toISOString(),
        updated_at: faker.date.past().toISOString()
    })
}
