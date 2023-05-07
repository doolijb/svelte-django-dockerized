<script lang="ts">
    import type { EmailAddress } from "src/interfaces/index"
    import { BoolCell, TextCell, DeleteControlCell, EditControlCell } from '@components'
    import Icon from "@iconify/svelte";
    import { clipboard, Paginator, Table, tableMapperValues } from "@skeletonlabs/skeleton"

    export let emailAddresses = new Map<string, EmailAddress>();

    export let pageCount = 0;

    const iconWidth = "1.5em";

    function getBoolDisplay(value: boolean): string {
        return value ? "TRUE" : "FALSE";
    }

</script>

<div class="table-container">
    <table class="table table-hover text-inherit">
        <thead>
            <tr>
                <th>Id</th>
                <th>Email</th>
                <th>Primary</th>
                <th>Verified</th>
                <th>Emailable</th>
                <th>Edit</th>
                <th>Delete</th>
            </tr>
        </thead>
        <tbody>
            {#each [...emailAddresses.values()] as row}
                <tr>
                    <TextCell text={row.id.slice(0, 8)} />
                    <TextCell text={row.email} />
                    <BoolCell value={row.isPrimary} />
                    <BoolCell value={row.isVerified} />
                    <td title={row.emailable_type.toLocaleUpperCase()}>
                        {#if row.emailable_type === "user"}
                            <Icon icon="mdi:user" width={iconWidth} />
                        {:else}
                            <Icon
                                icon="ant-design:file-unknown-filled"
                                width={iconWidth}
                            />
                        {/if}
                    </td>
                    <EditControlCell
                        onClick={({e: event, row: EmailAddress}) => {
                            console.log(`Edit Email Address Clicked for ${row.id}`);
                        }}
                    />
                    <DeleteControlCell
                        onClick={({e: event, row: EmailAddress}) => {
                            console.log(`Delete Email Address Clicked for ${row.id}`);
                        }}
                    />
                </tr>
            {/each}
        </tbody>
    </table>

    <Paginator pageCount={pageCount} class="mt-1" />

</div>

<style>
</style>
