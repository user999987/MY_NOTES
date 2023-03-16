## hashCode & equals
Java中, Set要求元素不重复. 如何判断重复?  Object.equals 方法<br>
如果集合中已经有1000元素了, 第1001个元素加入集合就要调用1000次 equals 方法<br>
hasdCode 得到一个对象存储的物理地址(实际可能并不是)<br>
新元素进来时候先 调用 hashCode 物理地址是不是被占用了 如果没有 放入 如果有 调用 equals

所以，Java对于eqauls方法和hashCode方法是这样规定的：

如果两个对象相同，那么它们的hashCode值一定要相同。

如果两个对象的hashCode相同，它们并不一定相同。

为什么重写eqauls一定要重写hashcode:<br>
hashCode本来就是为了提高程序少使用equals才存在的, 只重写 equals 会出现 不同类型对象的特征相同和判定是相同对象 实际上并不是
## open
Classes are final by default; to make a class inheritable, mark it as open.
```kotlin
open class Shape

class Rectangle(var height: Double, var length: Double): Shape() {
    var perimeter = (height + length) * 2
}
```
## null or not null
```kotlin
// ?表示nullable ?: 是null ?.非null
// not null
val files = File("Test").listFiles()
println(files?.size) // size is printed if files is not null
// is null
val values = ...
val email = values["email"] ?: throw IllegalStateException("Email is missing!")

// not null else
val files = File("Test").listFiles()
println(files?.size ?: "empty") // if files is null, this prints "empty"
```

## execute if not null
```kotlin
val value = ...

value?.let {
    ... // execute this block if not null
}

```

## swap two variable
```kotlin
var a=1
var b=2
a=b.also{b=a}
```

## mark TODO
Kotlin's standard library has a TODO() function that will always throw a NotImplementedError. Its return type is Nothing so it can be used regardless of expected type
```kotlin
fun calcTaxes(): BigDecimal = TODO("Waiting for feedback from accounting")
Copied!
```

## Kotlin has no implicit conversions
All number types support conversions to other types:
* toByte(): Byte
* toShort(): Short
* toInt(): Int
* toLong(): Long
* toFloat(): Float
* toDouble(): Double
* toChar(): Char
In many cases, there is no need in explicit conversions because the type is inferred from the context, and arithmetical operations are overloaded for appropriate conversions, for example:
```kotlin
val l = 1L + 3 // Long + Int => Long
```

## NaN and -0.0
* NaN is considered equal to itesefl
* NaN is considered greater than any other element including `POSITIVE_INFINITY`
* -0.0 is considered less than 0.0

## String template
```kotlin
val s = "abc"
println("$s.length is ${s.length}") // prints "abc.length is 3"
```

## Arrays
```kotlin
class Array<T> private constructor() {
    val size: Int
    operator fun get(index: Int): T
    operator fun set(index: Int, value: T): Unit

    operator fun iterator(): Iterator<T>
    // ...
}
//1
arrayOf(123)
//2
val asc = Array(5){i->(i*i).toString()}
asc.forEach { println(it) }
```
## Primitive type arrays
```kotlin
val x: IntArray = intArrayOf(1, 2, 3)
x[0] = x[1] + x[2]

val arr = IntArray(5)
```

## is and !is
```kotlin
if (obj is String) {
    print(obj.length)
}
if (obj !is String) { // same as !(obj is String)
    print("Not a String")
}
```

## for
```kotlin
for (i in 1..3) {
    println(i)
}
for (i in 6 downTo 0 step 2) {
    println(i)
}
for (i in array.indices) {
    println(array[i])
}
for ((index, value) in array.withIndex()) {
    println("the element at $index is $value")
}
```

## inheritance
All classes in Kotlin have a common superclass, `Any`, which is the default superclass for a class with no supertypes declared.<br>
By default, Kotlin classes are final – they can’t be inherited. To make a class inheritable, mark it with the open keyword.
```kotlin
open class Base(p: Int)

class Derived(p: Int) : Base(p)
```
If the derived class has a primary constructor, the base class can (and must) be initialized in that primary constructor according to its parameters.<br>
If the derived class has no primary constructor, then each secondary constructor has to initialize the base type using the super keyword or it has to delegate to another constructor which does.
```kotlin
class MyView : View {
    constructor(ctx: Context) : super(ctx)

    constructor(ctx: Context, attrs: AttributeSet) : super(ctx, attrs)
}
```

