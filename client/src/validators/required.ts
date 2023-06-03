import { makePopup } from "."
import type { IFieldValidator } from "@interfaces"

export default function (
    args: { label?: string } = {}
): IFieldValidator {
    return {
        args,
        badge: "Required",
        key: "required",
        message: "This field is required",
        popup: makePopup(),
        sticky: true,
        test: (value: string) => !!value
    }
}
