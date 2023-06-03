<script lang="ts">
    import {popup} from "@skeletonlabs/skeleton"
    import type {IFieldValidator} from "@interfaces"

    export let errors: IFieldValidator[] = []
    export let validators: IFieldValidator[] = []
</script>

{#each validators as validator}
    {#if validator.sticky || errors.includes(validator)}
        <!-- svelte-ignore a11y-click-events-have-key-events Required to make cursor behavior work as intended-->
        <span
            class="badge ms-1 select-none"
            class:variant-soft-primary={!errors.includes(validator)}
            class:variant-soft-error={errors.includes(validator)}
            use:popup={validator.popup}
            on:click={e => {
                e.preventDefault()
                // @ts-ignore
                e.target.event = "click"
            }}
            aria-label={validator.message}
        >
            {validator.badge}
        </span>
        {#if validator.popup}
            <div
                class="card z-10 block p-4"
                class:variant-filled-primary={!errors.includes(validator)}
                class:variant-filled-error={errors.includes(validator)}
                data-popup={validator.popup.target}
            >
                <p>{validator.message}</p>
                <div
                    class="arrow"
                    class:variant-filled-primary={!errors.includes(validator)}
                    class:variant-filled-error={errors.includes(validator)}
                />
            </div>
        {/if}
    {/if}
{/each}

<style lang="postcss">
</style>
