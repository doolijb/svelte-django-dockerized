<script lang="ts">
    import {
        BoolCell,
        DeleteControlCell,
        TextCell,
        ViewControlCell
    } from "@components"
    import Icon from "@iconify/svelte"
    import {
        clipboard,
        Paginator,
        Table,
        tableMapperValues
    } from "@skeletonlabs/skeleton"
    import type {IEmailAddress} from "src/interfaces/index"

    export let emailAddresses = new Map<string, IEmailAddress>()

    export let pageCount = 0

    const iconWidth = "1.5em"

    function getBoolDisplay(value: boolean): string {
        return value ? "TRUE" : "FALSE"
    }
</script>

<div class="table-container">
    <table class="table-hover table text-inherit">
        <thead>
            <tr>
                <th>Id</th>
                <th>Email</th>
                <th class="text-center">Primary</th>
                <th class="text-center">Verified</th>
                <th class="text-center">Emailable</th>
                <th class="text-center">View</th>
                <th class="text-center">Delete</th>
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
                    <ViewControlCell
                        onClick={({e: event, row: EmailAddress}) => {
                            console.log(
                                `View Email Address Clicked for ${row.id}`
                            )
                        }}
                    />
                    <DeleteControlCell
                        onClick={({e: event, row: EmailAddress}) => {
                            console.log(
                                `Delete Email Address Clicked for ${row.id}`
                            )
                        }}
                    />
                </tr>
            {/each}
        </tbody>
    </table>

    <Paginator {pageCount} class="mt-1" />
</div>

<style>
</style>
