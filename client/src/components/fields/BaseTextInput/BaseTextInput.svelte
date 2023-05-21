<script lang="ts">
    import {onMount} from "svelte"
    import Icon from "@iconify/svelte"
    import type {PopupSettings} from "@skeletonlabs/skeleton"
    import {popup} from "@skeletonlabs/skeleton"
    import {ValidStates} from "@constants"
    import type {IFieldValidator} from "@interfaces"

    export let label: string = "Field Label"
    export let type: string = "text"
    export let validators: IFieldValidator[] = []
    export let value: string = ""
    export let placeholder: string = ""
    export let errors: IFieldValidator[] = []
    export let disabled: boolean = false
    export let onInput: (e: Event) => void = () => {}
    export let onFocus: (e: Event) => void = () => {}
    export let onBlur: (e: Event) => void = () => {}
    export let ref = null

    let required = false
    let legendIcon = null
    $: isTouched = false
    $: validState = isTouched
        ? errors.length === 0
            ? ValidStates.VALID
            : ValidStates.INVALID
        : ValidStates.NONE

    function validate() {
        errors = validators.filter(validator => !validator.test(value))
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
        validators.forEach(validator => {
            if (validator.key === "requiredValidator") {
                required = true
            }
        })
    })
</script>

<label class="label">
    <span>
        {label}
        {#each validators as validator}
            {#if validator.sticky || errors.includes(validator)}
                <!-- svelte-ignore a11y-click-events-have-key-events -->
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
                        class="card z-10 block p-4"
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
            {required}
        />
        {#if validators.length}
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <div
                class="input-group-icon"
                on:click={e => e.preventDefault()}
                bind:this={legendIcon}
            >
                {#if validState === ValidStates.INVALID}
                    <Icon
                        icon="material-symbols:warning"
                        class="pointer-events-none text-error-500"
                        width="2em"
                    />
                {:else if validState === ValidStates.VALID}
                    <Icon
                        icon="material-symbols:check-small"
                        class="pointer-events-none text-success-700"
                        width="2em"
                    />
                {:else}
                    <Icon
                        icon="ic:sharp-minus"
                        class="pointer-events-none"
                        width="2em"
                    />
                {/if}
            </div>
        {/if}
    </div>
    {#if validators.length}
        <div
            class="card z-10 w-96 p-4 shadow-xl"
            data-popup={legendPopup.target}
        >
            <h4 class="h4 mb-2">Requirements</h4>
            <!-- Present the validators with name and description in a pretty layout -->
            {#each validators as validator}
                <div>
                    <span class="badge variant-filled">
                        {validator.badge}
                    </span>
                </div>
                <div class="mb-1 ps-2">
                    <span class="prose-sm">{validator.message}</span>
                </div>
            {/each}
            <div class="arrow bg-surface-100-800-token" />
        </div>
    {/if}
</label>

<style lang="postcss">
</style>
