<script>
    import PageHeading from '../components/basic/view/PageHeading/PageHeading.svelte'
    import {leftover} from '@roxi/routify'
</script>

<PageHeading title="Page not found" />

<div class="container">
    <div class="no-results text-center text-muted my-5">
        <h5 class="display-6">404</h5>
        <span>Path: /{$leftover}</span>
    </div>
</div>
