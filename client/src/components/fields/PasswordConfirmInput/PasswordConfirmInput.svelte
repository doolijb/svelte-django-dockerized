<script lang="ts">
    import {BaseTextInput} from "@components"
    import {
        requiredValidator,
        minLengthValidator,
        maxLengthValidator,
        lowercaseRequiredValidator,
        uppercaseRequiredValidator,
        numberRequiredValidator,
        specialCharRequiredValidator,
        confirmMatchValidator
    } from "@validators"
    import type {IFieldValidator} from "@interfaces"

    export let label: string = "Password"
    export let type: string = "password"
    export let validators: IFieldValidator[] = [
        requiredValidator({}),
        confirmMatchValidator({fieldName: "Password", getMatchValue})
    ]
    export let value: string = ""
    export let errors: IFieldValidator[] = []
    export let disabled: boolean = false
    export let onInput: (e: Event) => void = () => {}
    export let onFocus: (e: Event) => void = () => {}
    export let onBlur: (e: Event) => void = () => {}

    // Component specific
    export let matchValue: string = ""
    function getMatchValue(): string {
        return matchValue
    } // TODO
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
