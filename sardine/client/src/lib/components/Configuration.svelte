<script lang="ts">
	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';
	import Modal from './Modal.svelte';

	let showModal = false;
	interface Config {
		midi?: string;
		bpm?: number;
		beats?: number;
		link_clock?: boolean;
		superdirt_handler?: boolean;
		boot_supercollider?: boolean;
		sardine_boot_file?: boolean;
		verbose_superdirt?: boolean;
		superdirt_config_path?: string;
		editor?: boolean;
		debug?: boolean;
		user_config_path?: string;
	}
	let config: Writable<Config> = writable({});

	// Load the config data and store it in the config store on mount
	onMount(async () => {
		const response = await fetch('/config');
		const data = await response.json();
		$config = data; // Update the config store
	});

	const saveConfig = async () => {
		const response = await fetch('/save_config', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify($config) // Use the config store's value
		});
		const result = await response.json();
		console.log(result);
	};

	function resetConfig() {
		// Reset the config store to its initial state
		$config = {};
	}
</script>

<h1>Configuration Tool</h1>

<div class="row">
	<div class="column">
		<button class="button" on:click={resetConfig}>Reset</button>
	</div>
	<div class="column">
		<button class="button" on:click={() => (showModal = true)}>Show</button>
	</div>
</div>

<main>
	<form on:submit|preventDefault={saveConfig}>
		<div class="form-columns">
			<div>
				<fieldset>
					<legend>MIDI</legend>
					<label>
						MIDI Port:
						<input type="text" bind:value={$config.midi} />
					</label>
				</fieldset>

				<fieldset>
					<legend>Clock</legend>
					<label>
						BPM:
						<input type="number" min="20" max="800" step="1" bind:value={$config.bpm} />
					</label>

					<label>
						Beats per Measure:
						<input type="number" min="1" max="999" step="1" bind:value={$config.beats} />
					</label>

					<label>
						Link Clock:
						<input type="checkbox" bind:checked={$config.link_clock} class="big-checkbox" />
					</label>
				</fieldset>
			</div>

			<div>
				<fieldset>
					<legend>SuperCollider</legend>
					<div>
						<label>
							SuperDirt Handler:
							<input
								type="checkbox"
								bind:checked={$config.superdirt_handler}
								class="big-checkbox"
							/>
						</label>

						<label>
							Boot SuperCollider:
							<input
								type="checkbox"
								bind:checked={$config.boot_supercollider}
								class="big-checkbox"
							/>
						</label>
					</div>

					<div>
						<label>
							Sardine Boot File:
							<input
								type="checkbox"
								bind:checked={$config.sardine_boot_file}
								class="big-checkbox"
							/>
						</label>

						<label>
							Verbose SuperDirt:
							<input
								type="checkbox"
								bind:checked={$config.verbose_superdirt}
								class="big-checkbox"
							/>
						</label>
					</div>
					<label>
						SuperCollider Boot Path:
						<input type="text" bind:value={$config.superdirt_config_path} autocomplete="off" />
					</label>
				</fieldset>

				<fieldset>
					<legend>Editor</legend>
					<label>
						Open Embedded Code Editor:
						<input type="checkbox" bind:checked={$config.editor} class="big-checkbox" />
					</label>
				</fieldset>
			</div>
		</div>
		<fieldset>
			<legend>More</legend>
			<label>
				Debug Mode:
				<input type="checkbox" bind:checked={$config.debug} class="big-checkbox" />
			</label>

			<label>
				User Config Path:
				<input type="text" bind:value={$config.user_config_path} autocomplete="off" />
			</label>
		</fieldset>

		<button type="submit">Save</button>
	</form>
</main>

<Modal bind:showModal>
	<pre>{JSON.stringify($config, false, 4)}</pre>
</Modal>

<style>
	button {
		padding-top: 10px;
		padding-bottom: 10px;
		display: block;
		margin: 0 auto;
		width: 100%;
		height: 4rem;
		line-height: 3rem;
		font-size: 1.2rem;
		text-align: center;
		background-color: white;
		color: black;
		border: none;
		outline: none;
	}

	main {
		display: flex;
		flex-direction: column;
		align-items: center;
		color: white;
	}

	.form-columns {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: 1rem;
	}

	h1 {
		text-align: center;
		color: white;
	}
	fieldset {
		padding: 30px;
		height: 150px;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
	}
	.big-checkbox {
		transform: scale(2);
	}

	.row {
		display: flex;
		justify-content: space-between;
		width: 100%;
		margin-bottom: 1rem;
	}

	.column {
		width: 50%;
	}

	label {
		padding-top: 10px;
		padding-bottom: 10px;
		height: 20px;
	}
</style>
