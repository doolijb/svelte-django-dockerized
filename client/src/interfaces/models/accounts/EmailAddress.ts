export interface IEmailAddress {
    id: string // UUID
    email: string
    isPrimary?: boolean
    isVerified?: boolean
    emailable_type: string | null
    emailable_id: string | null
    created_at: string
    updated_at: string | null
}

/**
 * Minimal EmailAddress example, i.e. viewing publicly available data
 */
const minimal: IEmailAddress = {
    id: "abc-456-789",
    email: "john.doe@example.com",
    emailable_type: "User",
    emailable_id: "123-123-456",
    created_at: "2021-01-01T00:00:00.000Z",
    updated_at: null
}

/**
 * Example EmailAddress, i.e. viewing publicly available data
 * with all fields filled out
 */
const example: IEmailAddress = {
    ...minimal,
    isPrimary: true,
    isVerified: true,
    updated_at: "2021-01-01T00:00:00.000Z"
}

export const exampleEmailAddresses = {
    minimal,
    example
}
