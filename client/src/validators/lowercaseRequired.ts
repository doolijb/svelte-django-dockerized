import { makePopup } from "."
import type { IFieldValidator } from "@interfaces"

export default function (
    args: { label?: string; count: number } = { count: 1 }
): IFieldValidator { return {
    args,
    badge: "Lowercase Required",
    key: "lowercaseRequired",
    message: `Must have at least ${args.count} lowercase letter${args.count > 1 ? "s" : ""
    }`,
    popup: makePopup(),
    sticky: false,
    test: (value: string) => {
        const lowercase = value.match(/[a-z]/g) || []
        return value ? lowercase && lowercase.length >= args.count : true
    }
}}
