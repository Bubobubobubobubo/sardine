import React, { useEffect, useRef } from 'react';
import CodeMirror, { useCodeMirror } from '@uiw/react-codemirror';
import { python } from '@codemirror/lang-python';
import { vim } from "@replit/codemirror-vim";
import Menubar from './components/Menubar.js';
import Log from './components/Log.js';
import { executeCode } from './libs/service/runnerService.js';

function App() {
  const templateCode = `@swim
def baba():
    D('bd')
    again(baba)` + '\n'.repeat(40);

  const onChange = React.useCallback((value, viewUpdate) => {
    console.log('value:', value);
  }, []);

  function kedDownHandler(event) {
    // Ctrl + Enter
    if(event.key === 'Enter' && event.ctrlKey) {
      console.log(getSelectedLines());
      executeCode(getSelectedLines());
    }
  }

  function getSelection() {
    const { from, to } = codeMirror.current?.view?.state?.selection.main
    return codeMirror.current?.view?.state?.doc.sliceString(from, to)
  }

  function getSelectedLines() {
    // Get the current state of the editor
    const state = codeMirror.current?.view?.state;

    // Get the current selection
    const { from, to } = state?.selection.main

    // Get the line the cursor is currently on
    const fromLine = state?.doc.lineAt(from)
    const toLine = state?.doc.lineAt(to)

    return state?.doc.sliceString(fromLine.from, toLine.to)
  }

  useEventListener('keydown', kedDownHandler);

  const codeMirror = useRef();
  return (
    <div id="editor">
        <Menubar />
        <CodeMirror
          ref={codeMirror}
          value={templateCode}
          basicSetup={{
              foldGutter: false,
              dropCursor: false,
              lineNumbers: true,
          }}
          
          height="100%"
          theme="dark"
          extensions={[vim(), python({})]}
          onChange={onChange}
        />
        <Log />
    </div>
  );
}
export default App;


// Hook
function useEventListener(eventName, handler, element = window) {
  // Create a ref that stores handler
  const savedHandler = useRef();
  // Update ref.current value if handler changes.
  // This allows our effect below to always get latest handler ...
  // ... without us needing to pass it in effect deps array ...
  // ... and potentially cause effect to re-run every render.
  useEffect(() => {
    savedHandler.current = handler;
  }, [handler]);
  useEffect(
    () => {
      // Make sure element supports addEventListener
      // On
      const isSupported = element && element.addEventListener;
      if (!isSupported) return;
      // Create event listener that calls handler function stored in ref
      const eventListener = (event) => savedHandler.current(event);
      // Add event listener
      element.addEventListener(eventName, eventListener);
      // Remove event listener on cleanup
      return () => {
        element.removeEventListener(eventName, eventListener);
      };
    },
    [eventName, element] // Re-run if eventName or element changes
  );
}
