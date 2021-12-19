/* eslint-disable no-unused-vars */
import React from 'react';

export default function Input(props) {

    return (
        <div className=''>
            <input
                className='p-2 border-1 bg-gray-100 border-blue-200 text-black-500 text-center text-md'
                type={props.type}
                name={props.name}
                value={props.value}
                pattern={props.pattern}
                maxLength={props.maxLength}
                placeholder={props.placeholder}
                onChange={props.handleChange}
                required
            />
        </div>
    )
}
