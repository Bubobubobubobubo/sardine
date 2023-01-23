<script context="module">
    import { EditorView, minimalSetup, basicSetup,  } from 'codemirror'
    import { ViewPlugin } from '@codemirror/view'
    import { StateEffect } from '@codemirror/state'
    import {python} from "@codemirror/lang-python"
    export { minimalSetup, basicSetup }
</script>

<script>

  import { onMount, onDestroy, createEventDispatcher } from 'svelte';
	import { SardineTheme } from '$lib/SardineTheme';


    const dispatch = createEventDispatcher();
    let dom;
    let _mounted = false;

    /*
     * Setting some weird internal flags when the component is mounted.
    */
    onMount(() => {
      _mounted = true
      return () => { _mounted = false }
    });

    /**
     * Getting rid of the CodeMirror Editor when the component is destroyed.
    */
    onDestroy(() => {
      if (view) {
        view.destroy()
      }
    });

    /**
     * @type {EditorView}
     */
    export let view;
    
    /* `doc` is deliberately made non-reactive for not storing a reduntant string
    besides the editor. Also, setting doc to undefined will not trigger an
    update, so that you can clear it after setting one. */

    export let doc;
    
    /* Set this if you would like to listen to all transactions via `update` event. */
    export let verbose = false
    
    /* Cached doc string so that we don't extract strings in bulk over and over. */
    let _docCached = null
    
    /* Overwrite the bulk of the text with the one specified. */
    function _setText(text) {
      view.dispatch({
        changes: {from: 0, to: view.state.doc.length, insert: text},
      })
    }
    
    const subscribers = new Set();
    
    /* And here comes the reactivity, implemented as a r/w store. */
    export const docStore = {
      ready: () => (!!view),
      subscribe(cb) {
        subscribers.add(cb)
    
        if (!this.ready()) {
          cb(null)
        } else {
          if (_docCached == null) {
            _docCached = view.state.doc.toString()
          }
          cb(_docCached)
        }
    
        return () => void subscribers.delete(cb)
      },
      set(newValue) {
        if (!_mounted) {
          throw new Error('Cannot set docStore when the component is not mounted.')
        }
    
        const inited = _initEditorView(newValue)
        if (!inited) _setText(newValue)
      },
    }
    
    export let extensions;
    // add python language support
    extensions.push(python({}))
    extensions.push(SardineTheme);

    
    function _reconfigureExtensions() {
      if (!view) return
      view.dispatch({
        effects: StateEffect.reconfigure.of(extensions),
      })
    };
    
    $: extensions, _reconfigureExtensions()
    
    function _editorTxHandler(tr) {
      this.update([tr])
    
      if (verbose) {
        dispatch('update', tr)
      };
    
      if (tr.docChanged) {
        _docCached = null
        if (subscribers.size) {
          dispatchDocStore(_docCached = tr.newDoc.toString())
        }
        dispatch('change', {view: this, tr})
      }
    }
    
    function dispatchDocStore(s) {
      for (const cb of subscribers) {
        cb(s)
      }
    }


  export function getSelectedLines() {
    // Get the current state of the editor
    const state = view.state;

    // Get the current selection
    const { from, to } = state.selection.main

    // Get the line the cursor is currently on
    const fromLine = state?.doc.lineAt(from)
    const toLine = state?.doc.lineAt(to)

    return state?.doc.sliceString(fromLine.from, toLine.to)
  }
  
    
    // the view will be inited with the either doc (as long as that it is not `undefined`)
    // or the value in docStore once set
    function _initEditorView(initialDoc) {
      if (view) {
        return false
      }
    
      view = new EditorView({
        doc: initialDoc,
        extensions,
        parent: dom,
        dispatch: _editorTxHandler,
      })

      view.dispatch({
          effects: StateEffect.appendConfig.of([
          ViewPlugin.define((view) => {
              view.dom.classList.add('editor')
              view.dom.style.height = '70vh'
              view.dom.style.width = '99vw'
              return {}
          }),
        ]),
      })
      
      return true
    }
    
    $: if (_mounted && doc !== undefined) {
      const inited = _initEditorView(doc)
      dispatchDocStore(doc)
    }
    
    

</script>
    
<div class="codemirror" 
  bind:this={dom}
  on:keydown
  >
</div>
    
<style>
    .codemirror {
      display: contents;
    }
    
</style>