import type {PopupSettings} from "@skeletonlabs/skeleton"
import {v4 as uuidv4} from "uuid"

export const makePopup: () => PopupSettings = () => ({
    event: "hover",
    target: uuidv4(),
    placement: "top"
})

export const requiredValidator = () => ({
    key: "required",
    badge: "Required",
    sticky: true,
    message: "This field is required",
    popup: makePopup(),
    test: (value: any) =>
        !value || value === undefined || value === null || value === ""
})

export const minLengthValidator = (minLen = 3) => ({
    key: "minLength",
    badge: "Min length",
    sticky: false,
    message: `This field must be at least ${minLen} characters long`,
    popup: makePopup(),
    test: (value: any) => value && value.length < minLen
})

export const maxLengthValidator = (maxLen = 20) => ({
    key: "maxLength",
    badge: "Max length",
    sticky: false,
    message: `This field must be at most ${maxLen} characters long`,
    popup: makePopup(),
    test: (value: any) => value && value.length > maxLen
})

export const specialCharValidator = () => ({
    key: "specialChar",
    badge: "Special characters",
    sticky: false,
    message: "This field must not contain spaces or special characters",
    popup: makePopup(),
    test: (value: any) => value && !/^[a-zA-Z0-9_]+$/.test(value)
})

export const emailValidator = () => ({
    key: "email",
    badge: "Email",
    sticky: false,
    message: "This field must be a valid email address",
    popup: makePopup(),
    test: (value: any) =>
        value && !/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i.test(value)
})

export const numberRequiredValidator = (count = 1) => ({
    key: "numberRequired",
    badge: "Number Required",
    sticky: false,
    message: `This field must have at least ${count} number${
        count > 1 ? "s" : ""
    }`,
    popup: makePopup(),
    test: (value: any) => {
        const numbers = value.match(/\d/g) || []
        return value && numbers && numbers.length < count
    }
})

export const uppercaseRequiredValidator = (count = 1) => ({
    key: "uppercaseRequired",
    badge: "Uppercase Required",
    sticky: false,
    message: `This field must have at least ${count} uppercase letter${
        count > 1 ? "s" : ""
    }`,
    popup: makePopup(),
    test: (value: any) => {
        const uppercase = value.match(/[A-Z]/g) || []
        return value && uppercase && uppercase.length < count
    }
})

export const lowercaseRequiredValidator = (count = 1) => ({
    key: "lowercaseRequired",
    badge: "Lowercase Required",
    sticky: false,
    message: `This field must have at least ${count} lowercase letter${
        count > 1 ? "s" : ""
    }`,
    popup: makePopup(),
    test: (value: any) => {
        const lowercase = value.match(/[a-z]/g) || []
        return value && lowercase && lowercase.length < count
    }
})

export const specialCharRequiredValidator = (
    count = 1,
    choices = [
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
    ]
) => ({
    key: "specialCharRequired",
    badge: "Special Character Required",
    sticky: false,
    message: `This field must have at least ${count} special character${
        count > 1 ? "s" : ""
    }, such as ${choices.join(", ")}`,
    popup: makePopup(),
    test: (value: any) => {
        const escaped_chars = choices.map(char => "\\" + char).join("")
        const regex = new RegExp("[" + escaped_chars + "]", "g")
        const specialChars = value.match(regex) || []
        return value && specialChars && specialChars.length < count
    }
})
