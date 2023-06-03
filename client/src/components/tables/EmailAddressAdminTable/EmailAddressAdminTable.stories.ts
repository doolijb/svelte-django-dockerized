import Component from "."
import {faker} from "@faker-js/faker"
import type {Meta} from "@storybook/svelte"
import type {IEmailAddress} from "src/interfaces"


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
    emailAddresses: new Map<string, IEmailAddress>(),
    pageCount: 10
}

// for range of 10, lets add examples.example to emailAddresses with fake ids
for (let i = 0; i < 10; i++) {
    const id = faker.datatype.uuid()
    Default.args.emailAddresses.set(id, {
        id: id,
        email: faker.internet.email(),
        isPrimary: faker.datatype.boolean(),
        isVerified: faker.datatype.boolean(),
        emailable_type: "user",
        emailable_id: faker.datatype.string(),
        created_at: faker.date.past().toISOString(),
        updated_at: faker.date.past().toISOString()
    })
}
