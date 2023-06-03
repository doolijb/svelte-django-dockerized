<script lang="ts">
    /**
     * This is a component that imports the skeleton theme and styles.
     */
    import "@skeletonlabs/skeleton/themes/theme-skeleton.css"
    import "@skeletonlabs/skeleton/styles/all.css"

    export let dark = false
    export let theme = ""
</script>

<div class="dark:text-gray-100" data-theme={theme} class:dark>
    <slot name="body" />
</div>

<style lang="postcss">
    /* :not(.dark) {
        @apply bg-primary-100 text-primary-800;
    } */

    /* :not(.dark) :global(th) {
            @apply text-dark;
        }

    .dark :global(th) {
            @apply text-dark;
        } */
</style>
