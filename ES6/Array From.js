`Array.from方法用于将两类对象转为真正的数组：类似数组的对象（array-like object）和可遍历（iterable）的对象`

`
实际应用中，常见的类似数组的对象是 DOM 操作返回的 NodeList 集合，以及函数内部的arguments对象。
Array.from都可以将它们转为真正的数组。
`
// Condition 1
// NodeList对象
let ps = document.querySelectorAll('p');
Array.from(ps).filter(p => {
  return p.textContent.length > 100;
});

// Condition 2
`Array.from方法还支持类似数组的对象。所谓类似数组的对象，本质特征只有一点，即必须有length属性`
Array.from({ length: 3 });
// [ undefined, undefined, undefined ]

`对于还没有部署该方法的浏览器，可以用Array.prototype.slice方法替代。`
const toArray = (() =>
  Array.from ? Array.from : obj => [].slice.call(obj)
)();

`Array.from还可以接受第二个参数，作用类似于数组的map方法，用来对每个元素进行处理，将处理后的值放入返回的数组。`
Array.from(arrayLike, x => x * x);

`返回各种数据的类型。`
function typesOf () {
    return Array.from(arguments, value => typeof value)
  }
  typesOf(null, [], NaN)
  // ['object', 'object', 'number']


`Array()会因为参数的多少导致重载发生`
Array() // []
Array(3) // [, , ,]
Array(3, 11, 8) // [3, 11, 8]

`Array.of()行为始终保持一致`
Array.of() // []
Array.of(undefined) // [undefined]
Array.of(1) // [1]
Array.of(1, 2) // [1, 2]