import { createStore } from 'redux';
let { subsribe, dispatch, getState } = createStore(reducer);
`createStore可以接受第二个参数，表示State的最初状态。这个状态通常是服务器给的
window.STATE_FROM_SERVER就是整个应用的状态初始值。注意，如果提供了这个参数，它会覆盖 Reducer 函数的默认初始值。
`
let store = createStore(todoApp, window.STATE_FROM_SERVER)
`
下面是createStore方法的一个简单实现，可以了解一下 Store 是怎么生成的:
`
const createStore = (reducer) => {
    let state;
    let listeners = [];
  
    const getState = () => state;
  
    const dispatch = (action) => {
      state = reducer(state, action);
      listeners.forEach(listener => listener());
    };
  
    const subscribe = (listener) => {
      listeners.push(listener);
      return () => {
        listeners = listeners.filter(l => l !== listener);
      }
    };
  
    dispatch({});
  
    return { getState, dispatch, subscribe };
  };

`整个应用只有一个 State 对象，大型应用的 State 必然很大。Reducer要负责生成 State，势必会变得臃肿，此时需要拆分。
原函数如下`

const chatReducer = (state = defaultState, action = {}) => {
  const { type, payload } = action;
  switch (type) {
    case ADD_CHAT:
      return Object.assign({}, state, {
        chatLog: state.chatLog.concat(payload) // 改变 chatLog属性
      });
    case CHANGE_STATUS:
      return Object.assign({}, state, {
        statusMessage: payload //改变 statusMessage属性
      });
    case CHANGE_USERNAME:
      return Object.assign({}, state, {
        userName: payload //改变 userName属性
      });
    default: return state;
  }
};


const chatReducer = (state = defaultState, action = {}) => {
  return {
    chatLog: chatLog(state.chatLog, action),
    statusMessage: statusMessage(state.statusMessage, action),
    userName: userName(state.userName, action)
  }
};
`拆分之后锁上所示， 另外redux提供了一个 combineReducers 函数用于 Reducer 拆分`
const reducer = combineReducers({
  a: doSomethingWithA,
  b: processB,
  c: c
})
// combineReducers 如果State 的属性名与子 Reducer 同名 则可以 省略 key
// 等同于
function reducer(state = {}, action) {
  return {
    a: doSomethingWithA(state.a, action),
    b: processB(state.b, action),
    c: c(state.c, action)
  }
}

`可以把所有子 Reducer 放在一个文件里面，然后统一引入。`

import { combineReducers } from 'redux'
import * as reducers from './reducers'

const reducer = combineReducers(reducers)