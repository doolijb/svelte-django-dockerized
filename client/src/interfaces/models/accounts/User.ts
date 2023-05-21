export interface IUser {
    id: string
    username: string
    firstName?: string
    lastName?: string
    isAdmin?: boolean
    created_at?: string
    updated_at?: string
}

const minimalUser: IUser = {
    id: "123-456-789",
    username: "johndoe"
}

const exampleUser: IUser = {
    ...minimalUser,
    firstName: "John",
    lastName: "Doe",
    isAdmin: false,
    created_at: "2021-01-01T00:00:00.000Z",
    updated_at: "2021-01-01T00:00:00.000Z"
}

export const examples = {
    minimalUser,
    exampleUser
}
