<script>
	import { Meta, Template, Story } from '@storybook/addon-svelte-csf'
	import Index from './index.svelte'
    import Layout from './_layout.svelte'
    import {exampleWebsiteDefault} from '../stores/website/examples'
    import {exampleAccountDefault} from '../stores/account/examples'

    const defaultArgs = {}
</script>

<Meta
	component={Index}
/>

<Template let:args>
    <Layout website={exampleWebsiteDefault} account={exampleAccountDefault}>
	<Index {...args} />
    </Layout>
</Template>

<Story
	name="Default"
	args={{
		...defaultArgs,
	}}
/>