import React from 'react';

export default function Pagination(props) {
    const { page, totalPages, handlePageClick } = props;
    return (
        <div className='flex text-center justify-center'>
            <div className='mt-2 border-2 border-green-200 rounded font-bold text-white'>
                <button
                    className='bg-green-600 p-1 rounded font-bold'
                    onClick={() => handlePageClick('prev')}
                    disabled={page <= 1}
                    >
                    prev
                </button>
                <span className='px-3 text-white font-bold'>
                    page {page} of {totalPages}
                </span>
                <button
                    className='bg-green-600 p-1 rounded font-bold'
                    onClick={() => handlePageClick('next')}
                    disabled={page >= totalPages}
                    >
                    next
                </button>
            </div>
        </div>
    )
}