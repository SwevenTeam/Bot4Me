import React from 'react';
import CustomIcon from './CustomIcon'




const CustomButton = ({text,isDisabled,onSubmit,className,hidden,icon}) => {
    
    if(!icon){
        icon="Send"
    }
    const ButtonIcon = CustomIcon[icon]
    return (
       <button hidden={hidden} type="submit" disabled = {isDisabled} className={className} onClick={onSubmit}>
            <span hidden={true}>{text}</span>
            <ButtonIcon/>
        </button>
    )
}

export default CustomButton;