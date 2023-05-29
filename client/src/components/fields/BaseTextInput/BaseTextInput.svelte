<script lang="ts">
    import {onMount} from "svelte"
    import type {PopupSettings} from "@skeletonlabs/skeleton"
    import {ValidStates} from "@constants"
    import type {IFieldValidator} from "@interfaces"
    import {ValidationBadges, ValidationLegend} from "@components"
    import {v4 as uuidv4} from "uuid"

    /**
     * Exported Props
     */
    export let label: string = "Field Label"
    export let type: string = "text"
    export let placeholder: string = ""
    export let validators: IFieldValidator[] = []
    export let errors: IFieldValidator[] = []
    export let value: string = ""
    export let disabled: boolean = false
    // Events
    export let onInput: (e: Event) => void = () => {}
    export let onFocus: (e: Event) => void = () => {}
    export let onBlur: (e: Event) => void = () => {}
    // Refs
    export let ref: HTMLInputElement

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
    const legendPopup: PopupSettings = {
        // Represents the type of event that opens/closed the popup
        event: "click",
        // Matches the data-popup value on your popup element
        target: uuidv4(),
        // Defines which side of your trigger the popup will appear
        placement: "bottom"
    }

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
        <span class="cursor-pointer select-none">
            {label}
        </span>
        <ValidationBadges {validators} {errors} />
    </span>

    <div
        class="input-group"
        class:grid-cols-[auto_1fr_auto]={$$slots.prefix && validators.length}
        class:grid-cols-[1fr_auto]={!$$slots.prefix && validators.length}
        class:grid-cols-[auto_1fr]={$$slots.prefix && !validators.length}
        class:grid-cols-[1fr]={!$$slots.prefix && !validators.length}
    >
        <slot name="prefix" />
        <input
            class="input border-s-0 disabled:cursor-not-allowed"
            use:setType
            bind:value
            bind:this={ref}
            {placeholder}
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
        <div>
            <ValidationLegend.Icon
                {validators}
                {errors}
                {validState}
                {legendPopup}
            />
        </div>
    </div>
    <ValidationLegend.Popup {validators} {errors} {validState} {legendPopup} />
</label>

<style lang="postcss">
</style>
