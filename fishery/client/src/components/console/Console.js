import React from "react";

const Console = ({ logs }) => {

    // append logs to html var 
    let htmlLogs = "";

    for (let i = 0; i < logs.length; i++) {
        htmlLogs += "<li>" + logs[i] + "</li>";
    }

    console.log(htmlLogs);


    return (
        <div className="console">
        <div className="console-header">
            <h3>Console</h3>
        </div>
        <div className="console-content">
            <ul>
                {htmlLogs}
            </ul>
        </div>
        </div>
    );
};

export default Console;