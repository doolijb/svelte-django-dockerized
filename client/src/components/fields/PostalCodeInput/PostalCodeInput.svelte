<script lang="ts">
    import {BaseTextInput} from "@components"
    import { countries } from "@constants"
    import type {ICountry, IFieldValidator} from "@interfaces"
    import {
        requiredValidator,
        minLengthValidator,
        maxLengthValidator,
        postalCodeValidator,
    } from "@validators"
    import type { CountryCode } from "libphonenumber-js"

    /**
     * Variables
     */
    export let label: string = "Postal Code"
    export let type: string = "text"
    export let validators: IFieldValidator[] = [
        requiredValidator({}),
        minLengthValidator({minLen: 3}),
        maxLengthValidator({maxLen: 10}),
        postalCodeValidator({
            getCountryCode: () => countryCode || null
        })
    ]
    export let value: string = ""
    export let errors: IFieldValidator[] = []
    export let disabled: boolean = false
    // Events
    export let onInput: (e: Event) => void = () => {}
    export let onFocus: (e: Event) => void = () => {}
    export let onBlur: (e: Event) => void = () => {}
    // Refs
    export let ref: HTMLInputElement
    // Component specific
    export let countryCode: CountryCode

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
