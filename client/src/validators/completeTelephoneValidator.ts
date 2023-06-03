import {makePopup} from "."
import parsePhoneNumber, { type CountryCode } from "libphonenumber-js"
import type { IFieldValidator } from "@interfaces"

export default function (
    args: { label?: string; getCountryCode: () => string } = {
        getCountryCode: null as () => string
    }
): IFieldValidator {
    if (!args.getCountryCode) {
        throw new Error(
            "possibleTelephoneValidator requires a getCountryCode function"
        )
    }
    return {
        args,
        badge: "Invalid",
        key: "completeTelephone",
        message: "Must be a complete phone number",
        popup: makePopup(),
        sticky: false,
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
