`Store
用来保存数据
整个应用只有一个store 用createStore函数来生成`
import { createStore } from 'redux';
const store = createStore(fn);//fn是一个reducer函数 见 Line 91

`State
一个state对应一个view 反之亦然
某个时间点对Store生成快照就是，此时时间点的数据集合就是state
当前时刻的 State，可以通过store.getState()拿到。
`

import { createStore } from 'redux';
const store = createStore(fn);

const state = store.getState();

`Action
View 发出 Action通知告知State要发生变化了
Action 是一个对象。其中的type属性是必须的，表示 Action 的名称。
`
const action = {
    type: 'ADD_TODO',
    payload: 'Learn Redux'
  };

//**********************
const ADD_TODO = '添加 TODO';

function addTodo(text) {
    return {
        type: ADD_TODO,
        text
    }
}

const action = addTodo('Learn Redux');
// * 部分被称为Action Creator
//**********************

`Dispatch
View 发出Action的唯一方法 store.dispatch() 接受一个action对象
`
import { createStore } from 'redux';
const store = createStore(fn);

store.dispatch({
  type: 'ADD_TODO',
  payload: 'Learn Redux'
});

store.dispatch(addTodo('Learn Redux'));// this looks better

`Reducer
Store 收到 Action 后必须给出一个新的 State，这样 View才会变化。
计算State 的过程叫做 Reducer
为啥叫 Reducer？ 如下:
const actions = [
    { type: 'ADD', payload: 0 },
    { type: 'ADD', payload: 1 },
    { type: 'ADD', payload: 2 }
  ];
  
  const total = actions.reduce(reducer, 0); // 3
`
const reducer = function (state, action) {
    // ...
    return new_state;
  };

const defaultState = 0;
const reducer = (state = defaultState, action) => {
    switch (action.type) {
        case 'ADD':
        return state + action.payload;
        default: 
        return state;
    }
};

const state = reducer(1, {
    type: 'ADD',
    payload: 2
});

`实际应用中，Reducer 函数不用像上面这样手动调用，store.dispatch方法会触发 Reducer 
的自动执行。为此，Store 需要知道 Reducer 函数，做法就是在生成 Store 的时候，将 Reducer 传入createStore方法。
`

import { createStore } from 'redux';
const store = createStore(reducer);
//reducer是个纯函数 所以不能更新 只能新建对象
//最好把 State 对象设成只读。你没法改变它，要得到新的 State，唯一办法就是生成一个新对象

`store.subscribe()
设置监听函数 一旦State发生变化 就会自动执行这个函数
`
import { createStore } from 'redux';
const store = createStore(reducer);

store.subscribe(listener);
`只要把 View 的更新函数（对于 React 项目，就是组件的render方法或setState方法）放入listen，
就会实现 View 的自动渲染。
store.subscibe返回一个函数， 调用这个函数可以解除监听`
let unsubscribe = store.subscribe(() =>
  console.log(store.getState())
);

unsubscribe();
