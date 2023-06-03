<script lang="ts">
    import {BaseTextInput} from "@components"
    import {
        maxLengthValidator,
        minLengthValidator,
        requiredValidator,
        specialCharValidator
    } from "@validators"
    import type {IFieldValidator} from "@interfaces"





    /** If the field is disabled */
    export let disabled = false






    /** List of validators with errors */
    export let errors: IFieldValidator[] = []





    /** Name of the field */
    export let label = "Username"







    /** Additional events on:Blur */
    export let onBlur: (e: Event) => void | undefined









    /** Additional events on:Focus */
    export let onFocus: (e: Event) => void | undefined









    /** Additional events on:Input */
    export let onInput: (e: Event) => void | undefined







    /**
     * Exported Props
     */
    /** Ref to the input element */
    export let ref: HTMLInputElement






    /** Type of the input */
    export let type = "text"





    /** List of validators to test the field */
    export let validators: IFieldValidator[] = [
        requiredValidator({}),
        minLengthValidator({minLen: 3}),
        maxLengthValidator({maxLen: 20}),
        specialCharValidator({})
    ]


    /** Value of the field */
    export let value = ""

    /**
     * Reactivity
    */
    $: value = value.toLocaleLowerCase().trim()
</script>

<BaseTextInput
    bind:label
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
