# Asynchronous programming techniques

## Threading
* Threads aren't cheap. Threads require context switches which are costly.
* Threads aren't infinite. The number of threads that can be launched is limited by the underlying operating system. In server-side applications, this could cause a major bottleneck.
* Threads aren't always available. Some platforms, such as JavaScript do not even support threads.
* Threads aren't easy. Debugging threads, avoiding race conditions are common problems we suffer in multi-threaded programming.

## Callback
With callbacks, the idea is to pass one function as a parameter to another function, and have this one invoked once the process has completed. Callbacks are quite common in event-loop architectures such as JavaScript. 因为JS 是个异步语言
```javascript
var fs = require("fs")
var c
function f(x){
    console.log(x)
}
function writeFile(){
    fs.writeFile("xxx","xxx", function(err){
        if(!err){
            console.log("written done")
            c=1
        }
    });
}
c=0
writeFile()
f(c)

// 回调函数
function writeFile(callback){
    fs.writeFile("xxx","xxx", function(err){
        if(!err){
            console.log("written done")
            c=1
            callback(c)
        }
    });
}
writeFile(f)
```
程序运行到writeFile这一行时候是一个比较耗时的IO操作，JS碰到这种操作不会一直等函数执行完毕，而是直接指向下一行代码，writeFile内部的c=1没有被执行 所以打印的话结果为0<br>
* Difficulty of nested callbacks. Usually a function that is used as a callback, often ends up needing its own callback. This leads to a series of nested callbacks which lead to incomprehensible code. The pattern is often referred to as the titled christmas tree (braces represent branches of the tree).
* Error handling is complicated. The nesting model makes error handling and propagation of these somewhat more complicated.

## Futures, promises, and others
The idea behind futures or promises (there are also other terms these can be referred to depending on language/platform), is that when we make a call, we're promised that at some point it will return with an object called a Promise, which can then be operated on.

## Coroutines
Kotlin's approach to working with asynchronous code is using coroutines, which is the idea of suspendable computations, i.e. the idea that a function can suspend its execution at some point and resume later on.

# Coroutines in Kotlin

## Cancellations and timeouts
In a long-running application you might need fine-grained control on your background coroutines. For example, a user might have closed the page that launched a coroutine and now its result is no longer needed and its operation can be cancelled. The `launch` function returns a `Job` that can be used to cancel the running coroutine:
```kotlin
import kotlinx.coroutines.*

fun main() = runBlocking {
    val job = launch {
        repeat(1000) { i ->
            println("job: I'm sleeping $i ...")
            delay(500L)
        }
    }
    delay(1300L) // delay a bit
    println("main: I'm tired of waiting!")
    //There is also a Job extension function cancelAndJoin that combines cancel and join invocations
    job.cancel() // cancels the job
    job.join() // waits for job's completion 
    println("main: Now I can quit.")    
}
```
Coroutine cancellation is cooperative. A coroutine code has to cooperate to be cancellable. All the suspending functions in kotlinx.coroutines are cancellable. They check for cancellation of coroutine and throw CancellationException when cancelled. However, if a coroutine is working in a computation and does not check for cancellation, then it cannot be cancelled, like the following example shows
```kotlin
import kotlinx.coroutines.*

fun main() = runBlocking {
    val startTime = System.currentTimeMillis()
    val job = launch(Dispatchers.Default) {
        var nextPrintTime = startTime
        var i = 0
        // while (isActive)
        while (i < 5) { // computation loop, just wastes CPU
            // print a message twice a second
            if (System.currentTimeMillis() >= nextPrintTime) {
                println("job: I'm sleeping ${i++} ...")
                nextPrintTime += 500L
            }
        }
    }
    delay(1300L) // delay a bit
    println("main: I'm tired of waiting!")
    job.cancelAndJoin() // cancels the job and waits for its completion
    println("main: Now I can quit.")    
}
```
Two ways to solve this problem: 
1. use yield function
2. explictly check cancellation status `while (isActive)`<br>
isActive is an extension property available inside the coroutine via the CoroutineScope object.

