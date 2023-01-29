<script>
    import { metatags } from '@roxi/routify'
    import { websiteStore } from '../stores'
    import BlockGenerator from '../components/structural/blocks/BlockGenerator/BlockGenerator.svelte'
    import PageHeader from '../components/basic/view/PageHeading/PageHeading.svelte'

    metatags.title = `${$websiteStore.title}`
    metatags.description = $websiteStore.description

    $: page = $websiteStore.pages.find((page) => page.slug === 'index') || {}
</script>

{#if page.showHeader}
    <PageHeader title={page.title} />
{/if}

{#if page.blocks && page.blocks.length > 0 }

<BlockGenerator blocks={page.blocks || []} />

{:else}

<div class="container">
    <div class="no-results text-center text-muted my-5">
        <h5 class="display-6">Welcome to your new Creator Portal</h5>
        <span>There are a few more steps to complete your website.</span>
        <br />
        <br />
        <ol>
            <li>Login and head to the admin panel,</li>
            <li>Go to Meta > Site Options & configure your websites identity,</li>
            <li>Add content to your pages in Meta > Pages,</li>
            <li>Create your first category under Products > Categories,</li>
            <li>Start adding products under Products > Products,</li>
            <li>Give customers access to your products in Meta > Creator Settings,</li>
            <li>Add your patreon client to Social Accounts > Social applications.</li>
        </ol>
        <br>
        <h5>Enjoy!</h5>
        <span>This greeting will disapear when you add content to the <u>index</u> page.</span>
    </div>
</div>

{/if}
