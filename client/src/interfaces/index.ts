import type {PopupSettings} from "@skeletonlabs/skeleton"

export * from "./models"

export interface FieldValidator {
    key: string
    badge: string
    sticky: boolean
    message: string
    popup: PopupSettings
    test: (value: any) => boolean
}
