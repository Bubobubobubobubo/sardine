<script context="module">
	import { EditorView, minimalSetup, basicSetup } from 'codemirror';
	import { ViewPlugin } from '@codemirror/view';
	import { StateEffect } from '@codemirror/state';
</script>

<script lang="ts">
	import { onMount, onDestroy, createEventDispatcher } from 'svelte';
	import { SardineBasicSetup } from '$lib/SardineSetup';
	import { vim } from '@replit/codemirror-vim';
	import { StateField } from '@codemirror/state';
	import { Decoration } from '@codemirror/view';

	// Implement the blinking effect when evaluating text!
	const blinking_effect = StateEffect.define();
	const unblinking_effect = StateEffect.define();
	const blinking_extension = StateField.define({
		create() {
			return Decoration.none;
		},

		// Solution ici : https://discuss.codemirror.net/t/how-to-remove-a-decoration-mark-from-state/3809/3
		update(value, transaction) {
			value = value.map(transaction.changes);
			for (let effect of transaction.effects) {
				try {
					if (effect.is(blinking_effect)) {
						value = value.update({
							add: effect.value,
							sort: true
						});
					} else if (effect.is(unblinking_effect)) {
						value = value.update({
							filter: (f, t, value) => {
								value.class === 'XYZ';
							}
						});
					}
				} catch (err) {
					console.log(err);
				}
			}
			return value;
		},
		provide: (f) => EditorView.decorations.from(f)
	});

	const blinking_decoration = Decoration.mark({
		attributes: {
			style: 'background-color: orange'
		},
		class: 'red_back'
	});

	const unblinking_decoration = Decoration.mark({
		attributes: {
			style: 'background-color: black'
		},
		class: 'black'
	});

	const dispatch = createEventDispatcher();
	let _mounted: boolean = false;
	export let view: EditorView;
	export let dom;

	onMount((): Function => {
		_mounted = true;
		return () => {
			_mounted = false;
		};
	});

	onDestroy(() => {
		if (view) {
			view.destroy();
		}
	});

	/* `doc` is deliberately made non-reactive for not storing a reduntant string
  besides the editor. Also, setting doc to undefined will not trigger an update,
  so that you can clear it after setting one. */
	export let doc: string;

	/* Set this if you would like to listen to all transactions via `update` event. */
	export let verbose: boolean = false;

	/* Cached doc string so that we don't extract strings in bulk over and over. */
	let _docCached: string = '';

	/* Overwrite the bulk of the text with the one specified. */
	export function _setText(text: string): void {
		view.dispatch({
			changes: { from: 0, to: view.state.doc.length, insert: text }
		});
	}

	const subscribers = new Set();

	/* And here comes the reactivity, implemented as a r/w store. */
	export const docStore = {
		ready: () => !!view,
		subscribe(cb) {
			subscribers.add(cb);

			if (!this.ready()) {
				cb(null);
			} else {
				if (_docCached == null) {
					_docCached = view.state.doc.toString();
				}
				cb(_docCached);
			}

			return () => void subscribers.delete(cb);
		},
		set(newValue) {
			if (!_mounted) {
				throw new Error('Cannot set docStore when the component is not mounted.');
			}

			const inited = _initEditorView(newValue);
			if (!inited) _setText(newValue);
		}
	};

	// What is the expected type of extensions?
	export let extensions: any[];
	let extensionsWithVim = [SardineBasicSetup, vim(), blinking_extension];
	let extensionsWithoutVim = [SardineBasicSetup, blinking_extension];
	extensions = extensionsWithoutVim;

	export function addVim() {
		extensions = extensionsWithVim;
	}

	export function removeVim() {
		extensions = extensionsWithoutVim;
	}

	function _reconfigureExtensions(): void {
		if (!view) return;
		view.dispatch({
			effects: StateEffect.reconfigure.of(extensions)
		});
	}

	$: extensions, _reconfigureExtensions();

	function _editorTxHandler(tr): void {
		this.update([tr]);

		if (verbose) {
			dispatch('update', tr);
		}

		if (tr.docChanged) {
			_docCached = '';
			if (subscribers.size) {
				dispatchDocStore((_docCached = tr.newDoc.toString()));
			}
			dispatch('change', { view: this, tr });
		}
	}

	function dispatchDocStore(s) {
		for (const cb of subscribers) {
			cb(s);
		}
	}

	export function getCodeBlock(): string {
		// Get the current state of the editor
		const state = view.state;

		// Get the current selection
		const { head } = state.selection.main;

		// Get the line the cursor is currently on
		const currentLine = state.doc.lineAt(head);

		// Find the start and end of the code block
		let startLine = currentLine;
		while (startLine.number > 1 && !/^\s*$/.test(state.doc.line(startLine.number - 1).text)) {
			startLine = state.doc.line(startLine.number - 1);
		}

		let endLine = currentLine;
		while (
			endLine.number < state.doc.lines &&
			!/^\s*$/.test(state.doc.line(endLine.number + 1).text)
		) {
			endLine = state.doc.line(endLine.number + 1);
		}

		// Blink the text!
		view.dispatch({
			effects: blinking_effect.of([blinking_decoration.range(startLine.from, endLine.to)])
		});

		setTimeout(() => {
			view.dispatch({
				effects: unblinking_effect.of([unblinking_decoration.range(startLine.from, endLine.to)])
			});
		}, 400);

		return state.doc.sliceString(startLine.from, endLine.to);
	}

	export function getSelectedLines(): string {
		// Get the current state of the editor
		const state = view.state;

		// Get the current selection
		const { from, to } = state.selection.main;

		// Get the line the cursor is currently on
		const fromLine = state?.doc.lineAt(from);
		const toLine = state?.doc.lineAt(to);

		// Blink the text!
		view.dispatch({
			effects: blinking_effect.of([blinking_decoration.range(fromLine.from, toLine.to)])
		});

		setTimeout(() => {
			view.dispatch({
				effects: unblinking_effect.of([unblinking_decoration.range(fromLine.from, toLine.to)])
			});
		}, 400);

		return state?.doc.sliceString(fromLine.from, toLine.to);
	}

	// the view will be inited with the either doc (as long as that it is not `undefined`)
	// or the value in docStore once set
	function _initEditorView(initialDoc): boolean {
		if (view) {
			return false;
		}

		view = new EditorView({
			doc: initialDoc,
			extensions: extensions,
			parent: dom,
			dispatch: _editorTxHandler
		});

		view.dispatch({
			effects: StateEffect.appendConfig.of([
				ViewPlugin.define((view) => {
					view.dom.classList.add('editor');
					view.dom.style.height = '10%';
					view.dom.style.width = '99vw';
					return {};
				})
			])
		});

		return true;
	}

	$: if (_mounted && doc !== undefined) {
		const inited = _initEditorView(doc);
		dispatchDocStore(doc);
	}
</script>

<div class="codemirror" bind:this={dom} on:keydown />

<style>
	.codemirror {
		background-color: black;
	}
</style>
