<script lang="ts">
    /**
     * Defines a user detail modal view
     */
    import {Modal, modalStore, type ModalSettings} from "@skeletonlabs/skeleton"
    import {onMount} from "svelte"
    import Icon from "@iconify/svelte"

    export let registry: Record<string, any> = null
    export let settings: ModalSettings = null

    function showModal() {
        modalStore.trigger(settings)
    }

    onMount(() => {
        showModal()
    })
</script>

<button class="btn variant-filled" on:click={showModal}>
    <Icon icon="mdi:alert" class="mr-2 h-6 w-6" />
    Show Modal
</button>

<Modal components={registry} />
