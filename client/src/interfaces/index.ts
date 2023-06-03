import type { PopupSettings } from "@skeletonlabs/skeleton"

export * from "./models"

export interface IFieldValidator {
    args: object
    key: string
    badge: string
    sticky: boolean
    message: string
    popup: PopupSettings
    test: (value: any) => boolean
}

export interface ICountry {
    readonly name: string
    readonly code: string
    readonly dialCode: string
    readonly keywords: string[]
    readonly regionTitle?: string
    readonly postalCodeTitle?: string
    readonly getRegions: () => Map<string, IRegion>
}

export interface IRegion {
    readonly name: string
    readonly code: string
    readonly keywords: string[]
    readonly getCountry: () => ICountry
}
