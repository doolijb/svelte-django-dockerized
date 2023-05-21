<script lang="ts">
    import {BaseTextInput} from "@components"
    import {
        requiredValidator,
        minLengthValidator,
        maxLengthValidator,
        specialCharValidator
    } from "@validators"
    import type {IFieldValidator} from "@interfaces"

    export let label: string = "Username"
    export let type: string = "text"
    export let validators: IFieldValidator[] = [
        requiredValidator({}),
        minLengthValidator({minLen: 3}),
        maxLengthValidator({maxLen: 20}),
        specialCharValidator({})
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
