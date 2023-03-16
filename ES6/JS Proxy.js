`Proxy 类似Python中的一些魔术方法 可以对对象的一些行为重定义
ES6 原生提供 Proxy 构造函数，用来生成 Proxy 实例。`

//var proxy = new Proxy(target, handler);

var person = {
    name: "张三"
  };
  
var personProxy = new Proxy(person, {
    get: function(target, propKey) {
        if (propKey in target) {
        return target[propKey];
        } else {
        throw new ReferenceError("Prop name \"" + propKey + "\" does not exist.");
        }
    }
});
  
  personProxy.name // "张三"
  personProxy.age // 抛出一个错误

  `利用 Proxy，可以将读取属性的操作（get），转变为执行某个函数，从而实现属性的链式操作。`

  var pipe = (function () {
    return function (value) {
      var funcStack = [];
      var oproxy = new Proxy({} , {
        get : function (pipeObject, fnName) {
          if (fnName === 'get') {
            return funcStack.reduce(function (val, fn) {
              return fn(val);
            },value);
          }
          funcStack.push(window[fnName]);
          return oproxy;
        }
      });
  
      return oproxy;
    }
  }());
  
  var double = n => n * 2;
  var pow    = n => n * n;
  var reverseInt = n => n.toString().split("").reverse().join("") | 0;
  
  pipe(3).double.pow.reverseInt.get; // 63
`解释:
1 pipe是个匿名函数直接被运行 返回一个function (value) 这就是为啥可以 pipe(3)
2 pipe(3). 触发return oproxy; oproxy 是一个 Proxy 对象
  new Proxy({}, {
      get: function (pipeObject, fnName){
          如果 fnName 不是 get就把fnName压入 funcStack 中
          直到 遇到 get 调用 funcStac中存储的fnName 使用reduce函数 挨个执行存入的函数
      }
  })
`