## Run non-cancellable block
```kotlin
import kotlinx.coroutines.*

fun main() = runBlocking {
    val job = launch {
        try {
            repeat(1000) { i ->
                println("job: I'm sleeping $i ...")
                delay(500L)
            }
        } finally {
            // without using withContext(NonCancellable) will suspend in a cancelled coroutine
            // you will not see the second println
            withContext(NonCancellable) {
                println("job: I'm running finally")
                delay(1000L)
                println("job: And I've just delayed for 1 sec because I'm non-cancellable")
            }
        }
    }
    delay(1300L) // delay a bit
    println("main: I'm tired of waiting!")
    job.cancelAndJoin() // cancels the job and waits for its completion
    println("main: Now I can quit.")    
}
``` 

## Timeout
```kotlin
import kotlinx.coroutines.*

fun main() = runBlocking {
    withTimeout(1300L) {
        repeat(1000) { i ->
            println("I'm sleeping $i ...")
            delay(500L)
        }
    }
}
// below is output
I'm sleeping 0 ...
I'm sleeping 1 ...
I'm sleeping 2 ...
Exception in thread "main" kotlinx.coroutines.TimeoutCancellationException: Timed out waiting for 1300 ms
 at (Coroutine boundary. (:-1) 
 at FileKt$main$1$1.invokeSuspend (File.kt:-1) 
 at FileKt$main$1.invokeSuspend (File.kt:-1) 
Caused by: kotlinx.coroutines.TimeoutCancellationException: Timed out waiting for 1300 ms
at (Coroutine boundary .(:-1)
at FileKt$main$1$1 .invokeSuspend(File.kt:-1)
at FileKt$main$1 .invokeSuspend(File.kt:-1)
```
The TimeoutCancellationException that is thrown by withTimeout is a subclass of CancellationException.We have not seen its stack trace printed on the console before. That is because inside a cancelled coroutine CancellationException is considered to be a normal reason for coroutine completion. However, in this example we have used withTimeout right inside the main function.
``kotlin
fun main() = runBlocking {
    // in this way, no exception thrown
    val x=launch{
        withTimeout(1300L) {
            repeat(1000) { i ->
                println("I'm sleeping $i ...")
                delay(500L)
            }
        }
    }
}
```
You can wrap the code with timeout in a try {...} catch (e: TimeoutCancellationException) {...} block if you need to do some additional action specifically on any kind of timeout or use the withTimeoutOrNull function that is similar to withTimeout but returns null on timeout instead of throwing an exception:
```kotlin
import kotlinx.coroutines.*

fun main() = runBlocking {
    val result = withTimeoutOrNull(1300L) {
        repeat(1000) { i ->
            println("I'm sleeping $i ...")
            delay(500L)
        }
        "Done" // will get cancelled before it produces this result
    }
    println("Result is $result")
}
```

## Asynchronous timeout and resources
The timeout event in withTimeout is asynchronous with respect to the code running in its block and may happen at any time, even right before the return from inside of the timeout block.
```kotlin
var acquired = 0

class Resource {
    init { acquired++ } // Acquire the resource
    fun close() { acquired-- } // Release the resource
}

fun main() {
    runBlocking {
        repeat(100_000) { // Launch 100K coroutines
            launch { 
                val resource = withTimeout(60) { // Timeout of 60 ms
                    delay(50) // Delay for 50 ms
                    Resource() // Acquire a resource and return it from withTimeout block     
                }
                resource.close() // Release the resource
            }
        }
    }
    // Outside of runBlocking all coroutines have completed
    println(acquired) // Print the number of resources still acquired
}
```
If you run the above code you'll see that it does not always print zero, to workaround this:
```kotlin
repeat(100_000) { // Launch 100K coroutines
            launch { 
                var resource: Resource? = null // Not acquired yet
                try {
                    withTimeout(60) { // Timeout of 60 ms
                        delay(50) // Delay for 50 ms
                        resource = Resource() // Store a resource to the variable if acquired      
                    }
                    // We can do something else with the resource here
                } finally {  
                    resource?.close() // Release the resource if it was acquired
                }
            }
        }
