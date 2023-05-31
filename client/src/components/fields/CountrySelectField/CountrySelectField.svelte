<script lang="ts">
    import {BaseSearchSelectField} from "@components"
    import type {AutocompleteOption} from "@skeletonlabs/skeleton"
    import type {IFieldValidator, ICountryCode} from "@interfaces"
    import {CountryCodes} from "@constants"
    import {onMount} from "svelte"
    import {requiredValidator} from "@validators"

    export let label: string = "Country"
    export let placeholder: string = "Search countries"
    export let value: any = null
    export let validators: IFieldValidator[] = [requiredValidator()]
    export let errors: IFieldValidator[] = []
    export let disabled: boolean = false
    // Events
    export let onInput: (e: Event) => void = () => {}
    export let onFocus: (e: Event) => void = () => {}
    export let onBlur: (e: Event) => void = () => {}
    // Refs
    export let ref: HTMLSelectElement

    /**
     * Variables
     */

    const options: AutocompleteOption[] = Array.from(CountryCodes.values()).map(
        (countryCode: ICountryCode) => ({
            label: countryCode.name,
            value: countryCode.code,
            keywords: countryCode.keywords
        })
    )

    /**
     * Lifecycle
     */
</script>

<BaseSearchSelectField
    {label}
    {placeholder}
    {options}
    {validators}
    {onInput}
    {onFocus}
    {onBlur}
    bind:value
    bind:errors
    bind:disabled
    bind:ref
/>

<style lang="postcss">
</style>
