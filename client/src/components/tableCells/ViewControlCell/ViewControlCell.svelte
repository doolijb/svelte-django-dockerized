<script lang="ts">
    import Icon from "@iconify/svelte"

    export let disabled = false
    export let onClick = (args: any) => console.log("onClick")
    export let title = "View"

    let focused = false
</script>

<td class="select-none" {title}>
    <div class="flex items-center items-stretch justify-center py-2">
        <button
            type="button"
            class="variant-soft-primary btn-icon btn-icon-sm"
            {disabled}
            on:click={onClick}
            on:focus={() => (focused = true)}
            on:focusout={() => (focused = false)}
            on:mouseover={() => (focused = true)}
            on:mouseleave={() => (focused = false)}
        >
            <Icon
                icon="mdi:eye"
                width="1.5em"
                class={!focused ? "opacity-75" : "opacity-100"}
            />
        </button>
    </div>
</td>

<style>
    td {
        padding: 0 !important;
    }
</style>
