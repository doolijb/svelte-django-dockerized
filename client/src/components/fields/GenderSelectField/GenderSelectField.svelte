<script lang="ts">
    import {BaseSearchSelectField} from "@components"
    import { GenderIdentities } from "@constants"
    import {requiredValidator} from "@validators"
    import type {IFieldValidator} from "@interfaces"
    import type {AutocompleteOption} from "@skeletonlabs/skeleton"


    export let disabled = false

    export let errors: IFieldValidator[] = []
    /**
     * Exported Props
     */
    export let label = "Gender"
    export let onBlur: (e: Event) => void | undefined
    export let onFocus: (e: Event) => void | undefined
    // Events
    export let onInput: (e: Event) => void | undefined

    export let placeholder = "Search genders"


    // Refs
    export let ref: HTMLInputElement



    export let searchInput = ""


    export let validators: IFieldValidator[] = [requiredValidator()]

    export let value: any = null

    /**
     * Variables
     */
    const options: AutocompleteOption[] = Object.entries(GenderIdentities).map(([value, label]) => ({
        value,
        label,
    }))
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
    bind:searchInput
    bind:errors
    bind:disabled
    bind:ref
/>

<style lang="postcss">
</style>
