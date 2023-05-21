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
