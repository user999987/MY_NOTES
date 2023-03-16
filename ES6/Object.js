`ES6 允许在大括号里面，直接写入变量和函数，作为对象的属性和方法。这样的书写更加简洁`

const foo = 'bar';
const baz = {foo};
baz // {foo: "bar"}

// 等同于
const baz = {foo: foo};
`上面代码中，变量foo直接写在大括号里面。这时，属性名就是变量名, 属性值就是变量值。下面是另一个例子。`

function f(x, y) {
  return {x, y};
}

// 等同于

function f(x, y) {
  return {x: x, y: y};
}

f(1, 2) // Object {x: 1, y: 2}

`方法也可以简写`
const o = {
    method() {
      return "Hello!";
    }
  };

// 等同于

const o = {
method: function() {
        return "Hello!";
    }
};

function getPoint() {
    const x = 1;
    const y = 10;
    return {x, y};
}

getPoint()
// {x:1, y:10} 

`模块输出变量`
let ms = {};
function getItem (key) {
  return key in ms ? ms[key] : null;
}
function setItem (key, value) {
  ms[key] = value;
}
function clear () {
  ms = {};
}

module.exports = { getItem, setItem, clear };
// 等同于
module.exports = {
  getItem: getItem,
  setItem: setItem,
  clear: clear
};

`属性的赋值器（setter）和取值器（getter），事实上也是采用这种写法。`

const cart = {
  _wheels: 4,

  get wheels () {
    return this._wheels;
  },

  set wheels (value) {
    if (value < this._wheels) {
      throw new Error('数值太小了！');
    }
    this._wheels = value;
  }
}
`注意，简写的对象方法不能用作构造函数，会报错。`

`ES6 允许对象属性名用表达式`

//属性名
let lastWord = 'last word';

const a = {
  'first word': 'hello',
  [lastWord]: 'world'
};

a['first word'] // "hello"
a[lastWord] // "world"
a['last word'] // "world"

//方法名
let obj = {
    ['h' + 'ello']() {
      return 'hi';
    }
  };
  
  obj.hello() // hi

`遍历对象属性`
Reflect.ownKeys(obj)
Reflect.ownKeys({ [Symbol()]:0, b:0, 10:0, 2:0, a:0 })
// ['2', '10', 'b', 'a', Symbol()]

`optional chaining operator`
const firstName = message?.body?.user?.firstName || 'default';
const fooValue = myForm.querySelector('input[name=foo]')?.value

`下面是这个运算符常见的使用形式，以及不使用该运算符时的等价形式。`

a?.b
// 等同于
a == null ? undefined : a.b

a?.[x]
// 等同于
a == null ? undefined : a[x]

a?.b()
// 等同于
a == null ? undefined : a.b()

a?.()
// 等同于
a == null ? undefined : a()

delete a?.b
// 等同于
a == null ? undefined : delete a.b
`上面代码中，如果a是undefined或null，会直接返回undefined，而不会进行delete运算。`

`ES2020 引入了一个新的 Null 判断运算符??
只有运算符左侧的值为null或undefined时，才会返回右侧的值。`
const headerText = response.settings.headerText ?? 'Hello, world!';
const animationDuration = response.settings.animationDuration ?? 300;
const showSplashScreen = response.settings.showSplashScreen ?? true;

`??有一个运算优先级问题，它与&&和||的优先级孰高孰低。现在的规则是，如果多个逻辑运算符一起使用，必须用括号表明优先级，否则会报错。
`
// 报错
lhs && middle ?? rhs
lhs ?? middle && rhs
lhs || middle ?? rhs
lhs ?? middle || rhs
`上面四个表达式都会报错，必须加入表明优先级的括号。`

(lhs && middle) ?? rhs;
lhs && (middle ?? rhs);

(lhs ?? middle) && rhs;
lhs ?? (middle && rhs);

(lhs || middle) ?? rhs;
lhs || (middle ?? rhs);

(lhs ?? middle) || rhs;
lhs ?? (middle || rhs);