import actions from "./actions";
import data from '../components/sampleData.json';

export default function reducer(state= initialState, action) {
    switch(action.type) {
        case actions.setNews.type:
            console.log('Setting News data');
            console.log('Sorting out comments');
            const sortedNews = action.data.filter(item => item.type !== 'comment');

            return {
              ...state,
              news: sortedNews, newsData: sortedNews, newsType: 'Filter By Type', page: 1, totalPages: Math.ceil(sortedNews.length / state.pageSize)
            }          
        case actions.setNewsType.type:
            console.log('Setting News Type');
            const newsByType = state.newsData.filter(type => (type.type === action.data));

            return {
              ...state,
              newsType: action.data, news: newsByType, searchQuery: '', page: 1, totalPages: Math.ceil(newsByType.length / state.pageSize)
            }          
            case actions.setPage.type:
                console.log('Setting page');
            return {
                ...state,
                page: action.data
            }                   
            case actions.setTotalPages.type:
            console.log('Setting totalPages');
            return {
                ...state,
                totalPages: action.data
            }                   
            case actions.setSearchQuery.type:
                console.log('Setting Search Query');
                let newsBySearch;
                if(state.newsType === 'Filter By Type') {
                    if(action.data === '') {
                        newsBySearch = state.newsData;
                    } else {
                        newsBySearch = state.newsData.filter(item => {
                            return item?.text?.toLowerCase().indexOf(action.data.toLowerCase()) >= 0;
                        });
                    }
                } else {
                    newsBySearch = state.newsData.filter(item => (item?.text?.toLowerCase().indexOf(action.data.toLowerCase()) >= 0) && (item.type === state.newsType));
                }
                    
                return {
                    ...state,
                    searchQuery: action.data, news: newsBySearch, page: 1, totalPages: Math.ceil(newsBySearch.length / state.pageSize)
                }                   
            case actions.setNetworkStatus.type:
                console.log('Setting Network Status');
                
            return {
                ...state,
                networkStatus: action.data
            }                   
            default:
                return state;
    }
};
 
export const initialState = {
    newsData: [],
    news: [],
    newsType: 'Filter By Type',
    page: 1,
    pageSize: 10,
    totalPages: Math.ceil([...data].length / 10),
    searchQuery: '',
    networkStatus: true
};
