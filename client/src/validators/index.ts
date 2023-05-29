/* eslint-disable @typescript-eslint/no-unused-vars */
import type {PopupSettings} from "@skeletonlabs/skeleton"
import {get} from "svelte/store"
import {v4 as uuidv4} from "uuid"
import {sentenceCase} from "change-case"
import parsePhoneNumber, {type CountryCode} from "libphonenumber-js"
import type {IFieldValidator} from "@interfaces"

export const makePopup: () => PopupSettings = () => ({
    event: "hover",
    target: uuidv4(),
    placement: "bottom"
})

export const requiredValidator = (
    args: {label?: string} = {}
): IFieldValidator => ({
    args,
    key: "required",
    badge: "Required",
    sticky: true,
    message: "This field is required",
    popup: makePopup(),
    test: (value: string) =>
        !!value || value === undefined || value === null || value === ""
})

export const minLengthValidator = (
    args: {label?: string; minLen: number} = {minLen: 3}
): IFieldValidator => ({
    args,
    key: "minLength",
    badge: "Min length",
    sticky: false,
    message: `Must be at least ${args.minLen} characters long`,
    popup: makePopup(),
    test: (value: string) => (value ? value.length >= args.minLen : true)
})

export const maxLengthValidator = (
    args: {label?: string; maxLen: number} = {maxLen: 20}
): IFieldValidator => ({
    args,
    key: "maxLength",
    badge: "Max length",
    sticky: false,
    message: `Must be at most ${args.maxLen} characters long`,
    popup: makePopup(),
    test: (value: string) => (value ? value.length <= args.maxLen : true)
})

export const specialCharValidator = (
    args: {label?: string} = {}
): IFieldValidator => ({
    args,
    key: "specialChar",
    badge: "Special characters",
    sticky: false,
    message: "Must not contain spaces or special characters",
    popup: makePopup(),
    test: (value: string) => (value ? /^[a-zA-Z0-9_]+$/.test(value) : true)
})

export const emailValidator = (
    args: {label?: string} = {}
): IFieldValidator => ({
    args,
    key: "email",
    badge: "Email",
    sticky: false,
    message: "Must be a valid email address",
    popup: makePopup(),
    test: (value: string) =>
        value ? /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i.test(value) : true
})

export const numberRequiredValidator = (
    args: {label?: string; count: number} = {count: 1}
): IFieldValidator => ({
    args,
    key: "numberRequired",
    badge: "Number Required",
    sticky: false,
    message: `Must have at least ${args.count} number${
        args.count > 1 ? "s" : ""
    }`,
    popup: makePopup(),
    test: (value: string) => {
        const numbers = value.match(/\d/g) || []
        return value ? numbers && numbers.length >= args.count : true
    }
})

export const uppercaseRequiredValidator = (
    args: {label?: string; count: number} = {count: 1}
): IFieldValidator => ({
    args,
    key: "uppercaseRequired",
    badge: "Uppercase Required",
    sticky: false,
    message: `Must have at least ${args.count} uppercase letter${
        args.count > 1 ? "s" : ""
    }`,
    popup: makePopup(),
    test: (value: any) => {
        const uppercase = value.match(/[A-Z]/g) || []
        return value ? uppercase && uppercase.length >= args.count : true
    }
})

export const lowercaseRequiredValidator = (
    args: {label?: string; count: number} = {count: 1}
): IFieldValidator => ({
    args,
    key: "lowercaseRequired",
    badge: "Lowercase Required",
    sticky: false,
    message: `Must have at least ${args.count} lowercase letter${
        args.count > 1 ? "s" : ""
    }`,
    popup: makePopup(),
    test: (value: any) => {
        const lowercase = value.match(/[a-z]/g) || []
        return value ? lowercase && lowercase.length >= args.count : true
    }
})

export const specialCharRequiredValidator = (
    args: {label?: string; count: number; choices: string[]} = {
        count: 1,
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
        ]
    }
): IFieldValidator => ({
    args,
    key: "specialCharRequired",
    badge: "Special Character Required",
    sticky: false,
    message: `Must have at least ${args.count} special character${
        args.count > 1 ? "s" : ""
    }, such as ${args.choices.join(", ")}`,
    popup: makePopup(),
    test: (value: string) => {
        const escaped_chars = args.choices.map(char => "\\" + char).join("")
        const regex = new RegExp("[" + escaped_chars + "]", "g")
        const specialChars = value.match(regex) || []
        return value ? specialChars && specialChars.length >= args.count : true
    }
})

export const confirmMatchValidator = (
    args: {label?: string; getMatchValue: () => string} = {
        getMatchValue: null as () => string
    }
): IFieldValidator => {
    if (!args.getMatchValue) {
        throw new Error(
            "confirmMatchValidator requires a getMatchValue function"
        )
    }
    return {
        args,
        key: "confirmMatch",
        badge: `${
            args.label ? sentenceCase(args.label) + "s" : "Values"
        } Match`,
        sticky: false,
        message: `The ${
            args.label ? args.label.lowercase + "s" : "values"
        } entered does not match, please try again`,
        popup: makePopup(),
        test: (value: string) => {
            const matchValue = args.getMatchValue()
            return value ? matchValue && value === matchValue : true
        }
    }
}

export const completeTelephoneValidator = (
    args: {label?: string; getCountryCode: () => string} = {
        getCountryCode: null as () => string
    }
): IFieldValidator => {
    if (!args.getCountryCode) {
        throw new Error(
            "possibleTelephoneValidator requires a getCountryCode function"
        )
    }
    return {
        args,
        key: "completeTelephone",
        badge: "Invalid",
        sticky: false,
        message: "Must be a complete phone number",
        popup: makePopup(),
        test: (value: string) => {
            const numOnly = value.replace(/\D/g, "")
            const countryCode = args.getCountryCode() as CountryCode
            const parsedNumber = parsePhoneNumber(numOnly, countryCode)
            return value && parsedNumber.isPossible()
                ? parsedNumber && parsedNumber.isValid()
                : true
        }
    }
}

export const possibleTelephoneValidator = (args: {
    label?: string
    getCountryCode: () => string
}): IFieldValidator => {
    if (!args.getCountryCode) {
        throw new Error(
            "possibleTelephoneValidator requires a getCountryCode function"
        )
    }
    return {
        args,
        key: "possibleTelephone",
        badge: "Partial",
        sticky: false,
        message: "You must enter a valid phone number",
        popup: makePopup(),
        test: (value: string) => {
            const numOnly = value.replace(/\D/g, "")
            const countryCode = args.getCountryCode() as CountryCode
            const parsedNumber = parsePhoneNumber(numOnly, countryCode)
            console.log(value && parsedNumber && !parsedNumber.isPossible())
            return value ? parsedNumber && parsedNumber.isPossible() : true
        }
    }
}
