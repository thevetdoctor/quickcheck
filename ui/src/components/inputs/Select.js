/* eslint-disable no-unused-vars */
import React from 'react';

export default function Select(props) {
    // const [{ stateData }, dispatch] = useCozaState();

    // const handleInputChange = (e) => {
    //     const target = e.target;
    //     const name = target.name;
    //     const value = target.value;
    
    //     console.log(name, value);
     
    //   } 

    return (
        <div className=''>
            <select 
                name={props.name}
                value={props.value}
                onChange={props.handleChange}
                className='p-2 border-1 bg-gray-100 border-blue-200'
            >
                {props.options?.map((item, idx) => (
                    <option key={idx} value={item}>{item}</option> 
                ))}
            </select>
        </div>
    )
}
