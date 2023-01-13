import React from 'react';
import CodeMirror from '@uiw/react-codemirror';
import { python } from '@codemirror/lang-python';

function App() {
  const templateCode = `@swim
  def baba():
    D('bd')
    again(baba)`;
  const onChange = React.useCallback((value, viewUpdate) => {
    console.log('value:', value);
  }, []);
  return (
    <CodeMirror
      value={templateCode}
      height="auto"
      themes="dark"
      extensions={[python({})]}
      onChange={onChange}
    />
  );
}
export default App;
