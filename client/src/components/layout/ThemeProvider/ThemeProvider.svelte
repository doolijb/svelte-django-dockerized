<script lang="ts">
    import { onMount } from 'svelte';
    /**
     * This is a component that imports the Skeleton theme and styles.
     * It's recommended to choose a theme from themeMap and pass the value into
     * the ThemeProvider theme prop.
    */
    export let theme: string = "skeleton"
    export let darkMode: boolean = false

    let Theme = null

    async function getTheme(theme: string) {

        let importedTheme: Promise<any>

        switch (theme) {
            case "crimson":
                importedTheme = import('../../../themes/Crimson.svelte')
                break
            case "gold-nouveau":
                importedTheme = import('../../../themes/GoldNouveau.svelte')
                break
            case "hamlindigo":
                importedTheme = import('../../../themes/Hamlindigo.svelte')
                break
            case "modern":
                importedTheme = import('../../../themes/Modern.svelte')
                break
            case "seafoam":
                importedTheme = import('../../../themes/Seafoam.svelte')
                break
            case "skeleton":
                importedTheme = import('../../../themes/Skeleton.svelte')
                break
            case "vintage": // TODO: Broken
                importedTheme = import('../../../themes/Vintage.svelte')
                break
        }
        Theme = await importedTheme.then((module) => module.default)
    }

    onMount(async () => {
        await getTheme(theme)
    })

    $: theme ? getTheme(theme) : null

</script>

{#if Theme}
    <svelte:component this={Theme} theme="theme" dark={darkMode}>
        <slot slot="body" />
    </svelte:component>
{/if}
