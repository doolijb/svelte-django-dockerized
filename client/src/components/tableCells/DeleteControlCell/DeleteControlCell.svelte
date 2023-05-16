<script lang="ts">
    import Icon from "@iconify/svelte"

    export let title = "Delete"
    export let onClick: (args: any) => void = () => console.log("onClick")
    export let disabled = false

    let focused = false
</script>

<td class="select-none py-0" {title}>
    <div class="flex items-center items-stretch justify-center pt-2">
        <button
            type="button"
            class="btn-icon btn-icon-sm variant-soft-error"
            {disabled}
            on:click={onClick}
            on:focus={() => (focused = true)}
            on:focusout={() => (focused = false)}
            on:mouseover={() => (focused = true)}
            on:mouseleave={() => (focused = false)}
        >
            <Icon
                icon="mdi:delete"
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
