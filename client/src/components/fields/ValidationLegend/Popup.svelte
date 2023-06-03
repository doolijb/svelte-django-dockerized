<script lang="ts">
    import {ValidStates} from "@constants"
    import type {IFieldValidator} from "@interfaces"
    import type {PopupSettings} from "@skeletonlabs/skeleton"

    export let errors: IFieldValidator[] = []
    export let legendPopup: PopupSettings
    export let validState = ValidStates.NONE
    export let validators: IFieldValidator[] = []
</script>

{#if validators.length}
    <div class="card z-10 w-96 p-4 shadow-xl" data-popup={legendPopup.target}>
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

<style lang="postcss">
</style>
