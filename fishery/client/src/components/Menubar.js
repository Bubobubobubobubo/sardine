import React from 'react';
import './Menubar.css';
import logo from './sardine_logo.svg';

class Menubar extends React.Component {
  render() {
    return (
        <div className="menu">
        <img src={logo} alt="Logo" width="50px" height="50px"/>
        <h3>Sardine</h3>
        <button type="button">Click Me!</button>
        </div>
    )
  }
}

export default Menubar;
