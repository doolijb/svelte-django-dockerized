<script lang="ts">
    import {BaseTextInput} from "@components"
    import {
        requiredValidator,
        minLengthValidator,
        maxLengthValidator,
        specialCharValidator
    } from "@validators"

    export let label: string = "Username"
    export let type: string = "text"
    export let validators: FieldValidator[] = [
        requiredValidator(),
        minLengthValidator(3),
        maxLengthValidator(20),
        specialCharValidator()
    ]
    export let required: boolean = false
    export let value: string = ""
    export let errors: FieldValidator[] = []
    export let disabled: boolean = false
    export let onInput: (e: event) => void = () => {}
    export let onFocus: (e: event) => void = () => {}
    export let onBlur: (e: event) => void = () => {}
</script>

<BaseTextInput
    {label}
    {type}
    {validators}
    {required}
    {value}
    {errors}
    {onFocus}
    {onBlur}
/>

<style lang="postcss">
</style>
