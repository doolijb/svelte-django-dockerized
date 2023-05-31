import type {ICountryCode} from "@interfaces"
import {getRegionCodes} from "./RegionCodes"

export function getCountryCode(countryCode: string): ICountryCode {
    return CountryCodes.get(countryCode)
}

export const CountryCodes = new Map<string, ICountryCode>([
    [
        "US",
        {
            name: "United States",
            code: "US",
            dialCode: "1",
            keywords: ["us", "usa", "america", "united states"],
            getRegionCodes: () => getRegionCodes("US")
        }
    ],
    [
        "CA",
        {
            name: "Canada",
            code: "CA",
            dialCode: "1",
            keywords: ["ca", "canada"],
            getRegionCodes: () => getRegionCodes("CA")
        }
    ],
    [
        "CN",
        {
            name: "China",
            code: "CN",
            dialCode: "86",
            keywords: ["cn", "china"],
            getRegionCodes: () => getRegionCodes("CN")
        }
    ],
    [
        "UR",
        {
            name: "Ukraine",
            code: "UR",
            dialCode: "380",
            keywords: ["ur", "ukraine"],
            getRegionCodes: () => getRegionCodes("UR")
        }
    ],
    [
        "RU",
        {
            name: "Russia",
            code: "RU",
            dialCode: "7",
            keywords: ["ru", "russia"],
            getRegionCodes: () => getRegionCodes("RU")
        }
    ]
])
