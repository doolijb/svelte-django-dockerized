<script lang="ts">
    import {
        BoolCell,
        DeleteControlCell,
        TextCell,
        ViewControlCell as ViewControlCell
    } from "@components"
    import Icon from "@iconify/svelte"
    import {
        clipboard,
        Paginator,
        Table,
        tableMapperValues
    } from "@skeletonlabs/skeleton"
    import type {IUser} from "src/interfaces/index"

    export let pageCount = 0

    export let users = new Map<string, IUser>()

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
                <th>Username</th>
                <th class="text-center">Admin</th>
                <th>Created</th>
                <th>View</th>
                <th>Delete</th>
            </tr>
        </thead>
        <tbody>
            {#each [...users.values()] as row}
                <tr>
                    <TextCell text={row.id.slice(0, 8)} />
                    <TextCell text={row.username} />
                    <BoolCell value={row.isAdmin} />
                    <TextCell text={row.created_at} />
                    <ViewControlCell
                        onClick={({e: event, row: User}) => {
                            console.log(`View User Clicked for ${row.id}`)
                        }}
                    />
                    <DeleteControlCell
                        onClick={({e: event, row: User}) => {
                            console.log(`Delete User Clicked for ${row.id}`)
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
