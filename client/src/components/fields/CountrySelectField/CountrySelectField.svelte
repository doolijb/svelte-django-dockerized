<script lang="ts">
    import {BaseSearchSelectField} from "@components"
    import {countries} from "@data"
    import {requiredValidator} from "@validators"
    import type {ICountry,IFieldValidator} from "@interfaces"
    import type {AutocompleteOption} from "@skeletonlabs/skeleton"

    export let label = "Country"
    export let placeholder = "Search countries"
    export let value: any = null
    export let validators: IFieldValidator[] = [requiredValidator()]
    export let errors: IFieldValidator[] = []
    export let disabled = false
    // Events
    export let onInput: (e: Event) => void | undefined
    export let onFocus: (e: Event) => void | undefined
    export let onBlur: (e: Event) => void | undefined
    // Refs
    export let ref: HTMLInputElement

    /**
     * Variables
     */

    const options: AutocompleteOption[] = Object.values(countries).map(
        (country: ICountry) => ({
            label: country.name,
            value: country.code,
            keywords: country.keywords
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
