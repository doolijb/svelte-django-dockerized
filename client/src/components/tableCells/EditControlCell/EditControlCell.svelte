<script lang="ts">
    import Icon from "@iconify/svelte";

    export let title: string = "Edit"
    export let onClick = (args: any) => {}
    export let disabled: boolean = false

    let focused = false
</script>

<td
    class="select-none py-0 h-100"
    {title}
>
<div class="flex items-stretch items-center justify-center">
            <button
                type="button"
                class="btn-icon btn-icon-sm variant-soft-primary"
                {disabled}
                on:click={onClick}
                on:focus={() => focused = true}
                on:focusout={() => focused = false}
                on:mouseover={() => focused = true}
                on:mouseleave={() => focused = false}
                >
                <Icon icon="mdi:gear" width="1.5em" class="{!focused ? 'opacity-75' : 'opacity-100'}"/>
            </button>
            </div>
</td>

<style>
    td {
        padding: 0 !important;
    }
</style>
