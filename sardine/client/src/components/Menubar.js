import React from 'react';
import './Menubar.css';

class Menubar extends React.Component {
  data = {}
  render() {
  return (
        <div className="menu">
        <h2>Sardine</h2>
        <div id="button-zone">
          <button
          onClick={this.props.editingModeFunction}
          >{this.props.editingMode} Mode</button>
          <form 
          action="https://sardine.raphaelforment.fr"
          target="_blank">
            <button>Open Docs</button>
          </form>
        </div>
        </div>
    )
  }
}

export default Menubar;
