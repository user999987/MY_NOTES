`middleware就是一个函数作用在  store.dispatch()前后`

let next = store.dispatch;
store.dispatch = function dispatchAndLog(action) {
  console.log('dispatching', action);
  next(action);
  console.log('next state', store.getState());
}

`中间件的使用`
const store = createStore(
    reducer,
    applyMiddleware(thunk, promise, logger)
  );
// middleware的使用是有序的，使用千前要查下文档，比如logger一定要放在最后

const store = createStore(
    reducer,
    initial_state,
    applyMiddleware(logger)
  );
// 如果接受初始状态参数 那么 applyMiddleware 要放在第三个参数位置

`applyMiddleware 是 Redux 原生 方法`
export default function applyMiddleware(...middlewares) {
    return (createStore) => (reducer, preloadedState, enhancer) => {
      var store = createStore(reducer, preloadedState, enhancer);
      var dispatch = store.dispatch;
      var chain = [];
  
      var middlewareAPI = {
        getState: store.getState,
        dispatch: (action) => dispatch(action)
      };
      chain = middlewares.map(middleware => middleware(middlewareAPI));
      dispatch = compose(...chain)(store.dispatch);
  
      return {...store, dispatch}
    }
  }
