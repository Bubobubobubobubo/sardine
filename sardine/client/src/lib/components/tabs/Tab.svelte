<script>
	import { getContext } from 'svelte';
	import { TABS } from './Tabs.svelte';

	const tab = {};
	const { registerTab, selectTab, selectedTab } = getContext(TABS);

	registerTab(tab);
</script>

<button class:selected={$selectedTab === tab} on:click={() => selectTab(tab)}>
	<slot />
</button>

<style>
	button {
		background: none;
		border: none;
		border-radius: 0;
		margin: 0;
		font-size: 1.5vw;
		color: white;
	}

	button:hover {
		transform: scale(1.1);
	}

	.selected {
		border-bottom: 2px solid white;
		color: white;
	}
</style>

