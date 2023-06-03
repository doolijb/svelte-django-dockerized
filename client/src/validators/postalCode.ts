import { makePopup } from "."
import postalCodes from "postal-codes-js"
import type { IFieldValidator } from "@interfaces"

export default function (args: { getCountryCode: () => string | null }): IFieldValidator {
    return {
        args,
        badge: "Format",
        key: "postalCode",
        message: "Must be a valid postal code",
        popup: makePopup(),
        sticky: false,
        test: (value: string): boolean => {
            const countryCode = args.getCountryCode()
            // We will only test if the country code is valid
            if (!countryCode) {
                return true
            }
            return postalCodes.validate(countryCode, value) === true
        },
    }
}
