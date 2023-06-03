<script lang="ts">
    import {ValidStates} from "@constants"
    import Icon from "@iconify/svelte"
    import {popup, type PopupSettings} from "@skeletonlabs/skeleton"
    import {onMount} from "svelte"
    import type {IFieldValidator} from "@interfaces"

    export let errors: IFieldValidator[] = []
    export let legendPopup: PopupSettings
    export let validState = ValidStates.NONE
    export let validators: IFieldValidator[] = []
    let legendIcon: HTMLDivElement

    onMount(() => {
        // Enforce OOP to give elements a chance to render
        // before we try to attach the popup
        if (validators.length) {
            popup(legendIcon, legendPopup)
        }
    })
</script>

{#if validators.length}
    <!-- svelte-ignore a11y-click-events-have-key-events The event is required for event behavior to work as intended -->
    <!-- We need to execute the attached event, and prevent popagating up on click -->
    <div
        class="input-group-icon cursor-pointer"
        bind:this={legendIcon}
        on:click={e => {
            e.preventDefault()
            // @ts-ignore
            e.target.event = "click"
        }}
        aria-label="Requirements Legend"
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

<style lang="postcss">
</style>
