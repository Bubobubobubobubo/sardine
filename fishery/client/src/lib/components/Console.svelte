<script lang="ts">
	import { tick } from 'svelte';

	export let logs: Array<string> = [];
	export let autoScroll: boolean = true;
	let consoleView: HTMLDivElement;

	const scrollToTheBottomOfTheConsole = () => {
		if (!autoScroll) return;
		if (!consoleView) return;
		consoleView.scrollTop = consoleView.scrollHeight;
	};

	// watch for changes in the logs array and scroll to the bottom of the console
	$: {
		logs;
		tick().then(() => {
			scrollToTheBottomOfTheConsole();
		});
	}
</script>

<div class="console">
	<div class="console-content" bind:this={consoleView}>
		<ul>
			{#each logs as log}
				<li><pre>{log}</pre></li>
			{/each}
		</ul>
	</div>
</div>

<style>
	.console {
		color: white;
	}

	.console-header {
		display: flex;
		align-items: center;
	}

	h3 {
		font-size: 14px;
		padding-left: 15px;
		margin-left: 15px;
		padding: 4px;
		cursor: pointer;
	}

	h3:hover {
		color: black;
		background-color: white;
		transition: all 0.2s ease-in-out;
	}

	h3.active {
		color: black;
		background-color: white;
	}

	.console-content {
		font-size: 16px;
		height: 500px;
		overflow-y: scroll;
	}

	.console-content ul {
		font-size: 16px;
		list-style: none;
		padding: 0;
		margin: 0;
		background: black;
		color: #e6e6e6;
	}

	pre {
		margin: 0em;
		font-family: monospace;
	}

	.console-content li {
		font-size: 14px;
		padding: 0px 5px;
	}

	.splitpanes.default-theme .splitpanes__pane {
		background-color: black;
	}

	/*
    .console-content li:nth-child(odd){
        background-color: #777777;
    }
    */
</style>
