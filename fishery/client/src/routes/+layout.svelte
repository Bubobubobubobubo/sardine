<script lang='ts'>
	import Editor, { basicSetup } from '$lib/components/Editor.svelte'
	import Header from './Header.svelte';
	import Console from '$lib/components/Console.svelte';
	import { editorMode, activeTab } from '$lib/store';
	import { get } from 'svelte/store';
	import { vim } from "@replit/codemirror-vim";
	import './styles.css';
	import runnerService from '$lib/services/runnerService';
	import { onMount } from 'svelte';
	import { SardineTheme } from '$lib/SardineTheme.js';
	import { Tabs, TabList, TabPanel, Tab } from '$lib/components/tabs/tabs.js';
	import { keymap } from "@codemirror/view";
	import {indentWithTab} from "@codemirror/commands";
	import { listen, idle, onIdle } from 'svelte-idle';
	let inputted_characters: number = 0;
	const DEFAULT_TEXT: string = `# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Welcome to the embedded Sardine Code Editor! Press Shift+Enter while selecting text 
# to eval your code. You can select the editing mode through the menubar. Have fun!

# PRE WEB EDITOR RELEASE TASK LIST:
# - blinking on evaluation (!!)
# - fix the theme situation (!!)
# - make every button actually do something (!!)
# - make the logs resizable with a mouse handle (!!)
# - keybinding to switch tab and prevent losing focus
# - automatically create buffers folder when installing Sardine
# - shipping a tutorial along with the web editor

# You can play on any tab. They will be saved automatically :) (except scratch : *)
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=



@swim
def baba(p=0.5, i=0):
	"""I am the default swimming function. Please evaluate me!"""
	D('bd, hh, sn, hh', speed='1,1,0.5', i=i)
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

	/*
	 * This function will be called periodically to send the current state
	 * of all the text buffers to the Flask server. They will be parsed to
	 * text files and saved in the APPDIRS/buffers folder for later usage.
	 */ 
	function saveBuffers(buffers: Object) {
		console.log("Running auto-save");
		let buffersToSave = buffers;
		fetch("http://localhost:8000/save", {
				credentials: 'include',
				method: "POST", 
				body: JSON.stringify(buffers),
				headers: {
					"Content-type": "application/json; charset=UTF-8"}
				}
		)
		.then(response => console.log(response));
	};

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
            codeMirrorConf = [
				basicSetup, 
				vim(), 
				keymap.of([indentWithTab]),
				SardineTheme
			]
        } else {
            codeMirrorConf = [
				basicSetup, 
				keymap.of([indentWithTab]),
				SardineTheme
			]
        }
    });

	/**
	 * Intercepting keypresses and triggering action. The current events are covered:
	 * - Editing Mode Change : pressing Ctrl + Space will switch between Vim and Emacs.
	 * - Submitting code : pressing Shift + Enter or Ctrl + E will trigger code eval.
	 * @param event Keypress or combination of multiple keys
	 */
  	function keyDownHandler(event: KeyboardEvent): void {
		// Cancel 'tab' from being used as a navigation key
		if (event.key === "Tab") {
			event.preventDefault();
		}

		// Prevent 'Esc' from defocusing the page (hard to catch)
		if (event.key === "Escape" || event.keyCode === 27) {
			event.preventDefault();
		}


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

		// TODO: implement animation whenever the user evaluates code
		// TODO: implement switching tabs from keybindings
 	}

	/*
	 * Some events are hard to catch on key up but can be prevented by chasing
	 * key up events!
	 */
  	function keyUpHandler(event: KeyboardEvent): void {
		// Prevent 'Esc' from defocusing the page (hard to catch)
		if (event.key === "Escape" || event.keyCode === 27) {
			event.preventDefault();
		}
	};

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

	function handleBufferChange({ detail: {tr} }) {
		// Don't ask me what a tr is, no idea...

		// Getting the currently active tab through introspection
		let tab = get(activeTab);

		// We ignore the scratch buffer! 
		if (tab !== 0) {
			// Writing the content of the buffer to the internal dict.
			SARDINE_BUFFERS["["+(tab-1)+"]"] = tr._doc.text.join('\n');
		}
		
		// Everytime the user enters more than 50 characters, save the files to the disk!
		inputted_characters += 1;
		if (inputted_characters % 50 == 0) {
			saveBuffers(SARDINE_BUFFERS);
		}
	}

	// This will trigger a save rather frequently. This value needs some finetuning
	// to be less aggressive! I wonder what effect it can have on performances.
	listen({
		timer: 10,
		cycle: 500
	}); 
	onIdle(() => {
		saveBuffers(SARDINE_BUFFERS);
	});

</script>

<div class="app">
	<Header 
		on:play={handlePlay}
		on:stop={handleStop}
		on:save={()=> console.log('save')}
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
					on:keyup={keyUpHandler}
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

</style>