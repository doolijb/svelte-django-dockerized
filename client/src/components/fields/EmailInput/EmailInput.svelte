<script lang="ts">
    import {BaseTextInput} from "@components"
    import {
        requiredValidator,
        minLengthValidator,
        maxLengthValidator,
        emailValidator
    } from "@validators"

    export let label: string = "Email Address"
    export let type: string = "email"
    export let validators: FieldValidator[] = [
        requiredValidator(),
        minLengthValidator(5),
        maxLengthValidator(100),
        emailValidator()
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
    {type}
    {label}
    {validators}
    {required}
    {value}
    {errors}
    {onFocus}
    {onBlur}
/>

<style lang="postcss">
</style>
