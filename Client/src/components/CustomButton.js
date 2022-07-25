import React from 'react';

const CustomButton = ({text,isDisabled,onSubmit,className}) => {
    return (
        <button type="submit" disabled = {isDisabled} className={className} onClick={onSubmit}>{text}</button>
    )
}

export default CustomButton;