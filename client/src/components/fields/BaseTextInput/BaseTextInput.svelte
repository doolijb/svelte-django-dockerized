<script lang="ts">
    import {onMount} from "svelte"
    import Icon from "@iconify/svelte"
    import type {PopupSettings} from "@skeletonlabs/skeleton"
    import {popup} from "@skeletonlabs/skeleton"
    import {sentenceCase} from "change-case"
    import {ValidStates} from "@constants"

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

    onMount( () => {
        if (value) {
            isTouched = true
            validate()
        }
    })

</script>

<label class="label">
    <span>
        {label}
        {#each validators as validator}
            {#if validator.sticky || errors.includes(validator)}
                <span
                    class="badge ms-2"
                    class:variant-soft-primary={!errors.includes(validator)}
                    class:variant-soft-error={errors.includes(validator)}
                    use:popup={validator.popup}
                >
                    {validator.badge}
                </span>
                {#if validator.popup}
                    <div
                        class="card p-4"
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
            on:focus={onFocus}
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
                title={sentenceCase(validState)}
            >
                {#if validState === ValidStates.INVALID}
                    <Icon
                        icon="material-symbols:warning"
                        class="text-error-500"
                        width="2em"
                    />
                {:else if validState === ValidStates.VALID}
                    <Icon
                        icon="material-symbols:check-small"
                        class="text-success-700"
                        width="2em"
                    />
                {:else}
                    <Icon icon="ic:sharp-minus" width="2em" />
                {/if}
            </div>
        {/if}
    </div>
</label>

<style lang="postcss">
</style>
