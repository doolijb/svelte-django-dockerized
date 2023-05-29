<script lang="ts">
    import {ValidStates} from "@constants"
    import type {IFieldValidator} from "@interfaces"
    import { onMount } from "svelte"
    import {ValidationBadges} from "@components"

    /**
     * Exported Props
     */
    export let label: string = "Field Label"
    export let placeholder: string = "Select an option"
    export let options: Map<string, any> | any[] = []
    export let value: string = ""
    export let validators: IFieldValidator[] = []
    export let errors: IFieldValidator[] = []
    export let disabled: boolean = false
    // Events
    export let onInput: (e: Event) => void = () => {}
    export let onFocus: (e: Event) => void = () => {}
    export let onBlur: (e: Event) => void = () => {}
    // Refs
    export let ref: HTMLSelectElement

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
    // Convert options to a Map if it is an array
    $: mappedOptions = options instanceof Map
        ? options
        : new Map(options.map(option => [option, option]))

    /**
     * Functions
     */
    function validate() {
        errors = validators.filter(validator => !validator.test(value))
        validState =
            errors.length === 0 ? ValidStates.VALID : ValidStates.INVALID
    }

    /**
     * Constants
    */

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
    <div class="input-group">
        <select
            class="input"
            bind:value
            bind:this={ref}
            {disabled}
            aria-label={label}
            on:input={e => {
                isTouched = true
                validate()
                onInput(e)
            }}
            on:focus={e => {
                isTouched = true
                onFocus(e)
            }}
            on:blur={e => {
                isTouched = true
                validate()
                onBlur(e)
            }}
        >
            <option value="" disabled selected hidden>
                {placeholder}
            </option>
            {#each Object.keys(mappedOptions) as key}
                <option value={options[key]}>
                    {key}
                </option>
            {/each}
    </div>
</label>

<style lang="postcss">
</style>
