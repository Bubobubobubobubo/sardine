<script lang="ts">
	import logo from '$lib/images/logo.svg';
	import IconBtn from '$lib/components/buttons/IconBtn.svelte';
	import { editorMode } from '$lib/store';
	import { createEventDispatcher } from 'svelte';
	import { tutorialText } from '$lib/text/TutorialText';
	import { Button, Offcanvas } from 'sveltestrap';

	let spinLogo = false;
	export function toggleSpinLogo(): void {
		spinLogo = !spinLogo;
	}
	const dispatch = createEventDispatcher();
</script>

<header>
	<nav>
		<a href="/">
			<img class="logo" class:spin={spinLogo} src={logo} alt="Sardine logo" />
			<h1>Sardine</h1>
		</a>

		<div class="container">
			<div class="dropdown">
				<button class="dropbtn">[Help]</button>
				<div class="dropdown-content">
					{#each Object.entries(tutorialText) as [title, content]}
						<a href="" on:click|preventDefault={() => dispatch('loadtutorial', { text: content })}>
							{title}
						</a>
					{/each}
				</div>
			</div>
			<IconBtn icon="play" on:click={() => dispatch('play')} />
			<IconBtn icon="stop" on:click={() => dispatch('stop')} />
			<IconBtn icon="save" on:click={() => dispatch('save')} />
			<IconBtn icon="users" on:click={() => dispatch('users')} />
			<IconBtn icon="help" on:click={() => dispatch('help')} />
			<IconBtn icon="folder" on:click={() => dispatch('folder')} />
		</div>
	</nav>
</header>

<style>
	nav {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	nav {
		height: 4vh;
	}

	nav .logo {
		width: auto;
		height: 5vh;
		padding-top: 1vh;
	}

	.container {
		display: flex;
		align-items: center;
		height: 4vh;
	}

	a {
		padding: 2px;
		display: flex;
		align-items: center;
		text-decoration: none;
		color: inherit;
	}

	h1 {
		margin-left: 1vw;
		font-size: 3.5vh;
		color: white;
		padding-top: 1vh;
	}

	@keyframes spin {
		0% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(360deg);
		}
	}

	.spin {
		animation: spin 0.5s linear infinite;
	}

	/* Dropdown Button */
	.dropbtn {
		background-color: black;
		color: white;
		padding: 2vh;
		font-size: 1.5vw;
		border: none;
	}

	/* The container <div> - needed to position the dropdown content */
	.dropdown {
		padding-top: 0.5vh;
		position: relative;
		display: inline-block;
	}

	/* Dropdown Content (Hidden by Default) */
	.dropdown-content {
		display: none;
		position: absolute;
		background-color: white;
		min-width: 3vw;
		box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
		z-index: 1;
	}

	/* Links inside the dropdown */
	.dropdown-content a {
		color: black;
		padding: 6px 12px;
		width: 25vw;
		text-decoration: none;
		font-size: 0.75vw;
		display: block;
	}

	/* Change color of dropdown links on hover */
	.dropdown-content a:hover {
		background-color: black;
		color: white;
	}

	/* Show the dropdown menu on hover */
	.dropdown:hover .dropdown-content {
		display: block;
	}

	/* Change the background color of the dropdown button when the dropdown content is shown */
	.dropdown:hover .dropbtn {
		background-color: black;
	}
</style>
