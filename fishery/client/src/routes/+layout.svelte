<script lang='ts'>
    import FileSaver from 'file-saver';
    import { tick } from 'svelte';
	import type { EditorView } from '@codemirror/view';
    import Editor from '$lib/components/Editor.svelte';
	import _reconfigureExtensions from '$lib/components/Editor.svelte';
	import Header from './Header.svelte';
	import Console from '$lib/components/Console.svelte';
	import { editorMode, activeTab } from '$lib/store';
	import { get } from 'svelte/store';
	import { vim } from "@replit/codemirror-vim";
	import './styles.css';
	import runnerService from '$lib/services/runnerService';
	import { onMount } from 'svelte';
    import { SardineBasicSetup } from '$lib/SardineSetup.js';
	import { Tabs, TabList, TabPanel, Tab } from '$lib/components/tabs/tabs.js';
	import { keymap } from "@codemirror/view";
	import { listen, onIdle } from 'svelte-idle';
	import { default_buffer } from '$lib/DummyText';
	let inputted_characters: number = 0;

	/* =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
	Initialise a list of code buffers by fetching them from the server.  We are fetching files 
	from the APPDIRS/buffers directory and populating a TS dictionary.  We will then mix them
	up with our own TS-defined local text buffers before populating the tabs. The same mecha-
	nism in reverse is used for saving.
	=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
	*/

	// This is the data structure we use for storing text throughout the editor. It is basically
	// a dictionary mapping of the APPDIRS/buffers directory structure.
    interface Dictionary<T> { [Key: string]: T; }
	let SARDINE_BUFFERS: Dictionary<String> = {};
	
	// Fetching from the local server to grab the content of the files.
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
		let buffersToSave = buffers;
		fetch("http://localhost:8000/save", {
				credentials: 'include',
				method: "POST", 
				body: JSON.stringify(buffers),
				headers: {
					"Content-type": "application/json; charset=UTF-8"}
				}
		)
		.then(response => response);
        // There is nothing I can do with the response... 
	};

	/* This is the scratch buffer. This specific buffer will never be saved, whatever happens. */
	/* We are populating it with some dummy information gathered from DummyText.ts  */ 
	SARDINE_BUFFERS["[*]"] = default_buffer;

	/* =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= */
	// Initialise state of the code editor: we don't know anything about the state of anything.
	// We don't really know what we are dealing with and the state is crazy complex. Fun ahead :)
	let logs: string[] = [];
	let extensions: any[] = [];
	$: extensions = extensions;
	let store;
	let codeMirrorState;
	let view: EditorView;

	onMount((): void => {
		runnerService.watchLogs((log) => {
			logs = [...logs, log];
		})
	})

    onMount(() => {
      editorMode.subscribe(value => {
        if (value == 'vim') {
            console.log('Switch to VIM Mode.')
            tick().then(() => {
                view.addVim();
            });
        } else {
            console.log('Switch to Emacs Mode.')
            tick().then(() => {
                view.removeVim();
            });
        }
    });
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
			const code = view.getSelectedLines();
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

    function saveAsTextFile() {
        // Querying the content of the buffer
        let file = new Blob(
            [tr._doc.text.join('\n')],
            { type: "text/plain;charset=utf-8" },
        );
        FileSaver.saveAs(file, "sardine.py");
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
		on:save={saveAsTextFile}
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
                    extensions={extensions};
				 	bind:this={view}
					doc={buffer}
					bind:docStore={store}
					bind:effects={codeMirrorState}
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
