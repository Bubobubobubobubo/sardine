import React from 'react';
import './Menubar.css';
import SearchBar from "material-ui-search-bar";

class Menubar extends React.Component {
  data = {}
  render() {
  return (
        <div className="menu">
        <h2>Sardine</h2>
        <SearchBar
          value={this.state.value}
          onChange={(newValue) => console.log(newValue)}
          onRequestSearch={() => console.log('Search')}
        />
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
