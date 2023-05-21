<script lang="ts">
    import {BaseTextInput} from "@components"
    import type {IFieldValidator} from "@interfaces"
    import {
        requiredValidator,
        minLengthValidator,
        maxLengthValidator,
        emailValidator
    } from "@validators"

    export let label: string = "Email Address"
    export let type: string = "email"
    export let validators: IFieldValidator[] = [
        requiredValidator({}),
        minLengthValidator({minLen: 5}),
        maxLengthValidator({maxLen: 100}),
        emailValidator({})
    ]
    export let value: string = ""
    export let errors: IFieldValidator[] = []
    export let disabled: boolean = false
    export let onInput: (e: Event) => void = () => {}
    export let onFocus: (e: Event) => void = () => {}
    export let onBlur: (e: Event) => void = () => {}

    // Transform value
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
/>

<style lang="postcss">
</style>
