import React, { useState } from 'react';
import './Log.css'
import Console from './console/Console';

const logExample = [
  "[19:33] ERROR: ... blabla",
  "[19:33] ERROR: ... blabla",
  "[19:33] ERROR: ... blabla",
  "[19:33] ERROR: ... blabla",
]



class Log extends React.Component {
  
  render() {
      
    let logs = this.props.logs;
    
    return (
        <div id="log">
        <textarea 
            id="logwindow" 
        >
        Welcome to Sardine REPL: the embedded code editor for Sardine! Press Shift+Enter to eval selection.
        </textarea>
        <Console logs={logs} />
        </div>
    )
  }
}

export default Log;
