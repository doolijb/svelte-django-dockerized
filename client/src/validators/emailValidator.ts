import makePopup from "./makePopup"
import type { IFieldValidator } from "@interfaces"

export default function (
    args: { label?: string } = {}
): IFieldValidator { return {
    args,
    badge: "Email",
    key: "email",
    message: "Must be a valid email address",
    popup: makePopup(),
    sticky: false,
    test: (value: string) =>
        value ? /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i.test(value) : true
}
}