```
use try/finally make sure always close the resource

## Sequential by default & Concurrent using async & Lazily started async
Suspend functions run sequentially by default.
```kotlin
fun main() = runBlocking<Unit> {
    val time = measureTimeMillis {
        val one = doSomethingUsefulOne()
        val two = doSomethingUsefulTwo()
        println("The answer is ${one + two}")
    }
    println("Completed in $time ms")    
}

// make them run concurrently
val time = measureTimeMillis {
    // use async
    // difference between async and launch is lanuch do not return anything
    val one = async { doSomethingUsefulOne() }
    val two = async { doSomethingUsefulTwo() }
    println("The answer is ${one.await() + two.await()}")
}
println("Completed in $time ms")

//async can be made lazy by setting its start parameter to CoroutineStart.LAZY. In this mode it only starts the coroutine when its result is required by await, or if its Job 's start function is invoked
val time = measureTimeMillis {
    val one = async(start = CoroutineStart.LAZY) { doSomethingUsefulOne() }
    val two = async(start = CoroutineStart.LAZY) { doSomethingUsefulTwo() }
    // some computation
    one.start() // start the first one
    two.start() // start the second one
    println("The answer is ${one.await() + two.await()}")
}
println("Completed in $time ms")
```
If we just call await in println without first calling start on individual coroutines, this will lead to sequential behavior, since await starts the coroutine execution and waits for its finish,which is not the intended use-case for laziness. The use-case for async(start = CoroutineStart.LAZY) is a replacement for the standard lazy function in cases when computation of the value involves suspending functions.

## Naming coroutines for debugging
```kotlin
import kotlinx.coroutines.*

fun log(msg: String) = println("[${Thread.currentThread().name}] $msg")

fun main() = runBlocking(CoroutineName("main")) {
    log("Started main coroutine")
    // run two background value computations
    val v1 = async(CoroutineName("v1coroutine")) {
        delay(500)
        log("Computing v1")
        252
    }
    val v2 = async(CoroutineName("v2coroutine")) {
        delay(1000)
        log("Computing v2")
        6
    }
    log("The answer for v1 / v2 = ${v1.await() / v2.await()}")    
}

// check the result
//[main @main#1] Started main coroutine
//[main @v1coroutine#2] Computing v1
//[main @v2coroutine#3] Computing v2
//[main @main#1] The answer for v1 / v2 = 42
```

## combining context elements
```kotlin
import kotlinx.coroutines.*

fun main() = runBlocking<Unit> {
    launch(Dispatchers.Default + CoroutineName("test")) {
        println("I'm working in thread ${Thread.currentThread().name}")
    }    
}
```

## Coroutine scope
Launches a new coroutine without blocking the current thread and returns a reference to the coroutine as a Job. The coroutine is cancelled when the resulting job is cancelled.

The coroutine context is inherited from a CoroutineScope. Additional context elements can be specified with context argument. If the context does not have any dispatcher nor any other ContinuationInterceptor, then Dispatchers.Default is used.
```kotlin
// fun CoroutineScope.launch(context: CoroutineContext = EmptyCoroutineContext, start: CoroutineStart = CoroutineStart.DEFAULT, block: suspend CoroutineScope.() -> Unit): Job

import kotlinx.coroutines.*

class Activity {
    private val mainScope = CoroutineScope(Dispatchers.Default) // use Default for test purposes
    
    fun destroy() {
        mainScope.cancel()
    }

    fun doSomething() {
        // launch ten coroutines for a demo, each working for a different time
        repeat(10) { i ->
            mainScope.launch {
                delay((i + 1) * 200L) // variable delay 200ms, 400ms, ... etc
                println("Coroutine $i is done")
            }
        }
    }
} // class Activity ends

