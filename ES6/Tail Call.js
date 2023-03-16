`Tail call 尾调
函数的最后一步是函数调用`
function f(x){
  return g(x);
}

`
ES6 的尾调用优化只在严格模式下开启，正常模式是无效的。`

// 情况一
function f(x){
    let y = g(x);
    return y;
  }
// 情况二
function f(x){
return g(x) + 1;
}
// 情况三
function f(x){
g(x);
}
`上面代码中，情况一是调用函数g之后，还有赋值操作
所以不属于尾调用，即使语义完全一样。情况二也属于调用后还有操作，即使写在一行内。情况三等同于下面的代码。`
// 情况三 =  below
function f(x){
    g(x);
    return undefined;
  }

`重点 重点 重点 

尾调用之所以与其他调用不同，就在于它的特殊的调用位置。

我们知道，函数调用会在内存形成一个“调用记录”，又称“调用帧”（call frame），保存调用位置和内部变量等信息。
如果在函数A的内部调用函数B，那么在A的调用帧上方，还会形成一个B的调用帧。等到B运行结束，将结果返回到A，B的调用帧才会消失。
如果函数B内部还调用函数C，那就还有一个C的调用帧，以此类推。所有的调用帧，就形成一个“调用栈”（call stack）。

尾调用由于是函数的最后一步操作，所以不需要保留外层函数的调用帧，因为调用位置、内部变量等信息都不会再用到了，
只要直接用内层函数的调用帧，取代外层函数的调用帧就可以了。`

function f() {
    let m = 1;
    let n = 2;
    return g(m + n);
  }
  f();
  
  // 等同于
  function f() {
    return g(3);
  }
  f();
  
  // 等同于
  g(3);
`
上面代码中，如果函数g不是尾调用，函数f就需要保存内部变量m和n的值、g的调用位置等信息。但由于调用g之后，
函数f就结束了，所以执行到最后一步，完全可以删除f(x)的调用帧，只保留g(3)的调用帧。

这就叫做“尾调用优化”（Tail call optimization），即只保留内层函数的调用帧。如果所有函数都是尾调用，
那么完全可以做到每次执行时，调用帧只有一项，这将大大节省内存。这就是“尾调用优化”的意义。

注意，只有不再用到外层函数的内部变量，内层函数的调用帧才会取代外层函数的调用帧，否则就无法进行“尾调用优化”。
`  
function addOne(a){
    var one = 1;
    function inner(b){
      return b + one;
    }
    return inner(a);
  }
`
上面的函数不会进行尾调用优化，因为内层函数inner用到了外层函数addOne的内部变量one。

注意，目前只有 Safari 浏览器支持尾调用优化，Chrome 和 Firefox 都不支持。
`


`递归非常耗费内存，因为需要同时保存成千上百个调用帧，很容易发生“栈溢出”错误（stack overflow）。
但对于尾递归来说，由于只存在一个调用帧，所以永远不会发生“栈溢出”错误。`
function factorial(n) {
    if (n === 1) return 1;
    return n * factorial(n - 1);
  }
  
  factorial(5) // 120
// 上面代码是一个阶乘函数，计算n的阶乘，最多需要保存n个调用记录，复杂度 O(n) 
// 如果改写成尾递归，只保留一个调用记录，复杂度 O(1) 
function factorial(n, total) {
    if (n === 1) return total;
    return factorial(n - 1, n * total);
  }
  
  factorial(5, 1) // 120

`一般性递归 Fibonacci`
function Fibonacci (n) {
    if ( n <= 1 ) {return 1};
  
    return Fibonacci(n - 1) + Fibonacci(n - 2);
  }
  
  Fibonacci(10) // 89
  Fibonacci(100) // 超时
  Fibonacci(500) // 超时
`尾递归优化过的 Fibonacci`
  function Fibonacci2 (n , ac1 = 1 , ac2 = 1) {
    if( n <= 1 ) {return ac2};
  
    return Fibonacci2 (n - 1, ac2, ac1 + ac2);
  }
  
  Fibonacci2(100) // 573147844013817200000
  Fibonacci2(1000) // 7.0330367711422765e+208
  Fibonacci2(10000) // Infinity

`纯粹的函数式编程语言没有循环操作命令，所有的循环都用递归实现，这就是为什么尾递归对这些语言极其重要。
对于其他支持“尾调用优化”的语言（比如 Lua，ES6），只需要知道循环可以用递归代替，而一旦使用递归，就最好使用尾递归。`