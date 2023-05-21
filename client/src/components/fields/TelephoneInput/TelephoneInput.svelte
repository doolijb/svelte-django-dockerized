<script lang="ts">
    import {BaseTextInput} from "@components"
    import {
        maxLengthValidator,
        completeTelephoneValidator,
        possibleTelephoneValidator
    } from "@validators"
    import type {IFieldValidator} from "@interfaces"
    import {CountryCodes} from "@constants"
    import {AsYouType} from "libphonenumber-js"

    export let label: string = "Telephone"
    export let type: string = "tel"
    export let value: string = ""
    export let errors: IFieldValidator[] = []
    export let disabled: boolean = false
    export let onInput: (e: Event) => void = formatInput
    export let onFocus: (e: Event) => void = () => {}
    export let onBlur: (e: Event) => void = () => {}

    // Component specific
    let ref: HTMLInputElement
    let selectedCountry = CountryCodes.US.code

    function formatInput(e: InputEvent) {
        // Return if no country is selected or if the input is empty, or if backspace is pressed
        if (
            !selectedCountry ||
            !value ||
            e.inputType === "deleteContentBackward"
        )
            return
        // Format the input
        let draftValue = value
        // Remove all non-numeric characters
        draftValue = draftValue.replace(/\D/g, "")
        // Remove the dial code from the input if it exists
        if (draftValue.startsWith(CountryCodes[selectedCountry].dialCode)) {
            draftValue = draftValue.replace(
                CountryCodes[selectedCountry].dialCode,
                ""
            )
        }
        // Format the input
        const formatter = new AsYouType(selectedCountry as any)
        const formattedInput = formatter.input(draftValue)
        // Set the value of the input to the formatted input
        value = formattedInput
    }

    // Validators (OOP)
    export let validators: IFieldValidator[] = [
        maxLengthValidator({maxLen: 15}),
        completeTelephoneValidator({countryCode: selectedCountry}),
        possibleTelephoneValidator({countryCode: selectedCountry})
    ]
</script>

<BaseTextInput
    bind:label
    bind:type
    bind:validators
    bind:value
    bind:errors
    bind:disabled
    bind:ref
    onFocus={e => {
        onFocus(e)
        ref.select()
    }}
    {onBlur}
    onInput={e => {
        formatInput(e)
        onInput(e)
    }}
>
    <div slot="prefix" class="no-padding">
        <select
            bind:value={selectedCountry}
            class="cursor-pointer"
            on:change={() => ref.focus()}
            title={selectedCountry
                ? CountryCodes[selectedCountry].name
                : "Select a country"}
        >
            {#each Object.values(CountryCodes) as country}
                <option
                    value={country.code}
                    selected={country.code === selectedCountry}
                    title={country.name}>{country.code}</option
                >
            {/each}
        </select>
        <span class="muted select-none">
            {CountryCodes[selectedCountry].dialCode
                ? `+${CountryCodes[selectedCountry].dialCode}`
                : ""}
        </span>
    </div>
</BaseTextInput>

<style lang="postcss">
    .muted {
        opacity: 0.5;
    }
    .no-padding {
        padding: 0 !important;
    }
</style>
