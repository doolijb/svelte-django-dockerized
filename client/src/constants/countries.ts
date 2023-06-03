import { getCountryCallingCode, type CountryCode } from "libphonenumber-js"
import isoCountries from "i18n-iso-countries"
import locale from "i18n-iso-countries/langs/en.json"
import iso3166 from "iso-3166-2"
import type { ICountry, IRegion } from "@interfaces"

isoCountries.registerLocale(locale)

const countries: Map<string, ICountry> = new Map<string, ICountry>()

const countriesData: { [key: string]: Partial<ICountry> } = {
    US: {
        name: "United States",
        dialCode: "1",
        keywords: ["us", "usa", "america", "united states"],
        regionTitle: "State or Territory",
        postalCodeTitle: "ZIP Code",
    },
    CA: {
        regionTitle: "Province or Territory",
        postalCodeTitle: "Postal Code",
    },
    GB: {
        keywords: ["gb", "uk", "united kingdom", "britain", "england", "scotland", "wales", "northern ireland"],
        regionTitle: "County, District or Parish",
        postalCodeTitle: "Postcode",
    },
    AU: {
        keywords: ["au", "aus", "australia", "upside down", "down under", "oz"],
        regionTitle: "State or Territory",
        postalCodeTitle: "Postcode",
    },
    IN: {
        keywords: ["in", "ind", "india"],
        regionTitle: "State or Union Territory",
        postalCodeTitle: "PIN Code",
    },
    PK: {
        keywords: ["pk", "pak", "pakistan"],
        regionTitle: "Province or Territory",
        postalCodeTitle: "Postal Code",
    },
    BD: {
        keywords: ["bd", "bgd", "bangladesh"],
        regionTitle: "Division",
        postalCodeTitle: "Postal Code",
    },
    NG: {
        keywords: ["ng", "nga", "nigeria"],
        regionTitle: "State or Territory",
        postalCodeTitle: "Postal Code",
    },
    PH: {
        keywords: ["ph", "phl", "philippines"],
        regionTitle: "Province or Territory",
        postalCodeTitle: "ZIP Code",
    },
    EG: {
        keywords: ["eg", "egy", "egypt"],
        regionTitle: "Governorate",
        postalCodeTitle: "Postal Code",
    },
    ID: {
        keywords: ["id", "idn", "indonesia"],
        regionTitle: "Province or Territory",
        postalCodeTitle: "Postal Code",
    },
    BR: {
        keywords: ["br", "bra", "brazil"],
        regionTitle: "State",
        postalCodeTitle: "CEP",
    },
    CN: {
        keywords: ["cn", "chn", "china"],
        regionTitle: "Province or Territory",
        postalCodeTitle: "Postal Code",
    },
    JP: {
        keywords: ["jp", "jpn", "japan"],
        regionTitle: "Prefecture",
        postalCodeTitle: "Postal Code",
    },
    DE: {
        keywords: ["de", "deu", "germany"],
        regionTitle: "State",
        postalCodeTitle: "Postal Code",
    },
    FR: {
        keywords: ["fr", "fra", "france"],
        regionTitle: "Region",
        postalCodeTitle: "Postal Code",
    },
    IT: {
        keywords: ["it", "ita", "italy"],
        regionTitle: "Region",
        postalCodeTitle: "CAP",
    },
    MX: {
        keywords: ["mx", "mex", "mexico"],
        regionTitle: "State",
        postalCodeTitle: "Postal Code",
    },
    KR: {
        keywords: ["kr", "kor", "south korea"],
        regionTitle: "Province or Metropolitan City",
        postalCodeTitle: "Postal Code",
    },
    ES: {
        keywords: ["es", "esp", "spain"],
        regionTitle: "Autonomous Community",
        postalCodeTitle: "Postal Code",
    },
    RU: {
        keywords: ["ru", "rus", "russia"],
        regionTitle: "Federal Subject",
        postalCodeTitle: "Postal Code",
    },
    // Missing from libphonenumber-js
    AQ: {
        keywords: ["aq", "ata", "antarctica"],
        dialCode: "672",
        postalCodeTitle: "Postal Code",
    },
    BV: {
        keywords: ["bv", "bvt", "bouvet island"],
        dialCode: "47",
        postalCodeTitle: "Postal Code",
    },
    TF: {
        keywords: ["tf", "atf", "french southern territories"],
        dialCode: "262",
        postalCodeTitle: "Postal Code",
    },
    HM: {
        keywords: ["hm", "hmd", "heard island and mcdonald islands"],
        dialCode: "672",
        postalCodeTitle: "Postal Code",
    },
    PN: {
        keywords: ["pn", "pcn", "pitcairn"],
        dialCode: "64",
        postalCodeTitle: "Postal Code",
    },
    GS: {
        keywords: ["gs", "sgs", "south georgia and the south sandwich islands"],
        dialCode: "500",
        postalCodeTitle: "Postal Code",
    },
    UM: {
        keywords: ["um", "umi", "united states minor outlying islands"],
        dialCode: "1",
        postalCodeTitle: "ZIP Code",
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
            name,
            code,
            dialCode,
            keywords,
            regionTitle,
            postalCodeTitle,
            getRegions: () => getRegions(code),
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
            name: subdivisionName,
            code: subdivisionCode,
            keywords: keywords,
            getCountry: () => countries.get(country),
        })
    }

    return regions
}

// Generate the Countries structure
generateCountries()

export default countries
