<script>
	import Editor, { basicSetup } from '$lib/components/Editor.svelte'
	import Header from './Header.svelte';
	import Console from '$lib/components/Console.svelte';
	import { editorMode } from '$lib/store';
	import { vim } from "@replit/codemirror-vim"
	
	import './styles.css';

	let store;
	let codeMirrorState;

	const bufferText = `@swim
	def baba():
		D('bd')
		again(baba)`;

	// logs is a array of random logs string
	let logs = [
		"Error  404",
		"Hello World",
		"Hello World",
		"vfsdfsd",
		" Sat  12:00:00",
		"Hello World",
		"Hello World 2",
		"Hello World 2",
		"Hello World 2",
		"Hello World 2",
		"Hello World 2",
		"Hello World 2",
		"Hello World 2",
		"Hello World 2",
		"Hello World 2",
		"Hello World 2",

	]

	// if editorMode is vim, then add vim to the extensions
	let codeMirrorConf = basicSetup
    editorMode.subscribe(value => {
        if (value == 'vim') {
            codeMirrorConf = [basicSetup, vim()]
        } else {
            codeMirrorConf = basicSetup
        }
    })


	function changeHandler({ detail: {tr} }) {
		console.log('change', tr.changes.toJSON())
		console.log('change', $store)
	}

	async function executeCode(code) {
    const data = {
        code: code,
    }
    const response = await fetch('http://localhost:5000/execute', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    const result = await response.json();
    return result;

	}

	function keyDownHandler(e) {
    if(e.key === 'Enter' && e.ctrlKey) {
		e.preventDefault()
		console.log('Ctrl + Enter')
		console.log(codeMirrorConf)
      	executeCode($store);
    }
  }

</script>

<div class="app">
	<Header />

	<main>
		<div on:keydown={keyDownHandler}>
			<Editor doc={bufferText}
									bind:docStore={store}
									bind:effects={codeMirrorState}
									extensions={codeMirrorConf}
									on:change={changeHandler}
									/>
		</div>
		<Console logs={logs}/>
	</main>

	<footer>
	</footer>
</div>

<style>
	.app {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
		color: white;
		background-color: black;
	}

	main {
		flex: 1;
		display: flex;
		flex-direction: column;
		margin: 0 auto;
		box-sizing: border-box;
	}

	footer {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		padding: 12px;
	}

	footer a {
		font-weight: bold;
	}

	@media (min-width: 480px) {
		footer {
			padding: 12px 0;
		}
	}
</style>
