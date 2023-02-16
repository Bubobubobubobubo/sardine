<script>
    import SvelteMarkdown from 'svelte-markdown'

    // read doc from lib/text/Docs.md and pass it to SvelteMarkdown
    //
    import Docs from '$lib/text/doc.md?raw'

    export let source = Docs

</script>
<section>
    <SvelteMarkdown {source} />
</section>