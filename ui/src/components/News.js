/* eslint-disable no-unused-vars */
/* eslint-disable react/jsx-no-target-blank */
/* eslint-disable react-hooks/exhaustive-deps */
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { FaInternetExplorer } from 'react-icons/fa';
import { BsPersonFill } from 'react-icons/bs';
import { GiNewspaper } from 'react-icons/gi';
import { AiOutlineNumber } from 'react-icons/ai';
import { IoTrailSignSharp } from 'react-icons/io5';
import Moment from 'react-moment';
import Select from './inputs/Select';
import Input from './inputs/Input';
import Pagination from './Pagination';
import loader from './media/loading.svg';
import store from '../redux/store';
import { useSelector } from 'react-redux';
import './Loader.css';

export default function News({baseUrl}) {
    const [loading, setLoading] = useState(false);
    
    const {getState, dispatch} = store;
    const state = getState();
    const { news, newsType, page, pageSize, totalPages, searchQuery, networkStatus } = useSelector(state => state);
    // console.log(state);

    const handleInputChange = (e) => {
        const target = e.target;
        const name = target.name;
        const value = target.value;
        setLoading(true);
        console.log(name, value);
        
        if(name === 'search-query') {
            dispatch({
                type: 'SET_SEARCH_QUERY',
                data: value
            }); 
        } else {
            dispatch({
                type: 'SET_NEWS_TYPE',
                data: value
            });
        }
        setLoading(false);
      }

      
    const handlePageClick = (direction) => {
        let nextPage = page;
        nextPage = direction === 'next' ? nextPage + 1 : nextPage - 1;
        console.log(direction);
        dispatch({
            type: 'SET_PAGE',
            data: nextPage
        });
    }

    const getNews = async() => {
        const res = await axios({
            method: 'GET',
            url: `${baseUrl}/get_news`,
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .catch(err => console.log(err.message));

        if(res?.data) {
            dispatch({
                type: 'SET_NETWORK_STATUS',
                data: true
            });
            dispatch({
                type: 'SET_NEWS',
                data: res.data.news
            });
        } else {
            dispatch({
                type: 'SET_NETWORK_STATUS',
                data: false
            });
        }
    }
    useEffect(() => {
        getNews();
        
        return () => {}
    }, []);

    return (
        <div className='md:w-1/2 justify-center m-auto'>
            {!networkStatus && <div style={{backgroundColor: 'white', fontWeight: 'bold'}} className='text-red-500 text-bold py-2 m-1 rounded'>Please check your network !</div>}
            <div style={{backgroundColor: 'white', fontWeight: 'bold'}} className='text-bold mx-1 rounded flex justify-evenly'>
                <Select 
                    name='news-type'
                    value={newsType}
                    options={['Filter By Type', 'job', 'story', 'comment', 'poll', 'pollopt']}
                    handleChange={handleInputChange}
                />
                <Input
                    type='text'
                    name='search-query'
                    value={searchQuery}
                    placeholder='Search By Text'
                    handleChange={handleInputChange}
                /> 
            </div>
            <div className='flex flex-col md:justify-around'>
                {!loading ?
                <>{news.slice((page - 1) * pageSize, (pageSize * page)).sort((a, b) => b.time - a.time)
                    .map((singleNews, idx) => {
                        return <SingleNews key={idx} singleNews={singleNews}  />
                    })}
                </>
                :
                <div className='loader-div'>
                    <div>
                        <img className='loader' src={loader} alt='loader' />
                    </div>
                </div>}
            </div>

            {news.length > 0 ?
            <Pagination
                totalPages={totalPages}
                page={page}
                handlePageClick={handlePageClick}
            />
            :
            <div>
                <div className='mt-2 border-2 border-green-200 rounded font-bold text-white'>No data</div>
                {(news.slice((page - 1) * pageSize, (pageSize * page)).length < 4) && 
                <div style={{height: '80vh'}} className='mt-2 text-white'></div>}
            </div>}
        </div>
    )
}


const SingleNews = ({singleNews }) => {
    const { id, title, type, time, url, kids, by } = singleNews;
    // console.log(new Date(time).toUTCString(), time, JSON.parse(kids))
    return (
    <div style={{backgroundColor: 'white'}} className='bg-blue-200 p-2 border-blue-200 border-2 rounded m-1 flex flex-col'>
        <p className='text-md text-left flex flex-col'>
            <span className='flex'>
                <span className='ml-2 mb-2'>
                    <Moment>{new Date(time * 1000)}</Moment>
                </span>
            </span>
            <span className='flex'><AiOutlineNumber size={22} /><span className='ml-2'>{id}</span> </span>
            {title && <span className='flex'><IoTrailSignSharp size={22} /><span className='ml-2'>{title}</span> </span>}
            <span className='flex'> <GiNewspaper size={22} /> <span className='ml-2'>{type}</span></span>
            {url && <span className='flex'> <FaInternetExplorer size={22} /> <span className='ml-2 text-blue-600 hover:text-purple-600'><a href={url} target='_blank'>{url}</a></span></span>}
            {/* {kids && <span className='flex'> Kids: <span className='ml-2'>{kids}</span></span>} */}
            <span className='flex'> <BsPersonFill size={22}/> <span className='ml-2'>{by ? by : 'unknown'}</span></span>
        </p>
        {/* <p className='mt-3 mb-2'> */}
            {/* <span className='bg-blue-600 p-2 text-white mr-2 rounded cursor-pointer hover:bg-blue-400 hover:text-black'>{'single' ? 'Go Back' : 'View More'}</span>
            <span className='bg-green-600 p-2 text-white rounded cursor-pointer hover:bg-green-400 hover:text-black'> View </span> */}
        {/* </p> */}
    </div>
    )
}
