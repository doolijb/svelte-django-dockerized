<script lang="ts">
    /**
     * This is a component that imports the crimson theme and styles.
     */
    import "@skeletonlabs/skeleton/themes/theme-crimson.css"
    import "@skeletonlabs/skeleton/styles/all.css"

    export let dark = false
    export let theme = ""
</script>

<div class="dark:bg-gray-800" data-theme={theme} class:dark>
    <slot name="body" />
</div>

<style lang="postcss">
    /* :not(.dark) {
        @apply bg-primary-100 text-primary-800;
    } */

    /* .dark {
        @apply text-white-100;
    } */

    /* :not(.dark) :global(th) {
            @apply text-dark;
        }

    .dark :global(th) {
            @apply text-dark;
        } */
</style>
