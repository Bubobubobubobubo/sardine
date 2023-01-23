<script lang='ts'>
	import Editor, { basicSetup } from '$lib/components/Editor.svelte'
	import Header from './Header.svelte';
	import Console from '$lib/components/Console.svelte';
	import { editorMode } from '$lib/store';
	import { vim } from "@replit/codemirror-vim";
	import './styles.css';
	import runnerService from '$lib/services/runnerService';
	import { onMount } from 'svelte';
	import { SardineTheme } from '$lib/SardineTheme';

	const DEFAULT_TEXT: string = `# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Welcome to the embedded Sardine Code Editor! Press Shift+Enter while selecting text 
# to eval your code. You can select the editing mode through the menubar. Have fun!
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

@swim
def baba(p=0.5, i=0):
	"""I am the default swimming function. Please evaluate me!"""
	D('bd, hh, sn, hh', speed='1,1,0.5')
	again(baba, p=0.5, i=i+1)
`;
	let store, codeMirrorState, editorView;
	let logs: string[] = [];

	// Service to start when mounting the component.
	onMount((): void => {
		runnerService.watchLogs((log) => {
			logs = [...logs, log];
		})
	})

	// Change the current editing mode.
	let codeMirrorConf = [basicSetup, SardineTheme]
    editorMode.subscribe(value => {
        if (value == 'vim') {
            codeMirrorConf = [basicSetup, vim(), SardineTheme]
        } else {
            codeMirrorConf = [basicSetup, SardineTheme]
        }
    })

	/**
	 * Intercepting keypresses and triggering action. The current events are covered:
	 * - Editing Mode Change : pressing Ctrl + Space will switch between Vim and Emacs.
	 * - Submitting code : pressing Shift + Enter or Ctrl + E will trigger code eval.
	 * @param event Keypress or combination of multiple keys
	 */
  	function keyDownHandler(event: KeyboardEvent): void {
    	// Shift + Enter or Ctrl + E (Rémi Georges mode)
    	if(event.key === 'Enter' && event.shiftKey || event.key === 'e' && event.ctrlKey) {
      		event.preventDefault(); // Prevents the addition of a new line
      		const code = editorView.getSelectedLines();
      		runnerService.executeCode(code + "\n\n");
    	}
		// Keybinding to switch from Emacs mode to Vim Mode
		if(event.key === ' ' && event.ctrlKey) {
			console.log("Evenemnt reçu");
			event.preventDefault(); // Prevents the addition of a newline.
			editorMode.update(n => n === 'emacs' ? 'vim' : 'emacs');
		}
 	}

</script>

<div class="app">
	<Header 
		on:play={() => console.log("Play")}
		on:stop={() => console.log("Stop")}
		on:save={() => console.log("Save")}
		on:users={() => console.log("Users")}
	/>

	<main> 
		<Editor 
		 	bind:this={editorView}
			doc={DEFAULT_TEXT}
			bind:docStore={store}
			bind:effects={codeMirrorState}
			extensions={codeMirrorConf}
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