import React from 'react';
import './Menubar.css';
import { Button, IconBtn } from './buttons';

class Menubar extends React.Component {
  data = {}
  render() {
  return (
    <nav>
        <h2>Sardine</h2>
        <div className='btn-container'>
          <IconBtn icon="faPlay" onClick={() => console.log('Play')} />
          <IconBtn icon="faStop" onClick={() => console.log('Stop')} />
          <IconBtn icon="faFloppyDisk" onClick={() => console.log('Save')} />
          <IconBtn icon="faUserGroup" onClick={() => console.log('Share')} />
          <Button text="Mode" onClick={this.props.editingModeFunction} />   
          <a href="https://sardine.raphaelforment.fr" target="_blank">
            <Button text="Open Docs" />
          </a>

        </div>
    </nav>
    )
  }
}

export default Menubar;
