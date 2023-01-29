<script context="module">
	export const TABS = {};
</script>

<script lang='ts'>
	import { setContext, onDestroy } from 'svelte';
	import { writable, get } from 'svelte/store';
	import { activeTab, selectedTab, selectedPanel } from '$lib/store';

	const tabs: any[] = []; // what is the type of a tab?
	const panels: any[] = []; // what is the type of a panel?

	setContext(TABS, {
		registerTab: tab => {
			tabs.push(tab);
			selectedTab.update(current => current || tab);
			
			onDestroy(() => {
				const i = tabs.indexOf(tab);
				tabs.splice(i, 1);
				selectedTab.update(current => current === tab ? (tabs[i] || tabs[tabs.length - 1]) : current);
			});
		},

		registerPanel: panel => {
			panels.push(panel);
			selectedPanel.update(current => current || panel);
			
			onDestroy(() => {
				const i = panels.indexOf(panel);
				panels.splice(i, 1);
				selectedPanel.update(current => current === panel ? (panels[i] || panels[panels.length - 1]) : current);
			});
		},

		selectTab: tab => {
			const i = tabs.indexOf(tab);
			activeTab.set(i);
			selectedTab.set(tab);
			selectedPanel.set(panels[i]);
		},

		selectedTab,
		selectedPanel
	});
</script>

<div class="tabs">
	<slot></slot>
</div>