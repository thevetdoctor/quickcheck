/* eslint-disable no-unused-vars */
/* eslint-disable react-hooks/exhaustive-deps */
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { FaInternetExplorer, FaUserAlt, FaUserSecret } from 'react-icons/fa';
import { HiSpeakerphone } from 'react-icons/hi';
import data from './sampleData.json';
import Select from './inputs/Select';
import Input from './inputs/Input';

export default function News({baseUrl}) {
    const [status, setStatus] = useState(true);
    const [news, setNews] = useState([...data]);
    const [newsType, setNewsType] = useState('');
    const [searchQuery, setSearchQuery] = useState('');
    
    const handleInputChange = (e) => {
        const target = e.target;
        const name = target.name;
        const value = target.value;
    
        console.log(name, value);
        if(name === 'search-query') {
            setSearchQuery(value)
        } else {
            setNewsType(value);
        }
      }

    console.log(news);
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
            setStatus(false);
            setNews(res.data.news);
        } else {
            // setNews(data);
            setStatus(true);
        }
    }

    useEffect(() => {
        // getNews();
        
        return () => {}
    }, []);

    return (
        <div>
            {status && <div style={{backgroundColor: 'white', fontWeight: 'bold'}} className='text-red-500 text-bold py-2 m-2 rounded'>Please check your network !</div>}
            {status && <div style={{backgroundColor: 'white', fontWeight: 'bold'}} className='text-bold mx-2 rounded flex justify-between'>
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
            </div>}
            {'!single' &&
            <>{news?.filter(type => type.type === newsType).map((singleNews, idx) => {
                return <SingleNews key={idx} singleNews={singleNews}  />
            })}
            </>} 
        </div>
    )
}


const SingleNews = ({singleNews }) => {
    const { id, title, type, time, url, kids, by } = singleNews;
    return (
    <div style={{backgroundColor: 'white'}} className='bg-blue-200 p-2 border-blue-200 border-2 rounded m-1 flex flex-col'>
        {'!single' &&
        <p className=' text-left flex flex-col'>
            <span className='flex'><FaUserSecret /><span className='ml-2'>{id}</span> </span>
            <span className='flex'><FaUserSecret /><span className='ml-2'>{title}</span> </span>
            <span className='flex'> <FaUserAlt /> <span className='ml-2'>{type}</span></span>
            <span className='flex'> <FaInternetExplorer /> <span className='ml-2'>{time}</span></span>
            <span className='flex'> <HiSpeakerphone /> <span className='ml-2'>{url}</span></span>
            <span className='flex'> Albums: <span className='ml-2'>{kids}</span></span>
            <span className='flex'> Albums: <span className='ml-2'>{by}</span></span>
        </p>}
        <p className='mt-3 mb-2'>
            <span className='bg-blue-600 p-2 text-white mr-2 rounded cursor-pointer hover:bg-blue-400 hover:text-black'>{'single' ? 'Go Back' : 'View More'}</span>
            <span className='bg-green-600 p-2 text-white rounded cursor-pointer hover:bg-green-400 hover:text-black'> View </span>
        </p>
    </div>
    )
}
