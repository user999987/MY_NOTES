GoRoutine Schedules goroutines inside an operating system thread

Race Condition\
Behavior is dependent on the sequence or timing of other uncontrollable events


One Goroutine is always created automatically to execute the main()

```go
a = 1
foo()
a=2
// main goroutine blocks on call to foo()
```

```go
a=1
go foo()
// create a new goroutine for foo()
a=2
// main goroutine does not block
```

A goroutine exits when its code is complete. However, when main goroutine is complete, all other goroutines will be forced to end and exit.

Synchronization Example
```
Task1
x=1
x=x+1
GLOBAL EVENT

Task2
if GLOBAL EVENT
    print x
```
Every time we use synchronization, we are reducing the efficiency, we are reducing the amount of possible concurrency.

sync.WaitGroup contains an internal counter:
* increment counter for each goroutine to wait for (sync.WaitGroup.Add())
* decrement counter when each goroutine completes (sync.WaitGroup.Done())
* waiting goroutine unitil counter is 0 (sync.WaitGroup.Wait())

```go
func foo(wg *sync.WaitGroup){
    defer wg.Done()
    //Go 语言的 defer 会在当前函数返回前执行传入的函数，它会经常被用于关闭文件描述符、关闭数据库连接以及解锁资源
    fmt.Printf("New routine")
    
}

func main(){
    var wg sync.WaitGroup
    wg.Add(1)
    go foo (&wg)
    wg.Wait()
    fmt.Printf("Main routine")
}
```

Channel Example
```go
func prod(v1 int, v2 int, c chan int){
    c <- v1*v2
}
func main(){
    c:=make(chan int)
    go prod(1,2,c)
    go prod(3,4,c)
    a:=<-c
    b:=<-c
    fmt.Println(a*b)
}
```

Blocking and Synchronization
```
Task1
c<-3

Task2
<-c
```
This way it will act as sync.WaitGroup

Channel Capacity (buffered channle)
```go
c:=make(chan int, 3)
// 3 is capacity of channel c that it can hold in transit
// Sending only blocks if buffer is full
// Receiving only blocks if buffer is empty
```

Iterating through channel
```go
for i := range c{
    fmt.Println(i)
}
//need close(c) otherwise it will run forever
```

Select on channel
```go
select {
    case a = <-c1:
        fmt.Println(a)
    case b=<-c2:
        fmt.Println(b)
}
// first come first serve

select{
    case a=<-inchan:
        fmt.Println("received a")
    case outchan <-b:
        fmt.Println("sent b")
    default:
        fmt.Println("nop")
        // when has default do not block at all
}
```
Select with an Abort Channel</br>
Use select with a separate abort channel
```go
for {
    select{
        case a<-c:
            fmt.Println(a)
        case <-abort:
            return
    }
}
```

sync.Mutex
```go
i:=0
var mut sync.Mutex
func inc(){
    mut.Lock()
    i = i+1
    mut.Unlock()
}
```

Perform initialization with multiple goroutines?
1. perform initialization before starting the goroutines
2. sync.Once.Do()
```go
var wg sync.WaitGroup
var on sync.Once

func setup(){
    fmt.Println("init")
}

func dostuff(){
    on.Do(setup)
    fmt.Println("hello")
    wg.Done()
}

func main(){
    wg.Add(2)
    go destuff()
    go dostuff()
    wg.Wait()
}

// output will be 
// init
// hello
// hello
```