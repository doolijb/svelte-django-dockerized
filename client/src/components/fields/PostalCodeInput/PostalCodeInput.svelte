<script lang="ts">
    import {BaseTextInput} from "@components"
    import { countries } from "@data"
    import {
        maxLengthValidator,
        minLengthValidator,
        postalCodeValidator,
        requiredValidator,
    } from "@validators"
    import type {ICountry, IFieldValidator} from "@interfaces"
    import type { CountryCode } from "libphonenumber-js"


    // Component specific
    export let countryCode: CountryCode


    export let disabled = false


    export let errors: IFieldValidator[] = []

    /**
     * Variables
     */
    export let label = "Postal Code"

    export let onBlur: (e: Event) => void | undefined

    export let onFocus: (e: Event) => void | undefined


    // Events
    export let onInput: (e: Event) => void | undefined



    // Refs
    export let ref: HTMLInputElement




    export let type = "text"




    export let validators: IFieldValidator[] = [
        requiredValidator({}),
        minLengthValidator({minLen: 3}),
        maxLengthValidator({maxLen: 10}),
        postalCodeValidator({
            getCountryCode: () => countryCode || null
        })
    ]


    export let value = ""

    /**
     * Component specific
     */
    $: country = countryCode ? countries[countryCode] : null as ICountry

    // Transform value
    $: value = value.toLocaleUpperCase().trim()
</script>

<BaseTextInput
    label={country && country.postalCodeTitle ? country.postalCodeTitle : label}
    bind:type
    bind:validators
    bind:value
    bind:errors
    bind:disabled
    bind:onFocus
    bind:onBlur
    bind:onInput
    bind:ref
/>

<style lang="postcss">
</style>
