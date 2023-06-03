<script lang="ts">
    import {onMount} from "svelte"
    import {BaseTextInput} from "@components"
    import {
        maxLengthValidator,
        completeTelephoneValidator,
        possibleTelephoneValidator
    } from "@validators"
    import type {IFieldValidator} from "@interfaces"
    import {countries} from "@constants"
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
    export let readonlyCountry: boolean = false
    export let country = countries['US'].code

    function formatInput(e?: InputEvent | FocusEvent) {
        // Return if no country is selected or if the input is empty, or if backspace is pressed
        if (
            !country ||
            !value ||
            e === undefined ||
            e.type === "focus" ||
            (e.type === "input" &&
                (e as InputEvent).inputType === "deleteContentBackward")
        )
            return
        // Format the input
        let draftValue = value
        // Remove all non-numeric characters
        draftValue = draftValue.replace(/\D/g, "")
        // Remove the dial code from the input if it exists
        if (draftValue.startsWith(countries[country].dialCode)) {
            draftValue = draftValue.replace(countries[country].dialCode, "")
        }
        // Format the input
        const formatter = new AsYouType(country as any)
        const formattedInput = formatter.input(draftValue)
        // Set the value of the input to the formatted input
        value = formattedInput
    }

    $: value ? formatInput() : null

    // Validators (OOP)
    export let validators: IFieldValidator[] = [
        maxLengthValidator({maxLen: 15}),
        completeTelephoneValidator({getCountryCode: () => country}),
        possibleTelephoneValidator({getCountryCode: () => country})
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
    onBlur={e => {
        formatInput(e)
        onBlur(e)
    }}
    onInput={e => {
        formatInput(e)
        onInput(e)
    }}
>
    <div slot="prefix" class="no-padding">
        {#if readonlyCountry || disabled}
        <span class="cursor-pointer px-3 muted" title={countries[country].name}>
            {country}
        </span>
        {:else}
        <select
            bind:value={country}
            class="cursor-pointer"
            on:change={() => ref.focus()}
            title={country ? countries[country].name : "Select a country"}
        >
            {#each Object.values(countries) as country}
                <option
                    value={country.code}
                    selected={country.code === country}
                    title={country.name}>{country.code}</option
                >
            {/each}
        </select>
        {/if}
        <span class="muted cursor-pointer">
            {countries[country].dialCode
                ? `+${countries[country].dialCode}`
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
