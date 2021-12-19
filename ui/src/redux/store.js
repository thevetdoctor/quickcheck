import { createStore } from 'redux';
import { devToolsEnhancer } from 'redux-devtools-extension';
import reducer from './reducer';

const store = createStore(reducer, devToolsEnhancer());

export default store;