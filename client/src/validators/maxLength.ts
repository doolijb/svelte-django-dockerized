import { makePopup } from "."
import type { IFieldValidator } from "@interfaces"

export default function (
    args: { label?: string; maxLen: number } = { maxLen: 20 }
): IFieldValidator { return {
    args,
    badge: "Max length",
    key: "maxLength",
    message: `Must be at most ${args.maxLen} characters long`,
    popup: makePopup(),
    sticky: false,
    test: (value: string) => (value ? value.length <= args.maxLen : true)
}}
