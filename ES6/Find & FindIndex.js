`数组实例的find方法，用于找出第一个符合条件的数组成员。它的参数是一个回调函数，所有数组成员依次执行该回调函数，
直到找出第一个返回值为true的成员，然后返回该成员。如果没有符合条件的成员，则返回undefined。`

[1, 4, -5, 10].find((n) => n < 0)
// -5
//上面代码找出数组中第一个小于 0 的成员。

[1, 5, 10, 15].find(function(value, index, arr) {
  return value > 9;
}) // 10
`上面代码中，find方法的回调函数可以接受三个参数，依次为当前的值、当前的位置和原数组。
数组实例的findIndex方法的用法与find方法非常类似，返回第一个符合条件的数组成员的位置，如果所有成员都不符合条件，则返回-1。`
[1, 5, 10, 15].findIndex(function(value, index, arr) {
    return value > 9;
  }) // 2

  `这两个方法都可以接受第二个参数，用来绑定回调函数的this对象。`

  function f(v){
    return v > this.age;
  }
  let person = {name: 'John', age: 20};
  [10, 12, 26, 15].find(f, person);    // 26
  `上面的代码中，find函数接收了第二个参数person对象，回调函数中的this对象指向person对象。
  另外，这两个方法都可以发现NaN，弥补了数组的indexOf方法的不足。`
  
  [NaN].indexOf(NaN)
  // -1
  
  [NaN].findIndex(y => Object.is(NaN, y))
  // 0
  `上面代码中，indexOf方法无法识别数组的NaN成员，但是findIndex方法可以借助Object.is方法做到。`


  [1, 2, [3, [4, 5]]].flat()
// [1, 2, 3, [4, 5]]

[1, 2, [3, [4, 5]]].flat(2)
// [1, 2, 3, 4, 5]

[1, [2, [3]]].flat(Infinity)
// [1, 2, 3]

//[1, 2, , 4, 5].flat()
// [1, 2, 4, 5]