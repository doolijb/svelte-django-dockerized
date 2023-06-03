<!--
    Some documentation on how to use this component
 -->
<script lang="ts">
    /**
     * Some documentation on how to use this component
     */
    import {onMount} from "svelte"
    import {popup, type PopupSettings} from "@skeletonlabs/skeleton"
    import {ValidStates} from "@constants"
    import type {IFieldValidator} from "@interfaces"
    import {ValidationBadges, ValidationLegend} from "@components"
    import {Autocomplete} from "@skeletonlabs/skeleton"
    import type {AutocompleteOption} from "@skeletonlabs/skeleton"
    import {v4 as uuidv4} from "uuid"

    /**
     * Exported Props
     */
    export let label: string = "Field Label"
    export let placeholder: string = "Search options"
    export let options: AutocompleteOption[] = []
    export let value: any = null
    export let validators: IFieldValidator[] = []
    export let errors: IFieldValidator[] = []
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
    // On search input, we need to update the selected option
    $: searchInput = ""
    $: selectedOption = getOptionByLabel(searchInput) || null
    $: required = false
    $: isTouched = false
    $: validState = isTouched
        ? errors.length === 0
            ? ValidStates.VALID
            : ValidStates.INVALID
        : ValidStates.NONE

    /**
     * Functions
     */

    function validate() {
        errors = validators.filter(validator => !validator.test(value))
        validState =
            errors.length === 0 ? ValidStates.VALID : ValidStates.INVALID
    }

    function updateField() {
        // Update the value
        isTouched = true
        if (selectedOption) {
            value = selectedOption.value
            searchInput = selectedOption.label
        } else {
            value = null
        }
        isTouched = true
        validate()
    }

    function getOptionByLabel(label: string): AutocompleteOption {
        // Find the option by label so we can track state during input or selection
        const option = options.find(
            option =>
                option.label.toLocaleLowerCase() === label.toLocaleLowerCase()
        )
        return option
    }

    function getOptionByValue(value: any): AutocompleteOption {
        // Find the option by value so we can track state during input or selection
        const option = options.find(option => option.value === value)
        return option
    }

    function handleBlur(e: Event) {
        // If the user has not selected a valid option, clear the input
        updateField()
    }

    function handleSelection(e: CustomEvent) {
        // When an option is selected, update the search input,
        // the value will be updated automatically by the reactive variables
        if (!e.detail) {
            searchInput = ""
        } else {
            searchInput = e.detail.label
        }
        updateField()
    }

    /**
     * Constants
     */
    const legendPopup: PopupSettings = ValidationLegend.makePopupSettings()

    /**
     * Lifecycle
     */
    onMount(() => {
        if (value) {
            isTouched = true
            searchInput = getOptionByValue(value)?.label || ""
            validate()
        }
        validators.forEach(validator => {
            switch (validator.key) {
                case "required":
                    required = true
                    break
            }
        })
    })

    let popupSettings: PopupSettings = {
        event: "focus-click",
        target: uuidv4(),
        placement: "bottom"
    }
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
        class:grid-cols-[auto_1fr]={$$slots.prefix && !validators.length}
        class:grid-cols-[1fr]={!$$slots.prefix && !validators.length && !disabled}
    >
        <slot name="prefix" />
        <input
            bind:this={ref}
            class="autocomplete input"
            type="search"
            name="autocomplete-search"
            bind:value={searchInput}
            {placeholder}
            use:popup={popupSettings}
            on:input={onInput}
            on:blur={e => {
                // Perform the local blur event first
                handleBlur(e)
                onBlur(e)
            }}
            on:focus={onFocus}
            {disabled}
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
    <div data-popup={popupSettings.target} class="card z-10 p-3 shadow-xl max-h-[75vh] overflow-y-scroll">
        <span class="h3 mb-3 select-none"> Choose an option </span>
        <Autocomplete
            bind:input={searchInput}
            {options}
            on:selection={handleSelection}
        />
        <!-- Show a button to clear the value -->
        {#if searchInput}
            <div class="text-center">
                <button
                    class="btn-link btn variant-filled-secondary mt-3 select-none"
                    on:click={e => {
                        value = ""
                        searchInput = ""
                        validate()
                        e.preventDefault()
                    }}
                >
                    Reset
                </button>
            </div>
        {/if}
    </div>
    {#if !disabled}
        <ValidationLegend.Popup {validators} {errors} {validState} {legendPopup} />
    {/if}
</label>

<style lang="postcss">
</style>
