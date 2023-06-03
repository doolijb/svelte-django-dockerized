import { makePopup } from "."
import type { IFieldValidator } from "@interfaces"

export default function (
    args: { label?: string; count: number } = { count: 1 }
): IFieldValidator { return {
    args,
    badge: "Uppercase Required",
    key: "uppercaseRequired",
    message: `Must have at least ${args.count} uppercase letter${args.count > 1 ? "s" : ""
    }`,
    popup: makePopup(),
    sticky: false,
    test: (value: string) => {
        const uppercase = value.match(/[A-Z]/g) || []
        return value ? uppercase && uppercase.length >= args.count : true
    }
}}
