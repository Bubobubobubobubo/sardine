<script lang='ts'>
	import logo from '$lib/images/logo.svg';
	import IconBtn from '$lib/components/buttons/IconBtn.svelte';
	import Button from '$lib/components/buttons/Button.svelte';
	import { editorMode } from '$lib/store';
	import { createEventDispatcher } from 'svelte';
	
	const dispatch = createEventDispatcher();

	function changeMode(): void {
		editorMode.update(n => n === 'emacs' ? 'vim' : 'emacs');
	}
    
</script>

<header>
	<nav>
		<a href="/">
			<img class="logo" src={logo} alt="Sardine logo" />
			<h1>Sardine</h1>
		</a>

		<div class="container">
			<IconBtn icon="play"  on:click={()=>dispatch("play")}/>
			<IconBtn icon="stop"  on:click={()=>dispatch("stop")}/>
			<IconBtn icon="save"  on:click={()=>dispatch("save")}/>
			<IconBtn icon="users" on:click={()=>dispatch("users")}/>
			<IconBtn icon="tutorial" on:click={()=>dispatch("tutorial")}/>
			<IconBtn icon="folder" on:click={()=>dispatch("folder")}/>

			<span 
				on:click={() => { changeMode()}}
				on:keypress={() => {}}
			>
				<Button text={"Mode ["+$editorMode+"]"}/>
			</span>

			<a 
				href="https://sardine.raphaelforment.fr" 
				target="_blank"
				rel="noreferrer"
			>
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
		height: 50px;
	}

	.container {
		display: flex;
		align-items: center;
	}

	a {
        padding: 2px;
		display: flex;
		align-items: center;
		text-decoration: none;
		color: inherit;
	}

	h1 {
		margin-left: 10px;
		font-size: 1.3rem;
	}

</style>
