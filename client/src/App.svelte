<script>
    import { Router, createRouter } from '@roxi/routify'
    import routes from '../.routify/routes.default.js'
    import { accountStore } from './stores'

    $: appReady = false

    const router = createRouter({ routes })

    async function getInitialData() {
        await $accountStore.get()
        appReady = true
    }

    getInitialData()

</script>


{#if appReady}
    <Router {routes} />
{:else}
    <h1>Loading...</h1>
{/if}
