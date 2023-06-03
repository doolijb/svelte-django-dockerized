<script lang="ts">
    /**
     * This is a component that imports the vintage theme and styles.
     */
    import "@vintagelabs/vintage/themes/theme-vintage.css"
    import "@vintagelabs/vintage/styles/all.css"

    export let dark = false
    export let theme = ""
</script>

<div data-theme={theme} class:dark>
    <slot name="body" />
</div>

<style lang="postcss">
    /* :not(.dark) {
        @apply bg-primary-100 text-primary-800;
    }

    .dark {
        @apply bg-primary-100 text-primary-900;
    } */

    /* :not(.dark) :global(th) {
            @apply text-dark;
        }

    .dark :global(th) {
            @apply text-dark;
        } */
</style>
