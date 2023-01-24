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
	import { Tabs, TabList, TabPanel, Tab } from '$lib/components/tabs/tabs.js';
	import { selectedPanel, selectedTab } from '$lib/store';
	import  { get } from 'svelte/store';

	const TUTO_BUFFER: string = "There is no tutorial... One will magically appear in a few days :)"
	const DEFAULT_TEXT: string = `# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Welcome to the embedded Sardine Code Editor! Press Shift+Enter while selecting text 
# to eval your code. You can select the editing mode through the menubar. Have fun!

# You can play on any tab. They will be saved automatically :) (except scratch : *)
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

@swim
def baba(p=0.5, i=0):
	"""I am the default swimming function. Please evaluate me!"""
	D('bd, hh, sn, hh', speed='1,1,0.5')
	again(baba, p=0.5, i=i+1)
`;

	/* 
	Initialise a list of code buffers by fetching them from the server.  We are fetching files 
	from the APPDIRS/buffers directory and populating a TS dictionary.  We will then mix them
	up with our own TS-defined local text buffers before populating the tabs. The same mecha-
	nism in reverse is used for saving.
	*/

    interface Dictionary<T> { [Key: string]: T; }
	let SARDINE_BUFFERS: Dictionary<String> = {};
	
	let response = fetch('http://localhost:8000/text_files', {
		credentials: 'include',
		method: 'GET',
	})
	.then(response => response.json())
	.then((data: Object) => {
		for (let [key, value] of Object.entries(data)) {
			SARDINE_BUFFERS["["+key[0]+"]"] = value.toString();
		};
	});

	/* This is the scratch buffer. This specific buffer will never be saved, whatever happens. */
	SARDINE_BUFFERS["[*]"] = DEFAULT_TEXT;

	// Initialise logging
	let logs: string[] = [];


	// Initialise local state
	let store, codeMirrorState, editorView;
	onMount((): void => {
		runnerService.watchLogs((log) => {
			logs = [...logs, log];
		})
	})

	// Monitor the current editing mode (value queried from store)
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
			event.preventDefault(); // Prevents the addition of a newline.
			editorMode.update(n => n === 'emacs' ? 'vim' : 'emacs');
		}

		// Keybindings for changing tab!
		let anyTab: string[] = [
			'1', '&', '2', 'é', '3', '"',
			'4', '\'', '5', '(', '6', '-',
			'7', 'è', '8', '_', '9', 'ç',
			'*'];
		if (anyTab.includes(event.key) && event.ctrlKey) {
			// This stupid conversion method is here to handle AZERTY keyboards.
			// It is not needed at all by any other keyboard layout out there.
			let tabConvert: Dictionary<String> = {
				'&':  '1', 'é':  '2', '"':  '3',
				'\'': '4', '(':  '5', '-':  '6',
				'è':  '7', '_':  '8', 'ç':  '9'
			};
			let real_key: String = (!['1', '2', '3', '4', '5', '6', '7', '8', '9'].includes(event.key))?
				tabConvert[event.key] : event.key;

			// TODO: implement tab selection here!
			console.log('Switch to tab n°' + real_key);
		}

		// TODO: implement animation whenever the user evaluates code
 	}


	/**
	 * Reacting to the play button by resuming the FishBowl.
	 */
	function handlePlay() {
		runnerService.executeCode("bowl.dispatch('resume')")
	}

	/**
	 * Reacting to the pause button by 'pausing' the FishBowl.
	 */
	function handleStop() {
		runnerService.executeCode("bowl.dispatch('pause')")
	}

	/**
	 * Manually save a file somewhere in a local folder.
	 * TODO: implement this mechanism (???)
	 */
	function handleSave() {
		let content = 1;
		console.log('Saving current session');
        const file = new Blob([content], { type: 'text/plain' });
	}

	function handleBufferChange({ detail: {tr} }) {
		// Get the name of the currently active tab
		// Update the dictionary accordingly
		// Profit
		// console.log('change', tr.changes.toJSON())
		// console.log('change', $store)
	}

</script>

<div class="app">
	<Header 
		on:play={handlePlay}
		on:stop={handleStop}
		on:save={handleSave}
		on:users={() => console.log("Users")}
	/>

	<main> 
		<Tabs>
			<TabList>
				{#each Object.entries(SARDINE_BUFFERS) as [name, buffer]}
					<Tab>{name}</Tab>
				{/each}
			</TabList>

		{#each Object.entries(SARDINE_BUFFERS) as [name, buffer]}
			<TabPanel>
				<Editor 
				 	bind:this={editorView}
					doc={buffer}
					bind:docStore={store}
					bind:effects={codeMirrorState}
					extensions={codeMirrorConf}
					on:keydown={keyDownHandler}
					on:change={handleBufferChange}
				/>
			</TabPanel>
		{/each}
		</Tabs>
		<Console {logs}/>
	</main>
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