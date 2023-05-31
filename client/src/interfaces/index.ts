import type {PopupSettings} from "@skeletonlabs/skeleton"

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

export interface ICountryCode {
    readonly name: string
    readonly code: string
    readonly dialCode: string
    readonly keywords: string[]
    readonly getRegionCodes: () => Map<string, IRegionCode>
}

export interface IRegionCode {
    readonly name: string
    readonly code: string
    readonly keywords: string[]
    readonly getCountryCode: () => ICountryCode
}
