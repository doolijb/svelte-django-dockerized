import type {IRegionCode, ICountryCode} from "@interfaces"
import {getCountryCode} from "./CountryCodes"

export const USRegionCodes: Map<string, IRegionCode> = new Map<
    string,
    IRegionCode
>([
    [
        "AL",
        {
            name: "Alabama",
            code: "AL",
            keywords: ["al", "alabama"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "AK",
        {
            name: "Alaska",
            code: "AK",
            keywords: ["ak", "alaska"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "AS",
        {
            name: "American Samoa",
            code: "AS",
            keywords: ["as", "american samoa"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "AZ",
        {
            name: "Arizona",
            code: "AZ",
            keywords: ["az", "arizona"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "AR",
        {
            name: "Arkansas",
            code: "AR",
            keywords: ["ar", "arkansas"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "CA",
        {
            name: "California",
            code: "CA",
            keywords: ["ca", "california"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "CO",
        {
            name: "Colorado",
            code: "CO",
            keywords: ["co", "colorado"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "CT",
        {
            name: "Connecticut",
            code: "CT",
            keywords: ["ct", "connecticut"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "DE",
        {
            name: "Delaware",
            code: "DE",
            keywords: ["de", "delaware"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "DC",
        {
            name: "District Of Columbia",
            code: "DC",
            keywords: ["dc", "district of columbia"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "FL",
        {
            name: "Florida",
            code: "FL",
            keywords: ["fl", "florida"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "GA",
        {
            name: "Georgia",
            code: "GA",
            keywords: ["ga", "georgia"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "GU",
        {
            name: "Guam",
            code: "GU",
            keywords: ["gu", "guam"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "HI",
        {
            name: "Hawaii",
            code: "HI",
            keywords: ["hi", "hawaii"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "ID",
        {
            name: "Idaho",
            code: "ID",
            keywords: ["id", "idaho"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "IL",
        {
            name: "Illinois",
            code: "IL",
            keywords: ["il", "illinois"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "IN",
        {
            name: "Indiana",
            code: "IN",
            keywords: ["in", "indiana"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "IA",
        {
            name: "Iowa",
            code: "IA",
            keywords: ["ia", "iowa"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "KS",
        {
            name: "Kansas",
            code: "KS",
            keywords: ["ks", "kansas"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "KY",
        {
            name: "Kentucky",
            code: "KY",
            keywords: ["ky", "kentucky"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "LA",
        {
            name: "Louisiana",
            code: "LA",
            keywords: ["la", "louisiana"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "ME",
        {
            name: "Maine",
            code: "ME",
            keywords: ["me", "maine"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "MD",
        {
            name: "Maryland",
            code: "MD",
            keywords: ["md", "maryland"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "MA",
        {
            name: "Massachusetts",
            code: "MA",
            keywords: ["ma", "massachusetts"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "MI",
        {
            name: "Michigan",
            code: "MI",
            keywords: ["mi", "michigan"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "MN",
        {
            name: "Minnesota",
            code: "MN",
            keywords: ["mn", "minnesota"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "MS",
        {
            name: "Mississippi",
            code: "MS",
            keywords: ["ms", "mississippi"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "MO",
        {
            name: "Missouri",
            code: "MO",
            keywords: ["mo", "missouri"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "MP",
        {
            name: "Northern Mariana Islands",
            code: "MP",
            keywords: ["mp", "northern mariana islands"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "MT",
        {
            name: "Montana",
            code: "MT",
            keywords: ["mt", "montana"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "NE",
        {
            name: "Nebraska",
            code: "NE",
            keywords: ["ne", "nebraska"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "NV",
        {
            name: "Nevada",
            code: "NV",
            keywords: ["nv", "nevada"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "NH",
        {
            name: "New Hampshire",
            code: "NH",
            keywords: ["nh", "new hampshire"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "NJ",
        {
            name: "New Jersey",
            code: "NJ",
            keywords: ["nj", "new jersey"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "NM",
        {
            name: "New Mexico",
            code: "NM",
            keywords: ["nm", "new mexico"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "NY",
        {
            name: "New York",
            code: "NY",
            keywords: ["ny", "new york"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "NC",
        {
            name: "North Carolina",
            code: "NC",
            keywords: ["nc", "north carolina"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "ND",
        {
            name: "North Dakota",
            code: "ND",
            keywords: ["nd", "north dakota"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "OH",
        {
            name: "Ohio",
            code: "OH",
            keywords: ["oh", "ohio"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "OK",
        {
            name: "Oklahoma",
            code: "OK",
            keywords: ["ok", "oklahoma"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "OR",
        {
            name: "Oregon",
            code: "OR",
            keywords: ["or", "oregon"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "PA",
        {
            name: "Pennsylvania",
            code: "PA",
            keywords: ["pa", "pennsylvania"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "PR",
        {
            name: "Puerto Rico",
            code: "PR",
            keywords: ["pr", "puerto rico"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "RI",
        {
            name: "Rhode Island",
            code: "RI",
            keywords: ["ri", "rhode island"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "SC",
        {
            name: "South Carolina",
            code: "SC",
            keywords: ["sc", "south carolina"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "SD",
        {
            name: "South Dakota",
            code: "SD",
            keywords: ["sd", "south dakota"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "TN",
        {
            name: "Tennessee",
            code: "TN",
            keywords: ["tn", "tennessee"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "TX",
        {
            name: "Texas",
            code: "TX",
            keywords: ["tx", "texas"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "UM",
        {
            name: "United States Minor Outlying Islands",
            code: "UM",
            keywords: ["um", "united states minor outlying islands"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "UT",
        {
            name: "Utah",
            code: "UT",
            keywords: ["ut", "utah"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "VT",
        {
            name: "Vermont",
            code: "VT",
            keywords: ["vt", "vermont"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "VI",
        {
            name: "Virgin Islands, U.S.",
            code: "VI",
            keywords: ["vi", "virgin islands, u.s."],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "WA",
        {
            name: "Washington",
            code: "WA",
            keywords: ["wa", "washington"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "VA",
        {
            name: "Virginia",
            code: "VA",
            keywords: ["va", "virginia"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "WV",
        {
            name: "West Virginia",
            code: "WV",
            keywords: ["wv", "west virginia"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "WI",
        {
            name: "Wisconsin",
            code: "WI",
            keywords: ["wi", "wisconsin"],
            getCountryCode: () => getCountryCode("US")
        }
    ],
    [
        "WY",
        {
            name: "Wyoming",
            code: "WY",
            keywords: ["wy", "wyoming"],
            getCountryCode: () => getCountryCode("US")
        }
    ]
])

export const CARegionCodes: Map<string, IRegionCode> = new Map([
    [
        "AB",
        {
            name: "Alberta",
            code: "AB",
            keywords: ["ab", "alberta"],
            getCountryCode: () => getCountryCode("CA")
        }
    ],
    [
        "BC",
        {
            name: "British Columbia",
            code: "BC",
            keywords: ["bc", "british columbia"],
            getCountryCode: () => getCountryCode("CA")
        }
    ],
    [
        "MB",
        {
            name: "Manitoba",
            code: "MB",
            keywords: ["mb", "manitoba"],
            getCountryCode: () => getCountryCode("CA")
        }
    ],
    [
        "NB",
        {
            name: "New Brunswick",
            code: "NB",
            keywords: ["nb", "new brunswick"],
            getCountryCode: () => getCountryCode("CA")
        }
    ],
    [
        "NL",
        {
            name: "Newfoundland and Labrador",
            code: "NL",
            keywords: ["nl", "newfoundland and labrador"],
            getCountryCode: () => getCountryCode("CA")
        }
    ],
    [
        "NS",
        {
            name: "Nova Scotia",
            code: "NS",
            keywords: ["ns", "nova scotia"],
            getCountryCode: () => getCountryCode("CA")
        }
    ],
    [
        "NT",
        {
            name: "Northwest Territories",
            code: "NT",
            keywords: ["nt", "northwest territories"],
            getCountryCode: () => getCountryCode("CA")
        }
    ],
    [
        "NU",
        {
            name: "Nunavut",
            code: "NU",
            keywords: ["nu", "nunavut"],
            getCountryCode: () => getCountryCode("CA")
        }
    ],
    [
        "ON",
        {
            name: "Ontario",
            code: "ON",
            keywords: ["on", "ontario"],
            getCountryCode: () => getCountryCode("CA")
        }
    ],
    [
        "PE",
        {
            name: "Prince Edward Island",
            code: "PE",
            keywords: ["pe", "prince edward island"],
            getCountryCode: () => getCountryCode("CA")
        }
    ],
    [
        "QC",
        {
            name: "Quebec",
            code: "QC",
            keywords: ["qc", "quebec"],
            getCountryCode: () => getCountryCode("CA")
        }
    ],
    [
        "SK",
        {
            name: "Saskatchewan",
            code: "SK",
            keywords: ["sk", "saskatchewan"],
            getCountryCode: () => getCountryCode("CA")
        }
    ],
    [
        "YT",
        {
            name: "Yukon",
            code: "YT",
            keywords: ["yt", "yukon"],
            getCountryCode: () => getCountryCode("CA")
        }
    ]
])
