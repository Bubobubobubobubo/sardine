import React from 'react';
import './Log.css'

class Log extends React.Component {
  render() {
    return (
        <div id="log">
        <textarea 
            id="logwindow" 
        >
        Welcome to Sardine REPL: the embedded code editor for Sardine! Press Shift+Enter to eval selection.
        </textarea>
        </div>
    )
  }
}

export default Log;
