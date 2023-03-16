`Object.assign方法用于对象的合并，将源对象（source）的所有可枚举属性，复制到目标对象（target）。`

const target = { a: 1 };

const source1 = { b: 2 };
const source2 = { c: 3 };

Object.assign(target, source1, source2);
target // {a:1, b:2, c:3}


//1）为对象添加属性

class Point {
  constructor(x, y) {
    Object.assign(this, {x, y});
  }
}
//上面方法通过Object.assign方法，将x属性和y属性添加到Point类的对象实例。

//（2）为对象添加方法

Object.assign(SomeClass.prototype, {
  someMethod(arg1, arg2) {
    //···
  },
  anotherMethod() {
    //···
  }
});

// 等同于下面的写法
SomeClass.prototype.someMethod = function (arg1, arg2) {
  //···
};
SomeClass.prototype.anotherMethod = function () {
  //···
};
//上面代码使用了对象属性的简洁表示法，直接将两个函数放在大括号中，再使用assign方法添加到SomeClass.prototype之中。

//（3）克隆对象

function clone(origin) {
  return Object.assign({}, origin);
}
//上面代码将原始对象拷贝到一个空对象，就得到了原始对象的克隆。

//不过，采用这种方法克隆，只能克隆原始对象自身的值，不能克隆它继承的值。如果想要保持继承链，可以采用下面的代码。

function clone(origin) {
  let originProto = Object.getPrototypeOf(origin);
  return Object.assign(Object.create(originProto), origin);
}
//（4）合并多个对象

//将多个对象合并到某个对象。

const merge =
  (target, ...sources) => Object.assign(target, ...sources);
//如果希望合并后返回一个新对象，可以改写上面函数，对一个空对象合并。

const merge =
  (...sources) => Object.assign({}, ...sources);


`Object.getOwnPropertyDescriptors()方法，返回指定对象所有自身属性（非继承属性）的描述对象。`
const obj = {
    foo: 123,
    get bar() { return 'abc' }
  };
  
  Object.getOwnPropertyDescriptors(obj)
  // { foo:
  //    { value: 123,
  //      writable: true,
  //      enumerable: true,
  //      configurable: true },
  //   bar:
  //    { get: [Function: get bar],
  //      set: undefined,
  //      enumerable: true,
  //      configurable: true } }


  `Object.fromEntries()方法是Object.entries()的逆操作，用于将一个键值对数组转为对象。`

  Object.fromEntries([
    ['foo', 'bar'],
    ['baz', 42]
  ])
  // { foo: "bar", baz: 42 }

  `该方法的一个用处是配合URLSearchParams对象，将查询字符串转为对象。`

  Object.fromEntries(new URLSearchParams('foo=bar&baz=qux'))
  // { foo: "bar", baz: "qux" }