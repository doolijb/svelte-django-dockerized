import {v4 as uuidv4} from "uuid"
import type { PopupSettings } from "@skeletonlabs/skeleton"

export default function (): PopupSettings {
    return {
        event: "hover",
        placement: "bottom",
        target: uuidv4()
    }
}
