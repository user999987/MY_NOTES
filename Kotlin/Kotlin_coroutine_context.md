```kotlin
fun main(){
    val scope = CoroutineScope(CoroutineName("Coroutine-Name") + Dispatchers.IO)
    val job = scope.launch(start = CoroutineStart.DEFAULT){
        println("hello world")
    }
    //进程保活1s，只有进程存活的前提下，协程才能会启动和执行
    Thread.sleep(1000)
}
```
上面首先构造了一个CoroutineScope，它是协程的作用域，用于控制协程的生命周期，构造CoroutineScope需要一个CoroutineContext，它是协程的上下文，用于提供协程启动和运行时需要的信息.<br>
最后通过CoroutineScope的launch方法启动协程并输出hello world，其中启动协程时可以通过CoroutineStart指定协程的启动模式，它是一个枚举值，默认是立即启动，也通过指定CoroutineStart.LAZY变为延迟启动，延迟启动需要你主动调用返回的Job对象的start方法后协程才会启动，如果我们想取消掉这个协程的执行就可以调用CoroutineScope的cancel方法，或者调用launch方法返回的Job对象的cancel方法，其实CoroutineScope的cancel方法内部也是调用返回的Job对象的cancel方法来结束这个协程。<br>
上面就是启动一个协程的简单步骤，需要用到CoroutineScope、CoroutineContext、CoroutineStart。


## CoroutineContext

### Job
构造CoroutineScope使用到的CoroutineContext是一个特殊的集合，这个集合它既有Map的特点，也有Set的特点，集合的每一个元素都是Element，每个Element都有一个Key与之对应，对于相同Key的Element是不可以重复存在的，Element之间可以通过 + 号组合起来
CoroutineContext主要由以下4个Element组成：

* Job：协程的唯一标识，用来控制协程的生命周期(new、active、completing、completed、cancelling、cancelled)；
* CoroutineDispatcher：指定协程运行的线程(IO、Default、Main、Unconfined);
* CoroutineName: 指定协程的名称，默认为coroutine;
* CoroutineExceptionHandler: 指定协程的异常处理器，用来处理未捕获的异常.
  
Job提供了isActive、isCancelled、isCompleted属性来供外部判断协程是否处于Active、Cancelled、Completed状态<br>
协程中有两种类型的Job，如果我们平时启动协程时没有特意地通过CoroutineContext指定一个Job，那么使用launch/async方法启动协程时返回的Job它会产生异常传播. 启动一个协程1，在协程中继续启动协程2、协程3，那么协程1就是协程2、协程3的父协程，协程2、协程3就是协程1的子协程，每个协程都会有一个对应的Job. <br>
异常传播就是这个Job因为除了CancellationException以外的异常而失败时，那么父Job就会感知到并抛出异常，在抛出异常之前，父Job会取消所有子Job的运行, 如果要抑制这种异常传播的行为，那么可以用到另外一种类型的Job - SupervisorJob
```kotlin
fun main(){
     val parentJob = GlobalScope.launch {
       //childJob是一个SupervisorJob
        val childJob = launch(SupervisorJob()){
            throw NullPointerException()
        }
        childJob.join()
        println("parent complete")
    }
    Thread.sleep(1000)
}
```
childJob抛出异常并不会影响parentJob的运行，parentJob会继续运行并输出parent complete

### CoroutineDispatcher
CoroutineDispatcher可以指定协程的运行线程，CoroutineDispatcher里面有一个dispatch方法，这个dispatch方法用于把协程任务分派到特定线程运行，kotlin已经内置了CoroutineDispatcher的4个实现，可以通过Dispatchers的Default、IO、Main、Unconfined字段分别返回使用<br>
#### Default&IO
当你为协程指定Dispatchers.Default时，Dispatcher会把协程的任务指定为CPU密集型任务，对应mode为TASK_NON_BLOCKING，当你为协程指定Dispatchers.IO时，Dispatcher会把协程的任务指定为IO密集型任务，对应mode为TASK_PROBABLY_BLOCKING，所以这时CoroutineScheduler就可以根据task mode作出不同的线程创建、调度、唤醒策略，当启动协程时没有指定Dispatcher，默认会使用Dispatchers.Default。
#### Unconfined
Dispatchers.Unconfined的含义是不给协程指定运行的线程，在第一次被挂起(suspend)之前，由启动协程的线程执行它，但被挂起后, 会由恢复协程的线程继续执行,  如果一个协程会被挂起多次,  那么每次被恢复后,  都有可能被不同线程继续执行<br>
Dispatchers.Unconfined的含义是不给协程指定运行的线程，在第一次被挂起(suspend)之前，由启动协程的线程执行它，但被挂起后, 会由恢复协程的线程继续执行,  如果一个协程会被挂起多次,  那么每次被恢复后,  都有可能被不同线程继续执行
```kotlin
internal abstract class EventLoop : CoroutineDispatcher() {
  
  //...
  
  private var unconfinedQueue: ArrayQueue<DispatchedTask<*>>? = null
  
  public fun dispatchUnconfined(task: DispatchedTask<*>) {
        val queue = unconfinedQueue ?: ArrayQueue<DispatchedTask<*>>().also { unconfinedQueue = it }
        queue.addLast(task)
  }
  
  public fun processUnconfinedEvent(): Boolean {
        val queue = unconfinedQueue ?: return false
        val task = queue.removeFirstOrNull() ?: return false
        task.run()
        return true
  }
}
```
在kotlin中每个协程都有一个Continuation实例与之对应，当协程恢复时会调用Continuation的resumeWith方法<br>
EventLoop中有一个双端队列用于存放Unconfined任务，Unconfined任务是指指定了Dispatchers.Unconfined的协程任务，EventLoop的dispatchUnconfined方法用于把Unconfined任务放进队列的尾部，processUnconfinedEvent方法用于从队列的头部移出Unconfined任务执行，所以executeUnconfined方法里面的策略就是：在当前线程立即执行Unconfined任务，如果当前线程已经在执行Unconfined任务，就暂时把它放进跟当前线程关联的EventLoop中，等待执行，同时Unconfined任务里面会调用Continuation的resumeWith方法恢复协程运行，这也是为什么指定了Dispatchers.Unconfined后协程恢复能够被恢复协程的线程执行的原因

