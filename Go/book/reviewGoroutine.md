### Goroutine
Goroutine - concurrently executing activity. \
### Channels
How goroutines communicate with each other? Channels!\
A channel is a communication mechanism that lets one goroutine send values to another goroutine. \
In essential, channel is a struct.
As with maps, a channel is a reference to the data structure created by make. When we copy a channel or pass one as an argument to a function, we are copying a reference, so caller and callee refer to the same structure. Zero value of a channel is `nil`.

Channel has 2 principal operations send/receive
```go
ch <- x // send statement
x = <- ch // receive expression in an assignment 
<- ch // receive statement, result is discarded
```
Close operation, sets a flag indicating that no more values will ever be sent on this channel; 
1. subsequent attempts to send will panic.
2. Receive operations on a closed channel yield the values that have been sent until no more values are left, any receive operations thereafter complete immediately and yield the zero value of the channel's element type.
There is no way to test directly whether a channel has been closed, but there is a variant of the receive operation that produces two results: the received channel element, plus a boolean value, conventionally called ok, which is true for a successful receive and false for a receive on a closed and drained channel.
```go
go func() {
    for {
        x, ok := <-naturals
        if !ok {
            break // channel was closed and drained
        }
        squares <- x * x
    }
    close(squares)
}()
```

```go
close(ch)
ch = make(chan int) // unbuffered channel
ch = make(chan int, 0) // unbuffered channel
ch = make(chan int, 3) // buffered channel with capacity
```
A send operation on an unbuffered channel blocks the sending goroutine until another goroutine executes a corresponding receive on the same channel, at which point the value is transmitted and both goroutines may continue. Conversely, if the receive operation was attempted first, the receiving goroutine is blocked until another goroutine performs a send on the same channel\
Communication over an unbuffered channel causes the sending and receiving goroutines to synchronize.\
For above purpose, we can declare chan as `struct{}` then `done <- struct{}{}`

channel can be unidirectional which means read-only or receive-only
```go
var ch chan<- int // receive only
var ch <-chan int // send only
```
你可以这么声明 但是没这么用的 如果这么定义channel要死锁了. 正常情况是
```go
func foo(ch chan<- int)
func foo(ch <-chan int)
```
如此保证ch通道在函数内只能进行发或者收操作

### Select
专为channel设计, 每个case只能包含操作通道的表达式, 其默认为阻塞. 只有监听的channel中有发送或者接受数据时才运行. 设置default则不阻塞, 如果不设置default, 会有死锁风险.\
多个channel准备好时, 会随机选一个执行

### closure
```go
for _, f := range filenames {
    go func() {
        thumbnail.ImageFile(f) // NOTE: incorrect!
        // ...
    }()
}
```
上面这个单独的变量f是被所有的匿名函数值所共享，且会被连续的循环迭代所更新的。当新的goroutine开始执行字面函数时，for循环可能已经更新了f并且开始了另一轮的迭代或者（更有可能的）已经结束了整个循环，所以当这些goroutine开始读取f的值时，它们所看到的值已经是slice的最后一个元素了。显式地添加这个参数，我们能够确保使用的f是当go语句执行时的"当前"那个f。
```go
for _, f := range filenames {
    go func(f string) {
        thumbnail.ImageFile(f) // NOTE: incorrect!
        // ...
    }(f)
}
```
### 并发的退出
```go
var done = make(chan struct{})

func cancelled() bool {
    select {
    case <-done:
        return true
    default:
        return false
    }
}
```