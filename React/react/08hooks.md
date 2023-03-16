## Hooks at Glance
Hooks are a enw addition in React 16.8. They let you use state and other React features without writing a class. Hook 是一些可以让你在函数组件里“钩入” React state 及生命周期等特性的函数。Hook 不能在 class 组件中使用 —— 这使得你不使用 class 也能使用 React

## Declaring multiple state variables
```typescript
function ExampleWithManyStates() {
  // Declare multiple state variables!
  const [age, setAge] = useState(42);
  const [fruit, setFruit] = useState('banana');
  const [todos, setTodos] = useState([{ text: 'Learn Hooks' }]);
  // ...
}
```

## Update State
```typescript
<button onClick={()=> this.setState({ count: this.state.count + 1 })}>
  click me
</button>

<button onClick={()=> setCount(count+1)}>
  click me
</button>
```

## Effect Hook
`useEffect` 就是一个 Effect Hook，给函数组件增加了操作副作用的能力。它跟 class 组件中的 `componentDidMount`、`componentDidUpdate` 和 `componentWillUnmount` 具有相同的用途，只不过被合并成了一个 API

在 React 组件中有两种常见副作用操作：需要清除的和不需要清除的。有时候，我们只想在 React 更新 DOM 之后运行一些额外的代码。比如发送网络请求，手动变更 DOM，记录日志，这些都是常见的无需清除的操作。
```typescript
import React, { useState, useEffect } from 'react';

function FriendStatus(props){

    const [isOnline, setIsOnline] = useState(null);

    function handleStatusChange(status){
        setIsOnline(status.isOnline);
    }
    // 跟 useState 一样，你可以在组件中多次使用 useEffect
    useEffect(() => {
        document.title = `You clicked ${count} times`;
    });
    useEffect(() => {
        ChatAPI.subscribeToFriendStatus(props.friend.id, handleStatusChange);
        return () => {
            ChatAPI.unsubscribeFromFriendStatus(props.friend.id, handleStatus);
        }
    });

    if (isOnline === null) {
        return 'Loading...';
    }
    return isOnline ? 'Online' : 'Offline';
}
```
When you call useEffect, you’re telling React to run your “effect” function after flushing changes to the DOM. Effects are declared inside the component so they have access to its props and state. By default, React runs the effects after every render — including the first render.<br>
副作用函数还可以通过返回一个函数来指定如何“清除”副作用。例如，在下面的组件中使用副作用函数来订阅好友的在线状态，并通过取消订阅来进行清除操作<br>
在上面的示例中，React 会在组件销毁时取消对 ChatAPI 的订阅，然后在后续渲染时重新执行副作用函数。跟 useState 一样，你可以在组件中多次使用 useEffect

那么 React 怎么知道哪个 state 对应哪个 useState？答案是 React 靠的是 Hook 调用的顺序。因为我们的示例中，Hook 的调用顺序在每次渲染中都是相同的，所以它能够正常工作
```typescript
// ------------
// 首次渲染
// ------------
useState('Mary')           // 1. 使用 'Mary' 初始化变量名为 name 的 state
useEffect(persistForm)     // 2. 添加 effect 以保存 form 操作
useState('Poppins')        // 3. 使用 'Poppins' 初始化变量名为 surname 的 state
useEffect(updateTitle)     // 4. 添加 effect 以更新标题

// -------------
// 二次渲染
// -------------
useState('Mary')           // 1. 读取变量名为 name 的 state（参数被忽略）
useEffect(persistForm)     // 2. 替换保存 form 的 effect
useState('Poppins')        // 3. 读取变量名为 surname 的 state（参数被忽略）
useEffect(updateTitle)     // 4. 替换更新标题的 effect
```
只要 Hook 的调用顺序在多次渲染之间保持一致，React 就能正确地将内部 state 和对应的 Hook 进行关联
<br>如果我们想要有条件地执行一个 effect，可以将判断放到 Hook 的内部：
```typescript
useEffect( function persistFrom(){
    if (name!==''){
        localStorage.setItem('formData', name);
    }
});
```

## Rules of Hook
Hooks are JavaScript functions, but they impose two additional rules:
* 只能在函数最外层调用 Hook。不要在循环、条件判断或者子函数中调用。
* 只能在 React 的函数组件中调用 Hook。不要在其他 JavaScript 函数中调用。（还有一个地方可以调用 Hook —— 就是自定义的 Hook 中，我们稍后会学习到。）

## Building Your Own Hooks
前面，我们介绍了一个叫 FriendStatus 的组件，它通过调用 useState 和 useEffect 的 Hook 来订阅一个好友的在线状态。假设我们想在另一个组件里重用这个订阅逻辑。<br>
我们把这个逻辑抽取到一个叫做 useFriendStatus 的自定义 Hook 里
```typescript
import React, { useState, useEffect } from 'react'

function useFriendStatus(friendID){

    const [isOnline, setIsOnline] = useState(null);

    function handleStatusChange(status){
        setIsOnline(status.isOnlie);
    }

    useEffect(() => {
        ChatAPI.subscribeToFriendStatus(friendID, handleStatusChange);
        return () => {
            ChatAPI.unscribeFromFriendStatus(friendID, handleStatusChange);
        };
    });

    return isOnline;
}
```
将 friendID 作为参数 并返回好友是否在线<br>
现在在两个组件中使用它:
```typescript
function FriendStatus(props){
    const isOnline = useFriendStatus(props.friend.id);

    if (isOnline === null){
        return 'Loading...';
    }
    return isOnline ? 'Online' : 'Offline';
}

function FriendListItem(props){
    const isOnline = useFriendStatus(props.friend.id);
    return (
        <li style={{color: isOnline ? 'green' : 'balck'}}>
            {props.friend.name}
        </li>
    )
}
```
每个组件间的 state 是完全独立的。Hook 是一种复用状态逻辑的方式，它不复用 state 本身。事实上 Hook 的每次调用都有一个完全独立的 state —— 因此你可以在单个组件中多次调用同一个自定义 Hook。

自定义 Hook 更像是一种约定而不是功能。如果函数的名字以 “use” 开头并调用其他 Hook，我们就说这是一个自定义 Hook。 useSomething 的命名约定可以让我们的 linter 插件在使用 Hook 的代码中找到 bug。
