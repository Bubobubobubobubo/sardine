<script lang="ts">
	import logo from '$lib/images/logo.svg';
	import IconBtn from '$lib/components/buttons/IconBtn.svelte';
	import Button from '$lib/components/buttons/Button.svelte';
	import { editorMode } from '$lib/store';
	import { createEventDispatcher } from 'svelte';
	import { noop } from 'svelte/internal';

	let spinLogo = false;

	export function toggleSpinLogo(): void {
		spinLogo = !spinLogo;
	}

	const dispatch = createEventDispatcher();

	function changeMode(): void {
		editorMode.update((n) => (n === 'emacs' ? 'vim' : 'emacs'));
	}
</script>

<header>
	<nav>
		<a href="/">
			<img class="logo" class:spin={spinLogo} src={logo} alt="Sardine logo" />
			<h1>Sardine</h1>
		</a>

		<div class="container">
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
</style>
