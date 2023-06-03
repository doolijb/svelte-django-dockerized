import { makePopup } from "."
import { sentenceCase } from "change-case"
import type { IFieldValidator } from "@interfaces"

export default function (
    args: { label?: string; getMatchValue: () => string } = {
        getMatchValue: null as () => string
    }
): IFieldValidator {
    if (!args.getMatchValue) {
        throw new Error(
            "confirmMatchValidator requires a getMatchValue function"
        )
    }
    return {
        args,
        badge: `${args.label ? sentenceCase(args.label) + "s" : "Values"
        } Match`,
        key: "confirmMatch",
        message: `The ${args.label ? args.label.toLowerCase() + "s" : "values"
        } entered does not match, please try again`,
        popup: makePopup(),
        sticky: false,
        test: (value: string) => {
            const matchValue = args.getMatchValue()
            return value ? matchValue && value === matchValue : true
        }
    }
}
