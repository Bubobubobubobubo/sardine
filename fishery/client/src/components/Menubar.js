import React from 'react';
import './Menubar.css';
import { Button, IconBtn } from './buttons';
import Logo from "../static/sardine_logo_single.png"

class Menubar extends React.Component {
  data = {}
  render() {
  return (
    <nav>
        <img className='logo' src={Logo} alt="Sardine Logo" />
        <div className='btn-container'>
          <IconBtn icon="faPlay" onClick={() => console.log('Play')} />
          <IconBtn icon="faStop" onClick={() => console.log('Stop')} />
          <IconBtn icon="faFloppyDisk" onClick={() => console.log('Save')} />
          <IconBtn icon="faUserGroup" onClick={() => console.log('Share')} />
          <Button text={this.props.editingMode + "Mode"} onClick={this.props.editingModeFunction} />   
          <a href="https://sardine.raphaelforment.fr" target="_blank">
            <Button text="Open Docs" />
          </a>
        </div>
    </nav>
    )
  }
}

export default Menubar;
