<script lang="ts">
    import Icon from "@iconify/svelte";

    export let title: string = "Delete"
    export let onClick = (args: any) => {}
    export let disabled: boolean = false

    let focused = false

</script>

<td
    class="select-none"
    {title}
>
    <button
        type="button"
        class="btn-icon btn-icon-sm variant-soft-error"
        {disabled}
        on:click={onClick}
        on:focus={() => focused = true}
        on:focusout={() => focused = false}
        on:mouseover={() => focused = true}
        on:mouseleave={() => focused = false}
        >
        <Icon icon="mdi:delete" width="1.5em" class="{!focused ? 'opacity-75' : 'opacity-100'}"/>
    </button>
</td>

<style></style>
