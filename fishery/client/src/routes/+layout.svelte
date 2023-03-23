<script lang="ts">
	import FileSaver from 'file-saver';
	import { tick } from 'svelte';
	import type { EditorView } from '@codemirror/view';
	import Editor from '$lib/components/Editor.svelte';
	import _reconfigureExtensions from '$lib/components/Editor.svelte';
	import Header from './Header.svelte';
	import Console from '$lib/components/Console.svelte';
	import { editorMode, activeTab } from '$lib/store';
	import { get } from 'svelte/store';
	import { vim } from '@replit/codemirror-vim';
	import './styles.css';
	import runnerService from '$lib/services/runnerService';
	import { onMount } from 'svelte';
	import { SardineBasicSetup } from '$lib/SardineSetup';
	import { Tabs, TabList, TabPanel, Tab } from '$lib/components/tabs/tabs';
	import { keymap } from '@codemirror/view';
	import { tutorialText } from '$lib/text/TutorialText';
	import { Pane, Splitpanes } from 'svelte-splitpanes';

	let inputted_characters = 0;
	let editorHeight, editorWidth;

	/* =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    Initialise a list of code buffers by fetching them from the server.  We are fetching files
    from the APPDIRS/buffers directory and populating a TS dictionary.  We will then mix them
    up with our own TS-defined local text buffers before populating the tabs. The same mecha-
    nism in reverse is used for saving.
    =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
  */

	// This is the data structure we use for storing text throughout the editor. It is basically
	// a dictionary mapping of the APPDIRS/buffers directory structure.
	interface Dictionary<T> {
		[Key: string]: T;
	}

	let SARDINE_BUFFERS: Dictionary<string> = {};

	async function fetchLocalFiles() {
		let response = await fetch('http://localhost:8000/text_files', {
			method: 'GET'
		})
			.then((response) => response.json())
			.then((data: object) => {
				for (let [key, value] of Object.entries(data)) {
					SARDINE_BUFFERS[key] = value.toString();
				}
			});
	}

	fetchLocalFiles();

	// Fetching from the local server to grab the content of the files.

	/*
	 * This function will be called periodically to send the current state
	 * of all the text buffers to the Flask server. They will be parsed to
	 * text files and saved in the APPDIRS/buffers folder for later usage.///
	 */
	function saveBuffers(buffers: object) {
		fetch('http://localhost:8000/save', {
			method: 'POST',
			body: JSON.stringify(buffers),
			headers: {
				'Content-type': 'application/json; charset=UTF-8'
			}
		}).then((response) => response);
		// There is nothing I can do with the response...
	}

	/* =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= */
	// Initialise state of the code editor: we don't know anything about the state of anything.
	// We don't really know what we are dealing with and the state is crazy complex. Fun ahead :)
	/* =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= */

	let logs: string[] = [];
	let extensions: any[] = [];
	$: extensions = extensions;
	let store;
	let codeMirrorState;
	let view: EditorView;

	onMount((): void => {
		runnerService.watchLogs((log) => {
			logs = [...logs, log];
		});
		editorMode.subscribe((value) => {
			if (value == 'vim') {
				console.log('Switch to VIM Mode.');
				tick().then(() => {
					if (view) {
						view.addVim();
					}
				});
			} else {
				console.log('Switch to Emacs Mode.');
				tick().then(() => {
					if (view) {
						view.removeVim();
					}
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
		if (event.key === 'Tab') {
			event.preventDefault();
		}

		// Shift + Enter or Ctrl + E (Rémi Georges mode)
		if ((event.key === 'Enter' && event.shiftKey) || (event.key === 'e' && event.ctrlKey)) {
			event.preventDefault(); // Prevents the addition of a new line
			const code = view.getSelectedLines();
			runnerService.executeCode(code + '\n');
			saveBuffers(SARDINE_BUFFERS);
		}

		if (event.key === 'Enter' && event.ctrlKey) {
			event.preventDefault(); // Prevents the addition of a new line
			const code = view.getCodeBlock();
			runnerService.executeCode(code + '\n');
			saveBuffers(SARDINE_BUFFERS);
		}

		// Keybinding to switch from Emacs mode to Vim Mode
		if (event.key === ' ' && event.ctrlKey) {
			event.preventDefault(); // Prevents the addition of a newline.
			editorMode.update((n) => (n === 'emacs' ? 'vim' : 'emacs'));
		}
	}

	/*
	 * Some events are hard to catch on key up but can be prevented by chasing
	 * key up events!
	 */

	function keyUpHandler(event: KeyboardEvent): void {
		// Prevent 'Esc' from defocusing the page (hard to catch)
		if (event.key === 'Escape' || event.keyCode === 27) {
			event.preventDefault();
		}
	}

	/**
	 * Reacting to the play button by resuming the FishBowl.
	 */
	function handlePlay() {
		runnerService.executeCode("bowl.dispatch('resume')");
	}

	/**
	 * Reacting to the pause button by 'pausing' the FishBowl.
	 */

	function handleStop() {
		runnerService.executeCode("bowl.dispatch('pause')");
	}

	function handleBufferChange({ detail: { tr } }) {
		// Getting the currently active tab through introspection
		let tab = get(activeTab);
		SARDINE_BUFFERS['buffer' + (tab - 1) + '.py'] = tr._doc.text.join('\n');
	}

	function saveAsTextFile() {
		// Querying the content of the buffer
		let file = new Blob([tr._doc.text.join('\n')], { type: 'text/plain;charset=utf-8' });
		FileSaver.saveAs(file, 'sardine.py');
	}

	function spawnTutorial() {
		console.log('Spawning the basic tutorial');
		const tab = get(activeTab);
		// We change the buffer but we need to trigger a redraw as well
		SARDINE_BUFFERS[`buffer${tab}.py`] = tutorialText;
		view._setText(tutorialText);
	}

	function openSardineFolder() {
		// Will ask Flask to open the Sardine default folder
		console.log('Opening Sardine Folder');
		const response = fetch('http://localhost:8000/open_folder', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: {}
		});
	}

	function trimBufferName(name: string) {
		return '[' + name.replace('.py', '').replace('buffer', '') + ']';
	}
</script>

<div class="app">
	<Header
		on:play={handlePlay}
		on:stop={handleStop}
		on:save={saveAsTextFile}
		on:users={() => console.log('Users')}
		on:tutorial={spawnTutorial}
		on:folder={openSardineFolder}
	/>
	<main>
		<Tabs>
			<TabList>
				{#each Object.entries(SARDINE_BUFFERS) as [name, buffer]}
					<Tab>{trimBufferName(name)}</Tab>
				{/each}
				<Tab>Docs</Tab>
			</TabList>

			<Splitpanes
				horizontal="True"
				style="height: 80vh; background-color: black"
				pushOtherPanes="False"
				theme="sardine"
			>
				<Pane maxSize={90} minSize={10} snapSize={10}>
					{#each Object.entries(SARDINE_BUFFERS) as [name, buffer]}
						<TabPanel>
							<Editor
								extensions="{extensions};"
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
					<TabPanel>
						<iframe
							src="https://sardine.raphaelforment.fr"
							title="Sardine website"
							width="100%"
							height="100vh"
							frameborder="0"
							sandbox="allow-same-origin"
							onload="this.style.height=(this.contentWindow.document.body.scrollHeight+20)+'px';"
						/></TabPanel
					>
				</Pane>
				<Pane minSize={10} maxSize={90} snapSize={10}>
					<Console {logs} />
				</Pane>
			</Splitpanes>
		</Tabs>
	</main>
</div>

<style>
	:global(.splitpanes.sardine .splitpanes__pane) {
		background-color: #black;
	}

	.splitpanes.sardine .splitpanes__splitter {
		background-color: #fff;
		box-sizing: border-box;
		position: relative;
		flex-shrink: 0;
	}

	:global(.splitpanes.sardine .splitpanes__splitter:before),
	:global(.splitpanes.sardine .splitpanes__splitter:after) {
		content: '';
		position: absolute;
		top: 50%;
		left: 50%;
		background-color: rgba(0, 0, 0, 0.15);
		transition: background-color 0.3s;
	}

	:global(.splitpanes.sardine .splitpanes__splitter:hover:before),
	:global(.splitpanes.sardine .splitpanes__splitter:hover:after) {
		background-color: rgba(0, 0, 0, 0.25);
	}

	:global(.splitpanes.sardine .splitpanes__splitter:first-child) {
		cursor: auto;
	}

	:global(.sardine.splitpanes .splitpanes .splitpanes__splitter) {
		z-index: 1;
	}

	:global(.sardine.splitpanes--vertical > .splitpanes__splitter),
	:global(.sardine.splitpanes--vertical > .splitpanes__splitter) {
		width: 7px;
		border-left: 1px solid #eee;
		cursor: col-resize;
	}

	:global(.sardine.splitpanes--vertical > .splitpanes__splitter:before),
	:global(.sardine.splitpanes--vertical > .splitpanes__splitter:after),
	:global(.sardine.splitpanes--vertical > .splitpanes__splitter:before),
	:global(.sardine.splitpanes--vertical > .splitpanes__splitter:after) {
		transform: translateY(-50%);
		width: 1px;
		height: 30px;
	}

	:global(.sardine.splitpanes--vertical > .splitpanes__splitter:before),
	:global(.sardine.splitpanes--vertical > .splitpanes__splitter:before) {
		margin-left: -2px;
	}

	:global(.sardine.splitpanes--vertical > .splitpanes__splitter:after),
	:global(.sardine.splitpanes--vertical > .splitpanes__splitter:after) {
		margin-left: 1px;
	}

	:global(.sardine.splitpanes--horizontal > .splitpanes__splitter),
	:global(.sardine.splitpanes--horizontal > .splitpanes__splitter) {
		height: 7px;
		border-top: 1px solid #eee;
		cursor: row-resize;
	}

	:global(.sardine.splitpanes--horizontal > .splitpanes__splitter:before),
	:global(.sardine.splitpanes--horizontal > .splitpanes__splitter:after),
	:global(.sardine.splitpanes--horizontal > .splitpanes__splitter:before),
	:global(.sardine.splitpanes--horizontal > .splitpanes__splitter:after) {
		transform: translateX(-50%);
		width: 30px;
		height: 1px;
	}

	:global(.sardine.splitpanes--horizontal > .splitpanes__splitter:before),
	:global(.sardine.splitpanes--horizontal > .splitpanes__splitter:before) {
		margin-top: -2px;
	}

	:global(.sardine.splitpanes--horizontal > .splitpanes__splitter:after),
	:global(.sardine.splitpanes--horizontal > .splitpanes__splitter:after) {
		margin-top: 1px;
	}

	.app {
		display: flex;
		flex-direction: column;
		min-height: 99vh;
		color: black;
		background-color: black;
	}

	main {
		flex: 1;
		display: flex;
		flex-direction: column;
		margin: 0 auto;
		box-sizing: border-box;
	}

	iframe {
		flex: 1;
		display: flex;
		flex-direction: column;
		margin: 0 auto;
		box-sizing: border-box;
		height: 99vh;
		width: 99vw;
	}
</style>
