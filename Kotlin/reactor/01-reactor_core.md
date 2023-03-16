# Reactive Programming is programming with asynchronous data streams
When using reactive programming, data streams are going to be the spine of your application. Events, messages, calls, and even failures are going to be conveyed by a data stream. With reactive programming, you observe these streams and react when a value is emitted.

In order for an application to be reactive, the first thing it must be able to do is to produce a stream of data.

This could be something like the stock update example that we gave earlier. Without this data, we wouldn't have anything to react to, which is why this is a logical first step.

Reactive Core gives us two data types that enable us to do this:
1. Flux
2. Mono
```kotlin
import org.reactivestreams.Subscriber
import org.reactivestreams.Subscription
import reactor.core.publisher.Flux

val elemetns: MutableList<Int> = mutableListOf()
// to better understand what's happening let's provide a Subscriber interface directly
Flux.just(1, 2, 3, 4)
    .log()
    .subscribe(object : Subscriber<Int> {
        override fun onComplete() {}

        override fun onError(t: Throwable?) {}

        override fun onNext(t: Int) {
            elemetns.add(t)
        }

        override fun onSubscribe(s: Subscription?) {
            s?.request(Long.MAX_VALUE)
        }
    })
// equvalient to

Flux.just(1, 2, 3, 4)
    .log()
    .subscribe(elements::add)
```
```shell
13:22:22.262 [main] DEBUG reactor.util.Loggers - Using Slf4j logging framework
13:22:22.271 [main] INFO reactor.Flux.Array.1 - | onSubscribe([Synchronous Fuseable] FluxArray.ArraySubscription)
13:22:22.273 [main] INFO reactor.Flux.Array.1 - | request(unbounded)
13:22:22.273 [main] INFO reactor.Flux.Array.1 - | onNext(1)
13:22:22.273 [main] INFO reactor.Flux.Array.1 - | onNext(2)
13:22:22.273 [main] INFO reactor.Flux.Array.1 - | onNext(3)
13:22:22.273 [main] INFO reactor.Flux.Array.1 - | onNext(4)
13:22:22.274 [main] INFO reactor.Flux.Array.1 - | onComplete()
```

1. onSubscribe() – This is called when we subscribe to our stream
2. request(unbounded) – When we call subscribe, behind the scenes we are creating a Subscription. This subscription requests elements from the stream. In this case, it defaults to unbounded, meaning it requests every single element available
3. onNext() – This is called on every single element
4. onComplete() – This is called last, after receiving the last element. There's actually a onError() as well, which would be called if there is an exception, but in this case, there isn't

```kotlin
Flux.just(1, 2, 3, 4,5,6,7,8,9)
        .log()
        .subscribe(object : Subscriber<Int>{
            private var s: Subscription? = null
            var onNextAmount = 0

            override fun onSubscribe(s: Subscription) {
                this.s = s
                this.s?.request(1)
            }

            override fun onNext(integer: Int) {
                elemetns.add(integer)
                onNextAmount++
                if (onNextAmount == 1 ){
                //if (onNextAmount % 2 == 0) {
                    this.s?.request(2)
                }
            }

            override fun onError(t: Throwable?) {}

            override fun onComplete() {}
        })
```
```
23:31:15.395 [main] INFO  reactor.Flux.Array.1 - | onSubscribe([Synchronous Fuseable] FluxArray.ArraySubscription)
23:31:15.397 [main] INFO  reactor.Flux.Array.1 - | request(2)
23:31:15.397 [main] INFO  reactor.Flux.Array.1 - | onNext(1)
23:31:15.398 [main] INFO  reactor.Flux.Array.1 - | onNext(2)
23:31:15.398 [main] INFO  reactor.Flux.Array.1 - | request(2)
23:31:15.398 [main] INFO  reactor.Flux.Array.1 - | onNext(3)
23:31:15.398 [main] INFO  reactor.Flux.Array.1 - | onNext(4)
23:31:15.398 [main] INFO  reactor.Flux.Array.1 - | request(2)
23:31:15.398 [main] INFO  reactor.Flux.Array.1 - | onComplete()
```
Now if we run our code again, we'll see the request(2) is called, followed by two onNext() calls, then request(2) again.<br>
Essentially, this is reactive pull backpressure. We are requesting the upstream to only push a certain amount of elements, and only when we are ready.

## Hot Stream
```kotlin
val pub = Flux.create<Any> { fluxSink ->
        while(true){
            fluxSink.next(System.currentTimeMillis())
        }
    }.publish()

    pub.subscribe{i-> println(i)}
    pub.subscribe{i-> println(i)}
    pub.connect()
```
有时候，你不仅想要在某一个订阅者订阅之后才开始发出数据，可能还希望在多个订阅者“到齐”之后 才开始。ConnectableFlux的用意便在于此。Flux API 中有两种常用的返回ConnectableFlux 的方式：publish和replay。

1. publish会尝试满足各个不同订阅者的需求（也就是回压），并综合这些请求反馈给源。假设有某个订阅者的需求为 0，发布者会暂停向所有订阅者发出元素。
2. replay将对第一个订阅后产生的数据进行缓存，最多缓存数量取决于配置（时间/缓存大小）。 它会对后续接入的订阅者重新发送数据。
ConnectableFlux提供了多种对订阅的管理方式。包括：

* connect，当有足够的订阅接入后，可以对 flux 手动执行一次。它会触发对上游源的订阅。
* autoConnect(n)与connect类似，不过是在有 n 个订阅的时候自动触发。
* refCount(n)不仅能够在订阅者接入的时候自动触发，还会检测订阅者的取消动作。如果订阅者全部取消订阅，则会将源“断开连接”，再有新的订阅者接入的时候才会继续“连上”发布者。refCount(int, Duration)增加了一个倒计时：一旦订阅者数量太低了，它会等待 Duration 参数指定的时间，如果没有新的订阅者接入才会与源断开连接。

```kotlin
val pub = Flux.create<Any> { fluxSink ->
        while(true){
            fluxSink.next(System.currentTimeMillis())
        }
    }.sample(Duration.ofSeconds(2)).publish()

    pub.subscribe{i-> println(i)}
    pub.subscribe{i-> println(i)}
    pub.connect()
```
Values will only be pushed to our subscriber every two seconds, there are multiple strategies to reduce the amount of data sent downstream, such as windowing and buffering,