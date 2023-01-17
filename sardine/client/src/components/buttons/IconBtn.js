import React from "react";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faPlay, faStop, faFloppyDisk, faUserGroup  } from '@fortawesome/free-solid-svg-icons'

// Select the icon to display
function selectIcon(icon) {
    switch (icon) {
        case 'faPlay':
            return faPlay;
        case 'faStop':
            return faStop;
        case 'faFloppyDisk':
            return faFloppyDisk;
        case 'faUserGroup':
            return faUserGroup;
        default:
            return faPlay;
    }
}

// Icon button component
const IconBtn = ({ icon, onClick }) => {
    return (
        <button className="icon-btn" onClick={onClick}>
            <FontAwesomeIcon icon={selectIcon(icon)} />
        </button>
    );
};

export default IconBtn;