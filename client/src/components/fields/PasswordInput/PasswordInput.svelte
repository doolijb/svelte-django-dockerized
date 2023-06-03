<script lang="ts">
    import {BaseTextInput} from "@components"
    import {
        lowercaseRequiredValidator,
        maxLengthValidator,
        minLengthValidator,
        numberRequiredValidator,
        requiredValidator,
        specialCharRequiredValidator,
        uppercaseRequiredValidator    } from "@validators"
    import type {IFieldValidator} from "@interfaces"

    export let disabled = false
    export let errors: IFieldValidator[] = []
    export let label = "Password"
    export let onBlur: (e: Event) => void | undefined
    export let onFocus: (e: Event) => void | undefined
    export let onInput: (e: Event) => void | undefined
    export let type = "password"
    export let validators: IFieldValidator[] = [
        requiredValidator({}),
        minLengthValidator({minLen: 10}),
        maxLengthValidator({maxLen: 100}),
        lowercaseRequiredValidator({}),
        uppercaseRequiredValidator({}),
        numberRequiredValidator({}),
        specialCharRequiredValidator({})
    ]
    export let value = ""
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
