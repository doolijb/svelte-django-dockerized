<script lang="ts">
    import {BaseSearchSelectField} from "@components"
    import type {AutocompleteOption} from "@skeletonlabs/skeleton"
    import type {IFieldValidator, ICountry, IRegion} from "@interfaces"
    import {countries} from "@constants"
    import {requiredValidator} from "@validators"
    import type { CountryCode } from "libphonenumber-js"

    export let label: string = "Region"
    export let placeholder: string = "Search regions"
    export let value: any = null
    export let validators: IFieldValidator[] = [requiredValidator()]
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
     * Variables
     */
    $: country = countryCode ? countries[countryCode] : null as ICountry
    $: options = country ? getOptions() : [] as AutocompleteOption[]

    /**
     * Functions
     */
    function getOptions(): AutocompleteOption[] {
        let regions = null
        // Get regions
        try {
            regions = country.getRegions()
        } catch (e) {
            console.log(e)
            return []
        }
        // Return options
        return [...regions.values()].map((region: IRegion) => ({
            label: region.name,
            value: region.code,
            keywords: region.keywords
        })).sort((a: AutocompleteOption, b: AutocompleteOption) => a.label.localeCompare(b.label))
    }

</script>
{#if countryCode && options.length > 0}
    <BaseSearchSelectField
        label={country && country.regionTitle ? country.regionTitle : label}
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
{/if}

<style lang="postcss">
</style>
