<script lang="ts">
    import {ValidationBadges, ValidationLegend} from "@components"
    import {ValidStates} from "@constants"
    import {onMount} from "svelte"
    import type {IFieldValidator} from "@interfaces"
    import type {PopupSettings} from "@skeletonlabs/skeleton"


    export let disabled = false
    export let errors: IFieldValidator[] = []
    export let label = "Field Label"
    export let onBlur: (e: Event) => void | undefined
    export let onFocus: (e: Event) => void | undefined
    // Events
    export let onInput: (e: Event) => void | undefined

    export let placeholder = ""


    // Refs
    export let ref: HTMLInputElement



    export let type = "text"


    export let validators: IFieldValidator[] = []

    export let value = ""

    /**
     * Variables
     */
    $: required = false
    $: isTouched = false
    $: validState = isTouched
        ? errors.length === 0
            ? ValidStates.VALID
            : ValidStates.INVALID
        : ValidStates.NONE

    /**
     * Constants
     */
    const legendPopup: PopupSettings = ValidationLegend.makePopupSettings()

    /**
     * Functions
     */
    function validate() {
        errors = validators.filter(validator => !validator.test(value))
        validState =
            errors.length === 0 ? ValidStates.VALID : ValidStates.INVALID
    }

    function setType(node: HTMLInputElement) {
        // Can not set dynamic type directly in the input element
        node.type = type
    }

    /**
     * Lifecycle
     */
    onMount(() => {
        if (value) {
            isTouched = true
            validate()
        }
        validators.forEach(validator => {
            switch (validator.key) {
            case "required":
                required = true
                break
            case "maxLength":
                ref.maxLength = validator.args["maxLen"]
                break
            case "minLength":
                ref.minLength = validator.args["minLen"]
                break
            }
        })
    })
</script>

<label class="label">
    <span>
        <span class="cursor-pointer select-none" class:text-gray-500={disabled}>
            {label}
        </span>
        {#if !disabled}
            <ValidationBadges {validators} {errors} />
        {/if}
    </span>

    <div
        class="input-group"
        class:grid-cols-[auto_1fr_auto]={$$slots.prefix && validators.length}
        class:grid-cols-[1fr_auto]={!$$slots.prefix && validators.length}
        class:grid-cols-[auto_1fr]={$$slots.prefix && !validators.length && !disabled}
        class:grid-cols-[1fr]={!$$slots.prefix && !validators.length && !disabled}
    >
        <slot name="prefix" />
        <input
            class="input border-s-0 disabled:cursor-not-allowed"
            use:setType
            bind:value
            bind:this={ref}
            placeholder={!disabled ? placeholder : ""}
            {disabled}
            on:input={e => {
                isTouched = true
                validate()
                onInput(e)
            }}
            on:focus={onFocus}
            on:blur={e => {
                validate()
                onBlur(e)
            }}
            aria-label={label}
            {required}
        />
        {#if !disabled}
            <ValidationLegend.Icon
                {validators}
                {errors}
                {validState}
                {legendPopup}
            />
        {/if}
    </div>
    {#if !disabled}
        <ValidationLegend.Popup {validators} {errors} {validState} {legendPopup} />
    {/if}
</label>

<style lang="postcss">
</style>
