import React from 'react';
import CodeMirror from '@uiw/react-codemirror';
import { python } from '@codemirror/lang-python';
import { vim } from "@replit/codemirror-vim";
import Menubar from './components/Menubar.js';
import Log from './components/Log.js';

function App() {
  const templateCode = `@swim
def baba():
    D('bd')
    again(baba)`;
  const onChange = React.useCallback((value, viewUpdate) => {
    console.log('value:', value);
  }, []);
  return (
    <div id="editor">
        <Menubar />
        <CodeMirror
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