#### Main
Dispatchers.Main的含义是把协程运行在平台相关的只能操作UI对象的Main线程，所以它根据不同的平台有不同的实现，kotlin它支持下面三种平台
* kotlin/js：kotlin/js是kotlin对JavaScript的支持，提供了转换kotlin代码，kotlin标准库的能力，npm包管理能力，在kotlin/js上Dispatchers.Main等效于Dispatchers.Default；
* kotlin/native：kotlin/native是一种将kotlin代码编译为无需虚拟机就可运行的原生二进制文件的技术, 它的主要目的是允许对不需要或不可能使用虚拟机的平台进行编译，例如嵌入式设备或iOS，在kotlin/native上Dispatchers.Main等效于Dispatchers.Default；
* kotlin/JVM：kotlin/JVM就是需要虚拟机才能编译的平台，例如Android就是属于kotlin/JVM，对于kotlin/JVM我们需要引入对应的dispatcher，例如Android就需要引入kotlinx-coroutines-android库，它里面有Android对应的Dispatchers.Main实现，其实就是把任务通过Handler运行在Android的主线程.

### CoroutineName
CoroutineName就是协程的名字，它的结构很简单, 我们平时开发一般是不会去指定一个CoroutineName的，因为CoroutineName只在kotlin的调试模式下才会被用的, 它在debug模式下被用于设置协程运行线程的名字

### CoroutineExceptionHandler
CoroutineExceptionHandler就是协程的异常处理器，用来处理协程运行中未捕获的异常，每一个创建的协程默认都会有一个异常处理器，我们可以在启动协程时通过CoroutineContext指定我们自定义的异常处理器，我们可以通过CoroutineExceptionHandler方法创建一个CoroutineExceptionHandler，它会返回一个CoroutineExceptionHandler的默认实现，默认实现的handleException方法中调用了我们传进的handler方法<br>
CoroutineExceptionHandler只对launch方法启动的根协程有效，而对async启动的根协程无效，因为async启动的根协程默认会捕获所有未捕获异常并把它放在Deferred中，等到用户调用Deferred的await方法才抛出<br>
还有子协程抛出的未捕获异常会委托父协程的CoroutineExceptionHandler处理，子协程设置的CoroutineExceptionHandler永远不会生效(SupervisorJob 除外)，如下
```kotlin
fun main(){
    //根协程的Handler
    val parentHandler = CoroutineExceptionHandler{coroutineContext, throwable ->
        println("parent coroutineExceptionHandler catch exception, msg = ${throwable.message}")
    }
    //启动根协程
    val parentJob = GlobalScope.launch(parentHandler){
        //子协程的Handler
        val childHandler = CoroutineExceptionHandler{coroutineContext, throwable ->
            println("child coroutineExceptionHandler catch exception, msg = ${throwable.message}")
        }
        //启动子协程
        val childJob = launch(childHandler){
            throw IndexOutOfBoundsException("exception thrown from child launch")
        }
        childJob.start()
    }
    parentJob.start()
    
    Thread.sleep(1000)
}

输出：
parent coroutineExceptionHandler catch exception, msg = exception thrown from child launch
```
可以看到子协程设置CoroutineExceptionHandler没有输出，只有根协程的CoroutineExceptionHandler输出了，但是也有例外，如果子协程是SupervisorJob，那么它设置的CoroutineExceptionHandler是生效的，前面也说过SupervisorJob不会产生异常传播
<br>
当父协程的子协程同时抛出多个异常时，CoroutineExceptionHandler只会捕获第一个协程抛出的异常，后续协程抛出的异常被保存在第一个异常的suppressed数组中

```kotlin
fun main(){
    val handler = CoroutineExceptionHandler{coroutineContext, throwable ->
        println("my coroutineExceptionHandler catch exception, msg = ${throwable.message}, suppressed = ${throwable.suppressed.contentToString()}")
    }
    val parentJob = GlobalScope.launch(handler){
        launch {
            try {
                delay(200)
            }finally {
                //第二个抛出的异常
                throw IndexOutOfBoundsException("exception thrown from first child launch")
            }
        }.start()

        launch {
            delay(100)
            //第一个抛出的异常
            throw NullPointerException("exception thrown from second child launch")
        }.start()
    }
    parentJob.start()

    Thread.sleep(1000)
}

输出：
my coroutineExceptionHandler catch exception, msg = exception thrown from second child launch, suppressed = [java.lang.IndexOutOfBoundsException: exception thrown from first child launch]
```
可以看到CoroutineExceptionHandler只处理了第一个子协程抛出的异常，后续异常都放在了第一个抛出异常的suppressed数组中。
还有取消协程时会抛出一个CancellationException，它会被所有CoroutineExceptionHandler省略，但可以try catch它，同时当子协程抛出CancellationException时，并不会终止当前父协程的运行
