<script lang="ts">
    import Icon from "@iconify/svelte"
    import {clipboard} from "@skeletonlabs/skeleton"

    export let copy: string = null
    export let text = ""

    $: copyText = copy ? copy : text
    $: title = copyText ? "Click to copy" : ""

    let focused = false
</script>

<!-- svelte-ignore missing-declaration -->
<td
    class="select-none"
    {title}
    use:clipboard={copyText}
    on:focus={() => (focused = true)}
    on:focusout={() => (focused = false)}
    on:mouseover={() => (focused = true)}
    on:mouseleave={() => (focused = false)}
>
    <slot {text}>
        <span class="flex">
            {text}
            {#if copyText}
                <Icon
                    icon="mdi:content-copy"
                    class="ms-2 mt-1 {!focused ? "invisible" : ""}"
                />
            {/if}
        </span>
    </slot>
</td>

<style></style>
