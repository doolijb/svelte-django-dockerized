<script lang="ts">
    import type {User} from "@interfaces"
    import {ReviewModes} from "@constants"
    import {onMount} from "svelte"

    export let mode: string = ReviewModes.CREATE
    console.log("mode", mode)
    export let user: User | undefined | null = null

    export let formData = {
        user: {
            username: "",
            firstName: "",
            lastName: "",
            email: "",
            password: "",
            passwordConfirm: ""
        }
    }

    const invalidFields: string[] = ["username"]

    onMount(() => {
        if (user && mode === ReviewModes.EDIT) {
            formData.user = {
                ...formData.user,
                ...user
            }
        }
    })
</script>

<!-- USERNAME -->
<div class="my-4 flex flex-row">
    <label class="label mx-2 grow">
        <span>Username</span>
        {#if mode === ReviewModes.CREATE || mode === ReviewModes.EDIT}
            <input
                class="input variant-form-material"
                class:input-error={invalidFields.includes("username")}
                type="text"
                bind:value={formData.user.username}
            />
        {:else if mode === ReviewModes.VIEW && user}
            <div class="input variant-form-material">
                {user.username}
            </div>
        {/if}
    </label>
</div>

<!-- EMAIL ADDRESS -->
<div class="my-4 flex flex-row">
    <label class="label mx-2 grow">
        <span>Email Address</span>
        <input
            bind:value={formData.user.email}
            class="input variant-form-material"
            class:input-error={invalidFields.includes("email")}
            type="email"
        />
    </label>
</div>

<div class="my-4 flex flex-row">
    <label class="label mx-2 grow">
        <span>Password</span>
        <input
            bind:value={formData.user.email}
            class="input variant-form-material"
            class:input-error={invalidFields.includes("email")}
            type="email"
        />
    </label>
</div>
