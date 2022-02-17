/* eslint-disable no-unused-vars */
/* eslint-disable react/jsx-no-target-blank */
/* eslint-disable react-hooks/exhaustive-deps */
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { FaInternetExplorer, FaUserAlt, FaEdit} from 'react-icons/fa';
import { BsPersonFill } from 'react-icons/bs';
import { GiNewspaper } from 'react-icons/gi';
import { AiOutlineNumber, AiFillDelete} from 'react-icons/ai';
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
    const [error, setError] = useState('');
    const [formActive, setFormActive] = useState(false);
    const [status, setStatus] = useState(false);
    const [title, setTitle] = useState('');
    const [story, setStory] = useState('');
    const [url, setUrl] = useState('');
    const [author, setAuthor] = useState('');
    const [sync, setSync] = useState(false);

    const {getState, dispatch} = store;
    const state = getState();
    const { news, newsType, page, pageSize, totalPages, searchQuery, networkStatus } = useSelector(state => state);
    // console.log(state);

    const handleChange = (e) => {
        console.log(e.target.name);
        if(e.target.name === 'title') {
            setTitle(e.target.value);
        } else if(e.target.name === 'newStory') {
            setStory(e.target.value);
        } else if(e.target.name === 'url') {
            setUrl(e.target.value);
        } else {
            setAuthor(e.target.value);
        }
        setError('');
        setStatus(false);
    }

    const handleFormActive = () => {
        setFormActive(!formActive);
        setError('');
        setStatus(false);
    }

    const postStory = async() => {
        if(!story) {
            setError('Please enter some text!');
            return;
        }
        setLoading(true);
        console.log(story);
        const res = await axios({
            method: 'POST',
            url: `${baseUrl}/api/news`,
            data: { title, text: story, url, by: author, type: 'story' },
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .catch(err => console.log(err.message));

        if(res?.data) {
            setStatus(false);
            setFormActive(false);
            setTitle('');
            setStory('');
            setUrl('');
            setAuthor('');
        } else {
            setStatus(true);
        }
        setSync(!sync);
        setLoading(false);
    }

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

    const apiCallHook = async(method, url, data) => {
        setLoading(true);
        const res = await axios({
            method,
            url,
            data,
            headers: {
                'Content-Type': 'application/json',
            }
            })
            .catch(error => {
                if(error.isAxiosError) {
                    console.log(error.message);
                }
            });
            setLoading(false);
            setSync(!sync);
    }

    useEffect(() => {
        getNews();
        
        return () => {}
    }, [sync]);

    return (
        <div className='md:w-1/2 justify-center m-auto w-full'>
            {formActive && <p className='bg-gray-200 p-3'>
                <input 
                    type='text'
                    name='title'
                    value={title}
                    placeholder='Story title'
                    style={{width: '15em'}}
                    onChange={handleChange}
                />
                <textarea 
                    type='textarea'
                    name='newStory'
                    placeholder={!error ? 'Write a new story' : error}
                    className={error ? 'text-red-800 placeholder-red-600 font-bold border-red-700 border-3 p-2 mb-2 rounded' : 'border-blue-200 border-2 p-2 mb-2 rounded font-bold'}
                    style={{width: '15em'}}
                    cols={3}
                    rows={4}
                    maxLength={160}
                    value={story}
                    onChange={handleChange}
                    required={true}
                />
                <input
                    type='text'
                    name='url'
                    value={url}
                    placeholder='Url link'
                    style={{width: '15em', paddingLeft: '0.5em', marginBottom: '0.5em'}}
                    onChange={handleChange}
                /><br />
                <input
                    type='text'
                    name='author'
                    value={author}
                    placeholder='Author'
                    style={{width: '15em', paddingLeft: '0.5em'}}
                    onChange={handleChange}
                />
                <br /><br />
                <span 
                    className='cursor-pointer bg-gray-500 p-2 m-2 text-white rounded hover:bg-gray-400' onClick={handleFormActive}
                > 
                    Cancel 
                </span>
                <span 
                    className={story ? 'cursor-pointer bg-green-600 p-2 mb-2 text-white rounded hover:bg-green-400 hover:text-black' : 'bg-gray-600 p-2 mb-2 text-white rounded'} onClick={postStory}
                > 
                    Post a story 
                </span>
            </p>}
            {!formActive && <div style={{backgroundColor: 'white', fontWeight: 'bold'}} className='text-blue-500 text-bold py-2 m-1 rounded hover:bg-blue-200 hover:cursor-pointer' onClick={handleFormActive}>Post Story</div>}

            {!networkStatus && <div style={{backgroundColor: 'white', fontWeight: 'bold'}} className='text-red-500 text-bold py-2 m-1 rounded'>Please check your network !</div>}
            <div style={{backgroundColor: 'white', fontWeight: 'bold'}} className='text-bold mx-1 rounded flex justify-evenly'>
                <Select 
                    name='news-type'
                    value={newsType}
                    options={['Filter By Type', 'job', 'story', 'poll', 'pollopt']}
                    handleChange={handleInputChange}
                />
                <Input
                    type='text'
                    name='search-query'
                    value={searchQuery}
                    placeholder='Search By Text'
                    handleChange={handleInputChange}
                    className='outline-none'
                /> 
            </div>
            <div className='flex flex-col md:justify-around'>
                {!loading ?
                <>{news.filter(item => item.id !== 123).sort((a, b) => - a.time + b.time).slice((page - 1) * pageSize, (pageSize * page))
                    .map((singleNews, idx) => {
                        return <SingleNews key={idx} singleNews={singleNews} baseUrl={baseUrl} apiCallHook={apiCallHook} />
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


const SingleNews = ({singleNews, baseUrl, apiCallHook }) => {
    const { id, title, type, text, time, url, by, source } = singleNews;
    const [storyText, setStoryText] = useState(text);
    const [editForm, setEditForm] = useState(false);

    const handleStoryChange = (e) => {
        setStoryText(e.target.value);
    }

    const editStory = () => {
        setEditForm(!editForm);
    }
   
    const updateStory = () => {
        apiCallHook('PUT', `${baseUrl}/api/news/${id}`, {text: storyText});
        setStoryText('');
        setTimeout(() => {
            setEditForm(false);
        }, 300);
    }

    const deleteStory = () => {
        apiCallHook('DELETE', `${baseUrl}/api/news/${id}`);
    }
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
            {text && <span className='flex overflow-auto'> <GiNewspaper size={22} /> <span className='ml-2'>{text}</span></span>}
            {url && <span className='flex'> <FaInternetExplorer size={22} /> <span className='ml-2 text-blue-600 hover:text-purple-600 overflow-auto'><a href={url} target='_blank'>{url}</a></span></span>}
            <span className='flex'> <BsPersonFill size={22}/> <span className='ml-2'>{by ? by : 'unknown'}</span></span>
        </p>

        { source !== 'hackernews' && 
        <>
        <p className=' text-left flex flex-col'>
            {editForm && <span>
                <textarea 
                    className='border-red-700 border-3 p-2 mb-2 rounded bg-gray-300 outline-none'
                    style={{width: '100%'}}
                    cols={3}
                    rows={4}
                    maxLength={160}
                    value={storyText}
                    onChange={handleStoryChange}
                    required={true}
                /><br />
                 <span 
                    className='cursor-pointer bg-gray-500 p-2 m-2 text-white rounded hover:bg-gray-400' onClick={() => editStory()}
                > 
                    Cancel 
                </span>
                <span 
                    className='cursor-pointer bg-green-600 p-2 mb-2 text-white rounded hover:bg-green-400 hover:text-black' onClick={() => updateStory()}
                > 
                    Update Story 
                </span>
                </span>}
        </p>

        {!editForm && 
            <p className='my-2 flex justify-center'>
                <span className='cursor-pointer mr-3' onClick={() => editStory()}> 
                    <FaEdit size={23} />
                </span>
                <span className='cursor-pointer' onClick={() => deleteStory()}> 
                    <AiFillDelete size={23} color='red'/>
                </span>
            </p>}
        </>}
    </div>
    )
}
