
import {default as Icon} from "./Icon.svelte"
import {default as Popup} from "./Popup.svelte"
import {v4 as uuidv4} from "uuid"
import type {PopupSettings} from "@skeletonlabs/skeleton/index"

function makePopupSettings(): PopupSettings {
    return {
        // Represents the type of event that opens/closed the popup
        event: "click",
        // Matches the data-popup value on your popup element
        target: uuidv4(),
        // Defines which side of your trigger the popup will appear
        placement: "bottom"
    }
}

export default {
    Icon,
    Popup,
    makePopupSettings
}
