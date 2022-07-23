import React from 'react';

const CustomButton = ({text, isDisabled,onSubmit}) => {
    return (
        <button type="submit" disabled = {isDisabled} className="msger-send-btn" onClick={onSubmit}>{text}</button>
    )
}

export default CustomButton;