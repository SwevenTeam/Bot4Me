import React from 'react';

const CustomButton = ({text,isDisabled,onSubmit,className,hidden}) => {
    return (
        <button hidden={hidden} type="submit" disabled = {isDisabled} className={className} onClick={onSubmit}>{text}</button>
    )
}

export default CustomButton;