<!-- routify:options preload="proximity" -->
<script>
    import HeaderNavBar from '../components/structural/layout/HeaderNavBar/HeaderNavBar.svelte'
    import Footer from '../components/structural/layout/Footer/Footer.svelte'
    import Notifications from 'svelte-notifications'
    import CookieConsent from '../components/composite/consents/CookieConsent/CookieConsent.svelte'
    import { websiteStore, accountStore } from '../stores'
    import { goto, isChangingPage } from '@roxi/routify'

    $: if (!$accountStore.isAuth && !$websiteStore.aknowledgedConsent) {
        $websiteStore.showConsent = true
    }

    $: if ($accountStore.isAuth && !$accountStore.passwordSet) {
        $websiteStore.currentPage.absoluteNavBar = false
        $goto('/account/password/set')
    }

    function handleConsentCloseClick() {
        $websiteStore.showConsent = false
        $websiteStore.aknowledgedConsent = true
    }
</script>

<Notifications>
    <HeaderNavBar />
    <main>
        <slot />
    </main>
    <Footer />
    {#if $websiteStore.showConsent}
        <CookieConsent
            matureContent={$websiteStore.matureContent}
            handleCloseClick={handleConsentCloseClick}
        />
    {/if}
</Notifications>

<style>
    main {
        position: relative;
        overflow-x: hidden;
        min-height: 90vh;
    }
</style>
