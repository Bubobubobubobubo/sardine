<script lang="ts">
	import Fa from 'svelte-fa';
	import {
		faPlay,
		faStop,
		faFloppyDisk,
		faCircleQuestion,
		faUserGroup,
		faFolder,
		type IconDefinition
	} from '@fortawesome/free-solid-svg-icons';

	// Initialisation of props and events
	export let icon: string = '';

	interface Dictionary<T> {
		[Key: string]: T;
	}

	// Map icon names to FontAwesome glyphs
	const icons: Dictionary<IconDefinition> = {
		play: faPlay,
		stop: faStop,
		save: faFloppyDisk,
		users: faUserGroup,
		help: faCircleQuestion,
		folder: faFolder
	};
</script>

<section>
	<button on:click>
		<Fa class="fa-solid fa-coffee fa-xs" icon={icons[icon]} size="sm" />
	</button>
</section>

<style>
	button {
		background: none;
		color: white;
		border: none;
		padding-top: 1.5vh;
		padding: 1.5vh;
	}

	button:hover {
		transform: scale(1.5);
		cursor: pointer;
		transition: all 0.2s ease-in-out;
	}
</style>
