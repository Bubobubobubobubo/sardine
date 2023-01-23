<script>
	import Editor, { basicSetup } from '$lib/components/Editor.svelte'
	import Header from './Header.svelte';
	import Console from '$lib/components/Console.svelte';
	import { editorMode } from '$lib/store';
	import { vim } from "@replit/codemirror-vim";
	import './styles.css';
	import runnerService from '$lib/services/runnerService';
	import { onMount } from 'svelte';

	const DEFAULT_TEXT = `
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Welcome to the embedded Sardine Code Editor! Press Shift+Enter while selecting text 
# to eval your code. You can select the editing mode through the menubar. Have fun!
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

@swim
def baba(p=0.5, i=0):
	"""I am the default swimming function. Please evaluate me!"""
	D('bd, hh, sn, hh', speed='1,1,0.5')
	again(baba, p=0.5, i=i+1)
`;
	

	let store;
	let codeMirrorState;
	let editorView;

	// The logs are defined as an array of strings
	let logs = []

	// Change the current editing mode.
	let codeMirrorConf = basicSetup
    editorMode.subscribe(value => {
        if (value == 'vim') {
            codeMirrorConf = [basicSetup, vim()]
        } else {
            codeMirrorConf = basicSetup
        }
    })

	function changeHandler({ detail: {tr} }) {
		console.log('change', tr.changes.toJSON())
		console.log('change', $store)
	}

  function keyDownHandler(event) {
    // Shift + Enter
    if(event.key === 'Enter' && event.shiftKey) {
      event.preventDefault(); // Prevents the addition of a new line
      const code = editorView.getSelectedLines();
      runnerService.executeCode(code + "\n\n");
    }
  }

	onMount(() => {
		runnerService.watchLogs((log) => {
			logs = [...logs, log];
		})
	})
</script>

<div class="app">
	<Header />

	<main> 
		<Editor 
		 	bind:this={editorView}
			doc={DEFAULT_TEXT}
			bind:docStore={store}
			bind:effects={codeMirrorState}
			extensions={codeMirrorConf}
			on:change={changeHandler}
			on:keydown={keyDownHandler}
		/>

		<Console {logs}/>
	</main>

	<footer>
	</footer>
</div>

<style>

	.app {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
		color: white;
		background-color: black;
	}

	main {
		flex: 1;
		display: flex;
		flex-direction: column;
		margin: 0 auto;
		box-sizing: border-box;
	}

	footer {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		padding: 12px;
	}

	@media (min-width: 480px) {
		footer {
			padding: 12px 0;
		}
	}

</style>