```kotlin
open class Shape {
    open fun draw() { /*...*/ }
    fun fill() { /*...*/ }
}
// can only override method that is declared as open, if class has no open modifier, then 
// open on method has no effect
class Circle() : Shape() {
    override fun draw() { /*...*/ }
}
```
A member marked override is itself open, so it may be overridden in subclasses. If you want to prohibit re-overriding, use final
```kotlin
open class Rectangle() : Shape() {
    final override fun draw() { /*...*/ }
}
/can use the override keyword as part of the property declaration in a primary constructor
interface Shape {
    val vertexCount: Int
}

class Rectangle(override val vertexCount: Int = 4) : Shape // Always has 4 vertices

class Polygon : Shape {
    override var vertexCount: Int = 0  // Can be set to any number later
}
```
During the construction of a new instance of a derived class, the base class initialization is done as the first step (preceded only by evaluation of the arguments for the base class constructor), which means that it happens before the initialization logic of the derived class is run.<br>
This means that when the base class constructor is executed, the properties declared or overridden in the derived class have not yet been initialized. Using any of those properties in the base class initialization logic (either directly or indirectly through another overridden open member implementation) may lead to incorrect behavior or a runtime failure. When designing a base class, you should therefore avoid using open members in the constructors, property initializers, or init blocks.

Inside an inner class, accessing the superclass of the outer class is done using the super keyword qualified with the outer class name: super@Outer
```kotlin
class FilledRectangle: Rectangle() {
    override fun draw() {
        val filler = Filler()
        filler.drawAndFill()
    }

    inner class Filler {
        fun fill() { println("Filling") }
        fun drawAndFill() {
            super@FilledRectangle.draw() // Calls Rectangle's implementation of draw()
            fill()
            println("Drawn a filled rectangle with color ${super@FilledRectangle.borderColor}") // Uses Rectangle's implementation of borderColor's get()
        }
    }
}
```

## getter and setter
```kotlin
// example of a custom getter
val isEmpty: Boolean
    get() = this.size == 0
//a custom setter. By convention, the name of the setter parameter is value
var stringRepresentation: String
    get() = this.toString()
    set(value) {
        setDataFromString(value) // parses the string and assigns values to other properties
    }

//If you need to annotate an accessor or change its visibility, but you don't need to change the default implementation, you can define the accessor without defining its body:
var setterVisibility: String = "abc"
    private set // the setter is private and has the default implementation

var setterWithAnnotation: Any? = null
    @Inject set // annotate the setter with Inject

```

## backing fields
```kotlin
var counter = 0 // the initializer assigns the backing field directly
    set(value) {
        if (value >= 0)
            field = value
            // counter = value 
            // ERROR StackOverflow: Using actual name 'counter' would make setter recursive
    }
```

## Late-initialized properties and variables
Normally, properties declared as having a non-null type must be initialized in the constructor. However, it is often the case that doing so is not convenient.。
For example, properties can be initialized through dependency injection, or in the setup method of a unit test. In these cases, you cannot supply a non-null initializer in the constructor, but you still want to avoid null checks when referencing the property inside the body of a class.

To handle such cases, you can mark the property with the lateinit modifier:
```kotlin
public class MyTest {
    lateinit var subject: TestSubject

    @SetUp fun setup() {
        subject = TestSubject()
    }

    @Test fun test() {
        subject.method()  // dereference directly
    }
}

//This check is only available for properties that are lexically accessible when declared in the same type, in one of the outer types, or at top level in the same file.
if (foo::bar.isInitialized) {
    println(foo.bar)
}

```

## interface
What makes them different from abstract classes is that interfaces cannot store state. They can have properties but these need to be abstract or to provide accessor implementations.
```kotlin
interface MyInterface {
    fun bar()
    fun foo() {
      // optional body
    }
}
class Child : MyInterface {
    override fun bar() {
        // body
    }
}
```

