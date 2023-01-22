<script>
	import logo from '$lib/images/logo.svg';
	import IconBtn from '$lib/components/buttons/IconBtn.svelte';
	import Button from '$lib/components/buttons/Button.svelte';
	import { editorMode } from '$lib/store';


	function changeMode() {
		editorMode.update(n => n === 'emacs' ? 'vim' : 'emacs');
		console.log($editorMode);
	}
	

</script>

<header>
	<nav>
		<a href="/">
			<img class="logo" src={logo} alt="Sardine logo" />
			<h1>Sardine</h1>
		</a>

		<div class="container">
			<IconBtn icon="play"/>
			<IconBtn icon="stop"/>
			<IconBtn icon="save"/>
			<IconBtn icon="users"/>

			<span on:click={() => {changeMode()}}><Button text={"Mode ["+$editorMode+"]"}/></span>
			<a href="https://sardine.raphaelforment.fr" target="_blank">
				<Button text="Open Docs" />
			</a>
		</div>
	
	</nav>


</header>

<style>
	nav {
		display: flex;
		justify-content: space-between;
		padding: 15px;
		align-items: center;
		height: 5vh;
	}
	nav .logo {
		width: auto;
		height: 25px;
	}

	.container {
		display: flex;
		align-items: center;
	}

	a {
		display: flex;
		align-items: center;
		text-decoration: none;
		color: inherit;
	}

	h1 {
		margin-left: 10px;
		font-size: 1.8rem;
	}
</style>
