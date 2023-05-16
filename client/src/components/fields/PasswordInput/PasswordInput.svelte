<script lang="ts">
    import {BaseTextInput} from "@components"
    import {
        requiredValidator,
        minLengthValidator,
        maxLengthValidator,
        lowercaseRequiredValidator,
        uppercaseRequiredValidator,
        numberRequiredValidator,
        specialCharRequiredValidator
    } from "@validators"

    export let label: string = "Password"
    export let type: string = "password"
    export let validators: FieldValidator[] = [
        requiredValidator(),
        minLengthValidator(10),
        maxLengthValidator(100),
        lowercaseRequiredValidator(),
        uppercaseRequiredValidator(),
        numberRequiredValidator(),
        specialCharRequiredValidator()
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