fun main() = runBlocking<Unit> {
    val activity = Activity()
    activity.doSomething() // run test function
    println("Launched coroutines")
    delay(500L) // delay for half a second
    println("Destroying activity!")
    activity.destroy() // cancels all coroutines
    delay(1000) // visually confirm that they don't work    
}
```

## flow
collection is different from sequence, and flow is aynsc sequence.
```
// 启动协程
GlobalScope.launch {
    // 构建流
    flow { // 定义流如何生产数据
        (1 .. 3).forEach {
            // 每隔 1 秒发射 1 个数字
            delay(1000)
            emit(it)
        }
    }.collect { // 定义如何消费数据
        Log.v("test", "num=$it") // 打印数字
    }
}
```

## Flow cancellation
# Timeout
```fun simple(): Flow<Int> = flow { 
    for (i in 1..3) {
        delay(100)          
        println("Emitting $i")
        emit(i)
    }
}

fun main() = runBlocking<Unit> {
    withTimeoutOrNull(250) { // Timeout after 250ms 
        simple().collect { value -> println(value) } 
    }
    println("Done")
}
```
# ensureActive check
the flow builder performs additional ensureActive checks for cancellation on each emitted value. It means that a busy loop emitting from a flow { ... } is cancellable:
```
fun foo(): Flow<Int> = flow { 
    for (i in 1..5) {
        println("Emitting $i") 
        emit(i) 
    }
}

fun main() = runBlocking<Unit> {
    foo().collect { value -> 
        if (value == 3) cancel()  
        println(value)
    } 
}
```
However, most other flow operators do not do additional cancellation checks on their own for performance reasons. For example, if you use IntRange.asFlow extension to write the same busy loop and don't suspend anywhere, then there are no checks for cancellation
```kotlin
fun main() = runBlocking<Unit> {
    (1..5).asFlow().collect { value -> 
        if (value == 3) cancel()  
        println(value)
    } 
}
//1
//2
//3
//4
//5
//Exception in thread "main" kotlinx.coroutines.JobCancellationException: BlockingCoroutine was cancelled; job="coroutine#1":BlockingCoroutine{Cancelled}@3327bd23

```
All numbers from 1 to 5 are collected and cancellation gets detected only before return from runBlocking. In the case where you have a busy loop with coroutines you must explicitly check for cancellation. You can add .onEach { currentCoroutineContext().ensureActive() }, but there is a ready-to-use cancellable operator provided to do that:
```kotlin
fun main() = runBlocking<Unit> {
    (1..5).asFlow().cancellable().collect { value -> 
        if (value == 3) cancel()  
        println(value)
    } 
}
```

## Transform operator
It can be used to imitate simple transformations like map and filter, as well as implement more complex transformations. Using the transform operator, we can emit arbitrary values an arbitrary number of times.
```kotlin
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.*

suspend fun performRequest(request: Int): String {
    delay(1000) // imitate long-running asynchronous work
    return "response $request"
}

fun main() = runBlocking<Unit> {
    (1..2).asFlow() // a flow of requests
        .transform { request ->
            emit("Making request $request")
            emit(performRequest(request)) 
        }
        .collect { response -> println(response) }
}
```

## size-limiting operator
```kotlin
fun numbers(): Flow<Int> = flow {
    try {                          
        emit(1)
        emit(2) 
        println("This line will not execute")
        emit(3)    
    } finally {
        println("Finally in numbers")
    }
}

fun main() = runBlocking<Unit> {
    numbers() 
        .take(2) // take only the first two
        .collect { value -> println(value) }
}            
```

## Terminal operators
```kotlin
val sum = (1..5).asFlow()
    .map { it * it } // squares of numbers from 1 to 5                           
    .reduce { a, b -> a + b } // sum them (terminal operator)
println(sum)
```
Besides above there are `toList` `toSet` `first` `reduce` & `fold` to use
```kotlin
val numbers = listOf(5, 2, 10, 4)

