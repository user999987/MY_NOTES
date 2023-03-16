`简单说，this就是属性或方法“当前”所在的对象。`
var obj ={
    foo: function () {
      console.log(this);
    }
  };
  
obj.foo() // obj
`上面代码中，obj.foo方法执行时，它内部的this指向obj。
但是，下面这几种用法，都会改变this的指向。`

// 情况一
(obj.foo = obj.foo)() // window
// 情况二
(false || obj.foo)() // window
// 情况三
(1, obj.foo)() // window

`obj和obj.foo储存在两个内存地址，称为地址一和地址二。称为地址一和地址二。obj.foo()这样调用时，
是从地址一调用地址二，因此地址二的运行环境是地址一，this指向obj。但是，上面三种情况，都是直接取出地址二进行调用，
这样的话，运行环境就是全局环境，因此this指向全局环境。上面三种情况等同于下面的代码。`

// 情况一
(obj.foo = function () {
    console.log(this);
  })()
  // 等同于
  (function () {
    console.log(this);
  })()
  
  // 情况二
  (false || function () {
    console.log(this);
  })()
  
  // 情况三
  (1, function () {
    console.log(this);
  })()


`如果this所在的方法不在对象的第一层，这时this只是指向当前一层的对象，而不会继承更上面的层。`

var a = {
    p: 'Hello',
    b: {
        m: function() {
        console.log(this.p);
        }
    }
};

a.b.m() // undefined
`this 指向当前对象，所以b里面this 指向a，但是b里面的m的函数指向a.b 
因为实际执行的是下面的代码。`

var b = {
  m: function() {
   console.log(this.p);
  }
};

var a = {
  p: 'Hello',
  b: b
};

(a.b).m() // 等同于 b.m()
`如果要达到预期可以这样写`
var a={
    b: {
        p: 'hello',
        m: function(){
            console.log(this.p)
        }
    }
}
var x=a.b
x.m()//是预期效果
var y=a.b.m
y()//undefined 原因就是line 19


`多层嵌套this`
var o = {
    f1: function () {
      console.log(this);
      var f2 = function () {
        console.log(this);
      }();
    }
  }
  
  o.f1()
  // Object
  // Window

`解决方案`
var o = {
    f1: function() {
      console.log(this);
      var that = this;
      var f2 = function() {
        console.log(that);
      }();
    }
  }
  
  o.f1()
  // Object
  // Object
`事实上，使用一个变量固定this的值，然后内层函数调用这个变量，是非常常见的做法，请务必掌握。`

`数组的map和foreach方法，允许提供一个函数作为参数。这个函数内部不应该使用this。`
var o = {
  v: 'hello',
  p: [ 'a1', 'a2' ],
  f: function f() {
    this.p.forEach(function (item) {
      console.log(this.v + ' ' + item);
    });
  }
}

o.f()
// undefined a1
// undefined a2

`上面代码中，foreach方法的回调函数中的this，其实是指向window对象，因此取不到o.v的值。原因跟上一段的多层this是一样的，
就是内层的this不指向外部，而指向顶层对象。
解决这个问题的一种方法，就是前面提到的，使用中间变量固定this。`
var o = {
    v: 'hello',
    p: [ 'a1', 'a2' ],
    f: function f() {
      var that = this;
      this.p.forEach(function (item) {
        console.log(that.v+' '+item);
      });
    }
  }
  
o.f()
// hello a1
// hello a2

`另一种方法是将this当作foreach方法的第二个参数，固定它的运行环境。`

var o = {
  v: 'hello',
  p: [ 'a1', 'a2' ],
  f: function f() {
    this.p.forEach(function (item) {
      console.log(this.v + ' ' + item);
    }, this);
  }
}

o.f()
// hello a1
// hello a2

`call apply bind 都是改变this指向 但是call和apply是执行函数并改变this指向
bind是改变函数内部this指向并返回一个新函数 可以下次调用`
`call examples
函数实例的call方法，可以指定函数内部this的指向（即函数执行时所在的作用域），然后在所指定的作用域中，调用该函数。`
//1
var obj = {};

var f = function () {
  return this;
};

f() === window // true
f.call(obj) === obj // true

//2
var n = 123;
var obj = { n: 456 };

function a() {
  console.log(this.n);
}

a.call() // 123
a.call(null) // 123
a.call(undefined) // 123
a.call(window) // 123
a.call(obj) // 456

`call方法还可以接受多个参数。`

//func.call(thisValue, arg1, arg2, ...)
`call的第一个参数就是this所要指向的那个对象，后面的参数则是函数调用时所需的参数。`

function add(a, b) {
  return a + b;
}

add.call(this, 1, 2) // 3

//apply examples
//1
`apply方法的作用与call方法类似，也是改变this指向，然后再调用该函数。唯一的区别就是，它接收一个数组作为函数执行时的参数，
使用格式如下。
从另一个角度考虑其实就是把func作用在后面的数组
`
//func.apply(thisValue, [arg1, arg2, ...])

`通过apply方法，利用Array构造函数将数组的空元素变成undefined。`
Array.apply(null, ['a', ,'b'])
// [ 'a', undefined, 'b' ]
`空元素与undefined的差别在于，数组的forEach方法会跳过空元素，但是不会跳过undefined。因此，遍历内部元素的时候，会得到不同的结果。`

var a = ['a', , 'b'];

function print(i) {
  console.log(i);
}

a.forEach(print)
// a
// b

Array.apply(null, a).forEach(print)
// a
// undefined
// b

`类似数组对象转换为数组`
Array.prototype.slice.apply({0: 1, length: 1}) // [1]
Array.prototype.slice.apply({0: 1}) // []
Array.prototype.slice.apply({0: 1, length: 2}) // [1, undefined]
Array.prototype.slice.apply({length: 1}) // [undefined]
`从上面代码可以看到，这个方法起作用的前提是，被处理的对象必须有length属性，以及相对应的数字键`

// bind examples
var d = new Date();
d.getTime() // 1481869925657

var print = d.getTime;
print()// Uncaught TypeError: this is not a Date object.

`bind方法的参数就是所要绑定this的对象，下面是一个更清晰的例子。`

var counter = {
  count: 0,
  inc: function () {
    this.count++;
  }
};

var func = counter.inc.bind(counter);
func();
counter.count // 1
`如果不用bind就相当于把counter.inc给func, 但是 counter.inc此时是一个单纯的函数和counter没有关系 因为counter.inc指向
的是一个函数的地址`

`this绑定到其他对象也是可以的。`
var counter = {
  count: 0,
  inc: function () {
    this.count++;
  }
};

var obj = {
  count: 100
};
var func = counter.inc.bind(obj);
func();
obj.count // 101

`bind方法每运行一次，就返回一个新函数，这会产生一些问题。比如，监听事件的时候，不能写成下面这样。`
element.addEventListener('click', o.m.bind(o));

`正确的方法是写成下面这样`
var listener = o.m.bind(o);
element.addEventListener('click', listener);
//  ...
element.removeEventListener('click', listener);

`回调函数是 JavaScript 最常用的模式之一，但是一个常见的错误是，
将包含this的方法直接当作回调函数。解决方法就是使用bind方法，将counter.inc绑定counter。`

var counter = {
    count: 0,
    inc: function () {
      'use strict';
      this.count++;
    }
  };
  
  function callIt(callback) {
    callback();
  }
  
  callIt(counter.inc.bind(counter));
  counter.count // 1