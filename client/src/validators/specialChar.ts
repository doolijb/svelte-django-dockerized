import { makePopup } from "."
import type { IFieldValidator } from "@interfaces"

export default function (
    args: { label?: string } = {}
): IFieldValidator { return {
    args,
    badge: "Special characters",
    key: "specialChar",
    message: "Must not contain spaces or special characters",
    popup: makePopup(),
    sticky: false,
    test: (value: string) => (value ? /^[a-zA-Z0-9_]+$/.test(value) : true)
}}