## properties in interface
You can declare properties in interfaces. A property declared in an interface can either be abstract, or it can provide implementations for accessors. Properties declared in interfaces can't have backing fields, and therefore accessors declared in interfaces can't reference them.
```kotlin
interface MyInterface {
    val prop: Int // abstract

    val propertyWithImplementation: String
        get() = "foo"

    fun foo() {
        print(prop)
    }
}

class Child : MyInterface {
    override val prop: Int = 29
}
```

## functional interface, or a Single Abstract Method (SAM) interface
```kotlin
fun interface IntPredicate {
   fun accept(i: Int): Boolean
}

val isEven = IntPredicate { it % 2 == 0 }

fun main() {
   println("Is 7 even? - ${isEven.accept(7)}")
}
```

## modules
The internal visibility modifier means that the member is visible within the same module. More specifically, a module is a set of Kotlin files compiled together:
* an IntelliJ IDEA module
* a Maven project
* a Gradle source set (with the exception that the test source set can access the internal declarations of main)
* a set of files compiled with one invocation of the <kotlinc> Ant task

## extensions
You can write new functions for a class from a third-party library that you can't modify. Such functions can be called in the usual way, as if they were methods of the original class. This mechanism is called an extension function. There are also extension properties that let you define new properties for existing classes.

```kotlin
fun MutableList<Int>.swap(index1: Int, index2: Int) {
    val tmp = this[index1] // 'this' corresponds to the list
    this[index1] = this[index2]
    this[index2] = tmp
}

fun <T> MutableList<T>.swap(index1: Int, index2: Int) {
    val tmp = this[index1] // 'this' corresponds to the list
    this[index1] = this[index2]
    this[index2] = tmp
}
```

## Extensions are resolved statically
Extensions do not actually modify the classes they extend. By defining an extension, you are not inserting new members into a class, only making new functions callable with the dot-notation on variables of this type.
```kotlin
open class Shape
class Rectangle: Shape()

fun Shape.getName() = "Shape"
fun Rectangle.getName() = "Rectangle"

fun printClassName(s: Shape) {
    println(s.getName())
}

printClassName(Rectangle())
// Shape
```
If a class has a member function, and an extension function is defined which has the same receiver type, the same name, and is applicable to given arguments, the member always wins.<br>
However, it's perfectly OK for extension functions to overload member functions that have the same name but a different signature.

Note that extensions can be defined with a nullable receiver type. These extensions can be called on an object variable even if its value is null, and they can check for this == null inside the body.
```kotlin
fun Any?.toString(): String {
    if (this == null) return "null"
    // after the null check, 'this' is autocast to a non-null type, so the toString() below
    // resolves to the member function of the Any class
    return toString()
}
```
Since extensions do not actually insert members into classes, there's no efficient way for an extension property to have a backing field. This is why initializers are not allowed for extension properties. Their behavior can only be defined by explicitly providing getters/setters.
```kotlin
val <T> List<T>.lastIndex: Int
    get() = size - 1

// error: initializers are not allowed for extension properties
val House.number = 1 
```

## Generics: in, out, where
```kotlin
// Java
void copyAll(Collection<Object> to, Collection<String> from) {
    to.addAll(from);
    // !!! Would not compile with the naive declaration of addAll:
    // Collection<String> is not a subtype of Collection<Object>
}

//The wildcard type argument ? extends E indicates that this method accepts a collection of objects of E or a subtype of E, not just E itself. 
// Java
interface Collection<E> ... {
    void addAll(Collection<? extends E> items);
}

```
## Generic functions
Classes aren’t the only declarations that can have type parameters. Functions can, too. Type parameters are placed before the name of the function:
```kotlin
fun <T> singletonList(item: T): List<T> {
    // ...
}

fun <T> T.basicToString(): String {  // extension function
    // ...
}
```

## High-order function
A higher-order function is a function that takes functions as parameters, or returns a function
```kotlin
fun <T, R> Collection<T>.fold(
    initial: R,
    combine: (acc: R, nextElement: T) -> R
): R {
    var accumulator: R = initial
    for (element: T in this) {
        accumulator = combine(accumulator, element)
    }
    return accumulator
}
```

