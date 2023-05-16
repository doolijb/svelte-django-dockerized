<script lang="ts">
    import {onMount} from "svelte"
    import Icon from "@iconify/svelte"
    import type {PopupSettings} from "@skeletonlabs/skeleton"
    import {popup} from "@skeletonlabs/skeleton"
    import {sentenceCase} from "change-case"
    import {ValidStates} from "@constants"
    import {v4 as uuidv4} from "uuid"

    export let label: string = "Field Label"
    export let type: string = "text"
    export let validators: FieldValidator[] = []
    export let required: boolean = false
    export let value: string = ""
    export let placeholder: string = ""
    export let errors: FieldValidator[] = []
    export let disabled: boolean = false
    export let onInput: (e: event) => void = () => {}
    export let onFocus: (e: event) => void = () => {}
    export let onBlur: (e: event) => void = () => {}

    let legendIcon = null
    $: isTouched = false
    $: validState = isTouched
        ? errors.length === 0
            ? ValidStates.VALID
            : ValidStates.INVALID
        : ValidStates.NONE

    function validate() {
        errors = validators.filter(validator => validator.test(value))
        validState =
            errors.length === 0 ? ValidStates.VALID : ValidStates.INVALID
    }

    function setType(node: HTMLInputElement) {
        // Can not set dynamic type directly in the input element
        node.type = type
    }

    const legendPopup: PopupSettings = {
        // Represents the type of event that opens/closed the popup
        event: "hover",
        // Matches the data-popup value on your popup element
        target: "legendPopup",
        // Defines which side of your trigger the popup will appear
        placement: "bottom"
    }

    onMount(() => {
        if (value) {
            isTouched = true
            validate()
        }
        // use directive won't propagate on this element
        if (validators.length) {
            popup(legendIcon, legendPopup)
        }
    })
</script>

<label class="label">
    <span>
        {label}
        {#each validators as validator}
            {#if validator.sticky || errors.includes(validator)}
                <span
                    class="badge ms-1"
                    class:variant-soft-primary={!errors.includes(validator)}
                    class:variant-soft-error={errors.includes(validator)}
                    on:click={e => e.preventDefault()}
                    use:popup={validator.popup}
                >
                    {validator.badge}
                </span>
                {#if validator.popup}
                    <div
                        class="card block z-10 p-4"
                        class:variant-filled-primary={!errors.includes(
                            validator
                        )}
                        class:variant-filled-error={errors.includes(validator)}
                        data-popup={validator.popup.target}
                    >
                        <p>{validator.message}</p>
                        <div
                            class="arrow"
                            class:variant-filled-primary={!errors.includes(
                                validator
                            )}
                            class:variant-filled-error={errors.includes(
                                validator
                            )}
                        />
                    </div>
                {/if}
            {/if}
        {/each}
    </span>
    <div class="input-group input-group-divider grid-cols-[1fr_auto]">
        <input
            class="input disabled:cursor-not-allowed"
            use:setType
            bind:value
            {placeholder}
            {disabled}
            on:input={e => {
                isTouched = true
                validate()
                onInput(e)
            }}
            on:focus(onFocus)
            on:blur={e => {
                validate()
                onBlur(e)
            }}

        />
        {#if validators.length}
            <div
                class="input-group-icon"
                class:variant-glass-muted={validState === ValidStates.NONE}
                class:variant-glass-error={validState === ValidStates.INVALID}
                class:variant-glass-success={validState === ValidStates.VALID}
                on:click={e => e.preventDefault()}
                bind:this={legendIcon}
            >
                {#if validState === ValidStates.INVALID}
                    <Icon
                        icon="material-symbols:warning"
                        class="text-error-500 pointer-events-none"
                        width="2em"
                    />
                {:else if validState === ValidStates.VALID}
                    <Icon
                        icon="material-symbols:check-small"
                        class="text-success-700 pointer-events-none"
                        width="2em"
                    />
                {:else}
                    <Icon icon="ic:sharp-minus" class="pointer-events-none" width="2em" />
                {/if}
            </div>
        {/if}
    </div>
    {#if validators.length}
        <div class="card z-10 p-4 shadow-xl w-96" data-popup={legendPopup.target}>
            <h4 class="h4 mb-2">Requirements</h4>
            <!-- Present the validators with name and description in a pretty layout -->
            {#each validators as validator}
            <div>
                <span class="badge variant-filled">
                    {validator.badge}
                </span>
            </div>
            <div class="ps-2 mb-1">
                <span class="prose-sm">{validator.message}</span>
            </div>
            {/each}
            <div class="arrow bg-surface-100-800-token" />
        </div>
    {/if}
</label>

<style lang="postcss">
</style>