val sum = numbers.reduce { sum, element -> sum + element }
println(sum)
// 21
val sumDoubled = numbers.fold(0) { sum, element -> sum + element * 2 }
println(sumDoubled)
// 42
```
Reduce uses the first and the second elements as operation arguments on the first step.<br>
Fold takes an initial value and uses it as the accumulated value on the first step.

## flowOn
the long-running CPU-consuming code might need to be executed in the context of Dispatchers.Default and UI-updating code might need to be executed in the context of Dispatchers.Main. Usually, withContext is used to change the context in the code using Kotlin coroutines, but code in the flow { ... } builder has to honor the context preservation property and is not allowed to emit from a different context
<br>
The exception refers to the flowOn function that shall be used to change the context of the flow emission. The correct way to change the context of a flow is shown in the example below, which also prints the names of the corresponding threads to show how it all works
```kotlin
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.*

fun log(msg: String) = println("[${Thread.currentThread().name}] $msg")
           
fun simple(): Flow<Int> = flow {
    for (i in 1..3) {
        Thread.sleep(100) // pretend we are computing it in CPU-consuming way
        log("Emitting $i")
        emit(i) // emit next value
    }
}.flowOn(Dispatchers.Default) // RIGHT way to change context for CPU-consuming code in flow builder

fun main() = runBlocking<Unit> {
    simple().collect { value ->
        log("Collected $value") 
    } 
}            

//[DefaultDispatcher-worker-1 @coroutine#2] Emitting 1
//[main @coroutine#1] Collected 1
//[DefaultDispatcher-worker-1 @coroutine#2] Emitting 2
//[main @coroutine#1] Collected 2
//[DefaultDispatcher-worker-1 @coroutine#2] Emitting 3
//[main @coroutine#1] Collected 3       
```
flowOn operator has changed the default sequential nature of the flow. Now collection happens in one coroutine ("coroutine#1") and emission happens in another coroutine ("coroutine#2") that is running in another thread concurrently with the collecting coroutine. The flowOn operator creates another coroutine for an upstream flow when it has to change the CoroutineDispatcher in its context.


## buffering

We can use a buffer operator on a flow to run emitting code of the simple flow `concurrently` with collecting code, as opposed to running them sequentially
```kotlin
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.*
import kotlin.system.*

fun log(msg: String) = println("[${Thread.currentThread().name}] $msg")
fun simple(): Flow<Int> = flow {
    for (i in 1..3) {
        delay(100) // pretend we are asynchronously waiting 100 ms
        log("Emitting $i")
        emit(i) // emit next value
    }
}

fun main() = runBlocking<Unit> { 
    val time = measureTimeMillis {
        // without using buffer(), all happens in 1 thread
        simple().buffer().collect { value -> 
            delay(300) // pretend we are processing it for 300 ms
            log("collecting $value")
            println(value) 
        } 
    }   
    println("Collected in $time ms")
}
//[main @coroutine#2] Emitting 1
//[main @coroutine#2] Emitting 2
//[main @coroutine#2] Emitting 3
//[main @coroutine#1] collecting 1
//1
//[main @coroutine#1] collecting 2
//2
//[main @coroutine#1] collecting 3
//3
//Collected in 1046 ms
```

## conflate
Conflates flow emissions via conflated channel and runs collector in a separate coroutine. The effect of this is that emitter is never suspended due to a slow collector, but collector always gets the most recent value emitted
```kotlin
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.*
import kotlin.system.*

fun simple(): Flow<Int> = flow {
    for (i in 1..3) {
        delay(100) // pretend we are asynchronously waiting 100 ms
        emit(i) // emit next value
    }
}

