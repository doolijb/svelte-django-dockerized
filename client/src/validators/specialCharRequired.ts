import { makePopup } from "."
import type { IFieldValidator } from "@interfaces"

export default function (
    args: { label?: string },
    choices: [
        "!",
        "@",
        "#",
        "$",
        "%",
        "^",
        "&",
        "*",
        "(",
        ")",
        "-",
        "_",
        "=",
        "+",
        "[",
        "]",
        "{",
        "}",
        ";",
        ":",
        ",",
        ".",
        "<",
        ">",
        "?",
        "/",
        "|",
        "~",
        "`"
    ],
    count: 1
): IFieldValidator {
    return {
        args,
        badge: "Special Character Required",
        key: "specialCharRequired",
        message: `Must have at least ${count} special character${count > 1 ? "s" : ""
        }, such as ${choices.join(", ")}`,
        popup: makePopup(),
        sticky: false,
        test: (value: string) => {
            const escaped_chars = choices.map(char => "\\" + char).join("")
            const regex = new RegExp("[" + escaped_chars + "]", "g")
            const specialChars = value.match(regex) || []
            return value ? specialChars && specialChars.length >= count : true
        }
    }
}
