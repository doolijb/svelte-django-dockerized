import isoCountries from "i18n-iso-countries"
import locale from "i18n-iso-countries/langs/en.json"
import iso3166 from "iso-3166-2"
import { type CountryCode, getCountryCallingCode } from "libphonenumber-js"
import type { ICountry, IRegion } from "@interfaces"

isoCountries.registerLocale(locale)

const countries: Map<string, ICountry> = new Map<string, ICountry>()

const countriesData: { [key: string]: Partial<ICountry> } = {
    // Missing from libphonenumber-js
    AQ: {
        dialCode: "672",
        keywords: ["aq", "ata", "antarctica"],
        postalCodeTitle: "Postal Code",
    },

    AU: {
        keywords: ["au", "aus", "australia", "upside down", "down under", "oz"],
        postalCodeTitle: "Postcode",
        regionTitle: "State or Territory",
    },

    BD: {
        keywords: ["bd", "bgd", "bangladesh"],
        postalCodeTitle: "Postal Code",
        regionTitle: "Division",
    },

    BR: {
        keywords: ["br", "bra", "brazil"],
        postalCodeTitle: "CEP",
        regionTitle: "State",
    },

    BV: {
        dialCode: "47",
        keywords: ["bv", "bvt", "bouvet island"],
        postalCodeTitle: "Postal Code",
    },

    CA: {
        postalCodeTitle: "Postal Code",
        regionTitle: "Province or Territory",
    },

    CN: {
        keywords: ["cn", "chn", "china"],
        postalCodeTitle: "Postal Code",
        regionTitle: "Province or Territory",
    },

    DE: {
        keywords: ["de", "deu", "germany"],
        postalCodeTitle: "Postal Code",
        regionTitle: "State",
    },

    EG: {
        keywords: ["eg", "egy", "egypt"],
        postalCodeTitle: "Postal Code",
        regionTitle: "Governorate",
    },

    ES: {
        keywords: ["es", "esp", "spain"],
        postalCodeTitle: "Postal Code",
        regionTitle: "Autonomous Community",
    },

    FR: {
        keywords: ["fr", "fra", "france"],
        postalCodeTitle: "Postal Code",
        regionTitle: "Region",
    },

    GB: {
        keywords: ["gb", "uk", "united kingdom", "britain", "england", "scotland", "wales", "northern ireland"],
        postalCodeTitle: "Postcode",
        regionTitle: "County, District or Parish",
    },

    GS: {
        dialCode: "500",
        keywords: ["gs", "sgs", "south georgia and the south sandwich islands"],
        postalCodeTitle: "Postal Code",
    },

    HM: {
        dialCode: "672",
        keywords: ["hm", "hmd", "heard island and mcdonald islands"],
        postalCodeTitle: "Postal Code",
    },

    ID: {
        keywords: ["id", "idn", "indonesia"],
        postalCodeTitle: "Postal Code",
        regionTitle: "Province or Territory",
    },

    IN: {
        keywords: ["in", "ind", "india"],
        postalCodeTitle: "PIN Code",
        regionTitle: "State or Union Territory",
    },

    IT: {
        keywords: ["it", "ita", "italy"],
        postalCodeTitle: "CAP",
        regionTitle: "Region",
    },

    JP: {
        keywords: ["jp", "jpn", "japan"],
        postalCodeTitle: "Postal Code",
        regionTitle: "Prefecture",
    },

    KR: {
        keywords: ["kr", "kor", "south korea"],
        postalCodeTitle: "Postal Code",
        regionTitle: "Province or Metropolitan City",
    },

    MX: {
        keywords: ["mx", "mex", "mexico"],
        postalCodeTitle: "Postal Code",
        regionTitle: "State",
    },

    NG: {
        keywords: ["ng", "nga", "nigeria"],
        postalCodeTitle: "Postal Code",
        regionTitle: "State or Territory",
    },

    PH: {
        keywords: ["ph", "phl", "philippines"],
        postalCodeTitle: "ZIP Code",
        regionTitle: "Province or Territory",
    },
    PK: {
        keywords: ["pk", "pak", "pakistan"],
        postalCodeTitle: "Postal Code",
        regionTitle: "Province or Territory",
    },
    PN: {
        dialCode: "64",
        keywords: ["pn", "pcn", "pitcairn"],
        postalCodeTitle: "Postal Code",
    },
    RU: {
        keywords: ["ru", "rus", "russia"],
        postalCodeTitle: "Postal Code",
        regionTitle: "Federal Subject",
    },
    TF: {
        dialCode: "262",
        keywords: ["tf", "atf", "french southern territories"],
        postalCodeTitle: "Postal Code",
    },
    UM: {
        dialCode: "1",
        keywords: ["um", "umi", "united states minor outlying islands"],
        postalCodeTitle: "ZIP Code",
    },
    US: {
        dialCode: "1",
        keywords: ["us", "usa", "america", "united states"],
        name: "United States",
        postalCodeTitle: "ZIP Code",
        regionTitle: "State or Territory",
    },
}

// Generate the Countries structure
function generateCountries(): void {
    const countryNames = isoCountries.getNames("en") // Get an object of country codes and names
    Object.keys(countryNames).forEach((code) => {
        const countryData = countriesData[code] || {}

        const name = countryData.name || countryNames[code]
        const regionTitle = countryData.regionTitle || ""
        let dialCode = countryData.dialCode || ""
        const keywords = [code.toLowerCase(), name.toLowerCase(), ...(countryData.keywords || [])]
        const postalCodeTitle = countryData.postalCodeTitle || null

        try {
            // Attempt to get the dial code from libphonenumber-js
            !dialCode ? dialCode = getCountryCallingCode(code as CountryCode) : null
        } catch (e) {
            console.log(e)
        }

        countries[code] = {
            code,
            dialCode,
            getRegions: () => getRegions(code),
            keywords,
            name,
            postalCodeTitle,
            regionTitle,
        }
    })
}

// Generate the Regions for a specific country
function getRegions(country: string): Map<string, IRegion> {
    const regions: Map<string, IRegion> = new Map<string, IRegion>()

    const subdivisions = iso3166.country(country).sub
    for (const subdivisionCode in subdivisions) {
        const subdivisionName = subdivisions[subdivisionCode].name
        const keywords = [subdivisionCode.toLowerCase(), subdivisionName.toLowerCase()]

        regions.set(subdivisionCode, {
            code: subdivisionCode,
            getCountry: () => countries.get(country),
            keywords: keywords,
            name: subdivisionName,
        })
    }

    return regions
}

// Generate the Countries structure
generateCountries()

export default countries
