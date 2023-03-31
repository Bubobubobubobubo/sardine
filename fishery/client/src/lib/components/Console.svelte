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
			setTimeout(() => {
				scrollToTheBottomOfTheConsole();
			}, 0);
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
</style>
