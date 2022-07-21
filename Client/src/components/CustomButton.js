import React from 'react';

const CustomButton = ({text, onSubmit}) => {
    return (
        <button type="submit" className="msger-send-btn" onClick={onSubmit}>{text}</button>
    )
}

export default CustomButton;