fun main() = runBlocking<Unit> { 
    val time = measureTimeMillis {
        simple()
            .conflate() // conflate emissions, don't process each one
            .collect { value -> 
                delay(300) // pretend we are processing it for 300 ms
                println(value) 
            } 
    }   
    println("Collected in $time ms")
}
```
Note that conflate operator is a shortcut for buffer with capacity of Channel.CONFLATED, with is, in turn, a shortcut to a buffer that only keeps the latest element as created by buffer(onBufferOverflow = BufferOverflow.DROP_OLDEST)

## zip
```kotlin
val nums = (1..3).asFlow() // numbers 1..3
val strs = flowOf("one", "two", "three") // strings 
nums.zip(strs) { a, b -> "$a -> $b" } // compose a single string
    .collect { println(it) } // collect and print
```

## combine
onEach() returns a flow that invokes the given actionbefore each value of the upstream flow is emitted downstream.

```kotlin

val nums = (1..3).asFlow().onEach { delay(300) } // numbers 1..3 every 300 ms
val strs = flowOf("one", "two", "three").onEach { delay(400) } // strings every 400 ms
val startTime = System.currentTimeMillis() // remember the start time 
nums.zip(strs) { a, b -> "$a -> $b" } // compose a single string with "zip"
    .collect { value -> // collect and print 
        println("$value at ${System.currentTimeMillis() - startTime} ms from start") 
    } 
/* 
1 -> one
2 -> two
3 -> three
*/


val nums = (1..3).asFlow().onEach { delay(300) } // numbers 1..3 every 300 ms
val strs = flowOf("one", "two", "three").onEach { delay(400) } // strings every 400 ms          
val startTime = System.currentTimeMillis() // remember the start time 
nums.combine(strs) { a, b -> "$a -> $b" } // compose a single string with "combine"
    .collect { value -> // collect and print 
        println("$value at ${System.currentTimeMillis() - startTime} ms from start") 
    } 
/*
1 -> one at 452 ms from start
2 -> one at 651 ms from start
2 -> two at 854 ms from start
3 -> two at 952 ms from start
3 -> three at 1256 ms from start
*/
```

## Flattening flows
```kotlin
fun requestFlow(i: Int): Flow<String> = flow {
    emit("$i: First")
    delay(500) // wait 500 ms
    emit("$i: Second")
}
(1..3).asFlow().map { requestFlow(it) }
```
Then we end up with a flow of flows (Flow<Flow<String>>) that needs to be flattened into a single flow for further processing

## flatMapConcat
wait for the inner flow to complete before starting to collect the next one as the following example shows
```kotlin
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.*

fun requestFlow(i: Int): Flow<String> = flow {
    emit("$i: First") 
    delay(500) // wait 500 ms
    emit("$i: Second")    
}

fun main() = runBlocking<Unit> { 
    val startTime = System.currentTimeMillis() // remember the start time 
    (1..3).asFlow().onEach { delay(100) } // a number every 100 ms 
        .flatMapConcat { requestFlow(it) }                                                                           
        .collect { value -> // collect and print 
            println("$value at ${System.currentTimeMillis() - startTime} ms from start") 
        } 
}
/*
1: First at 121 ms from start
1: Second at 622 ms from start
2: First at 727 ms from start
2: Second at 1227 ms from start
3: First at 1328 ms from start
3: Second at 1829 ms from start
*/
```

## flatMapMerge
concurrently collect all the incoming flows and merge their values into a single flow so that values are emitted as soon as possible.
```kotlin
val startTime = System.currentTimeMillis() // remember the start time 
(1..3).asFlow().onEach { delay(100) } // a number every 100 ms 
    .flatMapMerge { requestFlow(it) }                                                                           
    .collect { value -> // collect and print 
        println("$value at ${System.currentTimeMillis() - startTime} ms from start") 
    } 
/*
1: First at 136 ms from start
2: First at 231 ms from start
3: First at 333 ms from start
1: Second at 639 ms from start
2: Second at 732 ms from start
3: Second at 833 ms from start
*/
```



+++1
---1
---1
---1
+++2
---2
---2
---2
+++3
---3
---3
---3
+++4
///1
---4
---4
---4