## what is  <T,R>
```
To be able to create a generic function the compiler must know that you want to work with diferent types. Kotlin is (like Java or C#) a strongly typed language. so just passing different types into a function will make the compiler mad.

To tell the compiler that a function should be accepting multiple types you need to add a "Type Parameter"

The <T> after fun is the definition of said "Type Parameter".
Which is then used at the item Argument.

Now the compiler knows that you'll specifiy the type of item when you make the call to singletonList(item: T)

Just doing

fun singletonList(item: T) : List<T> {[...]}
would make the compiler unhappy as it does not know T.
(As long as you don't have a class named T)

You also can have multiple "Type Params" when you separate them with commas:

fun <T, U> otherFunction(firstParam: T, secondParam: U): ReturnType
```

## Passing trailing lambdas
```kotlin
//According to Kotlin convention, if the last parameter of a function is a function, then a lambda expression passed as the corresponding argument can be placed outside the parentheses
val product = items.fold(1) { acc, e -> acc * e }
//If the lambda is the only argument in that call, the parentheses can be omitted entirely:
run { println("...") }
//If the compiler can parse the signature without any parameters, the parameter does not need to be declared and -> can be omitted. The parameter will be implicitly declared under the name it
ints.filter { it > 0 } // this literal is of type '(it: Int) -> Boolean'
// the value of the last expression is implicitly returned.
ints.filter {
    val shouldFilter = it > 0
    shouldFilter
}
```

## inline
调用一个方法其实就是一个方法压栈和出栈的过程，调用方法时将栈帧压入方法栈，然后执行方法体，方法结束时将栈帧出栈，这个压栈和出栈的过程是一个耗费资源的过程，这个过程中传递形参也会耗费资源。我们在写代码的时候难免会遇到这种情况,就是很多处的代码是一样的,于是乎我们就会抽取出一个公共方法来进行调用,这样看起来就会很简洁;但是也出现了一个问题,就是这个方法会被频繁调用,就会很耗费资源。由于 lambda 表达式都会被悄悄的编译成一个匿名类。这也就意味着需要占用内存。如果短时间内 lambda 表达式被多次调用，大量的对象实例化就会产生内存流失（Memory Churn）
``` kotlin
fun <T> method(lock: Lock, body: () -> T): T {
        lock.lock()
        try {
            return body()
        } finally {
            lock.unlock()
        }
    }
```
对于编译器来说，调用method方法就要将参数lock和lambda表达式{"我是body的方法体"}进行传递，就要将method方法进行压栈出栈处理，这个过程就会耗费资源。如果是很多地方调用,就会执行很多次,这样就非常消耗资源了.
于是乎就引进了inline

被inline标记的函数就是内联函数,其原理就是:在编译时期,把调用这个函数的地方用这个函数的方法体进行替换
```kotlin
// 调用此方法 在编译时期就会把下面的内容替换到调用该方法的地方,这样就会减少方法压栈,出栈,进而减少资源消耗
method(lock, {"我是body方法体"})//lock是一个Lock对象

lock.lock()
try {
    return "我是body方法体"
} finally {
    lock.unlock()
}
```
因为method是内联函数,所以它的形参也是inline的,所以body就是inline的,但是在编译时期,body已经不是一个函数对象,而是一个具体的值,然而otherMehtod却要接收一个body的函数对象,所以就编译不通过了
```kotlin
// 解决方法 inline fun <T> mehtod(lock: Lock, noinline body: () -> T): T
inline fun <T> mehtod(lock: Lock, body: () -> T): T {
            lock.lock()
            try {
                otherMehtod(body)//会报错
                return body()
            } finally {
                lock.unlock()
            }
    }

fun <T> otherMehtod(body: ()-> T){

}
```
crossinline的作用是内联函数中让被标记为crossinline 的lambda表达式不允许非局部返回。如果一个函数中,存在一个lambda表达式，在该lambda中不支持直接通过return退出该函数的,只能通过return@XXXinterface这种方式，如果这个函数是内联的却是可以的，这种直接从lambda中return掉函数的方法就是非局部返回。crossinline就是为了让其不能直接return