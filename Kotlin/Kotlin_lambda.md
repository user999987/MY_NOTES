# Higher-order functions
A higher-order function is a function that takes functions as parameters, or returns a function.<br>
Kotlin 里「函数可以作为参数」这件事的本质，是函数在 Kotlin 里可以作为对象存在——因为只有对象才能被作为参数传递。但 Kotlin 的函数本身的性质又决定了它没办法被当做一个对象。那怎么办呢？Kotlin 的选择是，那就创建一个和函数具有相同功能的对象。怎么创建？使用双冒号。<br>
在 Kotlin 里，一个函数名的左边加上双冒号，它就不表示这个函数本身了，而表示一个对象，或者说一个指向对象的引用，但，这个对象可不是函数本身，而是一个和这个函数具有相同功能的对象。<br>
```kotlin
fun b(param: Int): String {
  return param.toString()
}

fun a(funParam: (Int) -> String): String {
  return funParam(1)
}

a(::b)
val d = ::b

b(1) // 调用函数
d(1) // 用对象 a 后面加上括号来实现 b() 的等价操作 实际上 d.invoke(1)
(::b)(1) // 用对象 :b 后面加上括号来实现 b() 的等价操作 实际上 (::b).invoke(1)
```

```kotlin
fun calculate(name: String, operation: (String) -> String): String {  // 1
        return operation(name)                                          // 2
    }

    fun sum(x: String) = x
    val sumResult = calculate("4", ::sum)                          // 4
    val mulResult = calculate("4") { name ->
        val n= "x"
        val name1=name+n
        println(name1)
        name1

    }               // 5
    println("sumResult $sumResult, mulResult $mulResult")
```

```kotlin
//都是传递实参时候的例子

//如果 Lambda 是函数的最后一个参数，你可以把 Lambda 写在括号的外面
view.setOnClickListener() { v: View ->
  switchToNextPage()
}
//如果 Lambda 是函数唯一的参数，你还可以直接把括号去了
view.setOnClickListener { v: View ->
  switchToNextPage()
}

//如果这个 Lambda 是单参数的，它的这个参数也省略掉不写
//如果需要用 可以用 it
view.setOnClickListener {
  switchToNextPage()
  it.setVisibility(GONE)
}
```