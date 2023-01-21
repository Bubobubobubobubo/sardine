import React from "react";

const Console = ({ logs }) => {


    return (
        <div className="console">
        <div className="console-header">
            <h3>Console</h3>
        </div>
        <div className="console-content">
            <ul>
                {logs.map((log) => {
                    return <li>{log}</li>
                })}
            </ul>
        </div>
        </div>
    );
};

export default Console;