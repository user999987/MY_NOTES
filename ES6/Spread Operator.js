const a1 = [1, 2];
// ES5 copy array
const a2 = a1.concat();
// ES6
const a2 = [...a1]

`shallow copy`
const a1 = [{ foo: 1 }];
const a2 = [{ bar: 2 }];

const a3 = a1.concat(a2);
const a4 = [...a1, ...a2];

`a1[0]['foo']=1
then a3[0]['foo']也会变成1`


console.log([...5]) // 会报错
//需要实现iterator 就像下面
//左边是实现iterator的写法 [Symbol.iterator] 右边是定一个generator
Number.prototype[Symbol.iterator] = function*() {
    let i = 0;
    let num = this.valueOf();
    while (i < num) {
        yield i++;
    }
}
console.log([...5]) // [0, 1, 2, 3, 4] 此时不会报错

let aarrayLike = {
    '0': 'a',
    '1': 'b',
    '2': 'c',
    length: 3,
    [Symbol.iterator]: function*(){yield this['0']},
};
`
[...aarrayLike]
Array [ "a" ]
扩展运算符内部调用的是数据结构的 Iterator 接口，因此只要具有 Iterator 接口的对象，都可以使用扩展运算符
`
