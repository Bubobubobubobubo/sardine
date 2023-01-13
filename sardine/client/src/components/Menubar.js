import React from 'react';
import logo from './sardine_logo.svg';
import './Menubar.css';

class Menubar extends React.Component {
  render() {
    return (
        <div className="menu">
        <h2>SARDINE</h2>
        <button>Click Me!</button>
        </div>
    )
  }
}

export default Menubar;
