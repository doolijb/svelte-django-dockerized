<script lang="ts">
    import Icon from "@iconify/svelte"

    export let title: string | null = null
    export let value: boolean | null = null

    function getBoolDisplay(value: boolean): string {
        if (typeof value === "undefined" || value === null) {
            return "NONE"
        }
        return value ? "TRUE" : "FALSE"
    }

    const iconWidth = "1.5em"
</script>

<td title={title || getBoolDisplay(value)}>
    <div class="flex items-center items-stretch justify-center">
        {#if value}
            <Icon
                class="inline"
                icon="ant-design:check-circle-filled"
                width={iconWidth}
            />
        {:else if value === false}
            <Icon
                class="text-surface-500"
                icon="ant-design:close-circle-filled"
                width={iconWidth}
            />
        {:else}
            <Icon
                class="text-surface-500"
                icon="ant-design:question-circle-filled"
                width={iconWidth}
            />
        {/if}
    </div>
</td>

<style></style>
