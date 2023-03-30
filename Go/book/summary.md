
```go
     var cwd string
     func init() {
         var err error
         cwd, err = os.Getwd()
         if err != nil {
             log.Fatalf("os.Getwd failed: %v", err)
} }
```

A string is an immutable sequence of bytes. The i-th byte of a string is not necessarily the i-th character of a string, because the UTF-8 encoding of a non-ASCII code point requires two or more bytes

```go
var (
	mu      sync.Mutex // guards mapping
	mapping = make(map[string]string)
)

func Lookup(key string) string {
	mu.Lock()
	v := mapping[key]
	mu.Unlock()
	return v
}
// 上下等价 但是下面的用到了内嵌结构体的特性字结构的方法可以直接
// 被父结构体本身直接使用 本质身上是个语法糖 从实现角度来说 相当于
// 编译器生成了额外的代码 比如生成了 cache的 Lock方法 然后
// cache的 Lock 方法 调用了 sync.Mutex类型的Lock方法
var cache = struct {
	sync.Mutex
	mapping map[string]string
}{
	mapping: make(map[string]string),
}

func Lookup(key string) string {
	cache.Lock()
	v := cache.mapping[key]
	cache.Unlock()
	return v
}
```

```go
package io
type Reader interface {
    Read(p []byte) (n int, err error)
}
type Closer interface {
    Close() error
}
// 接口内嵌
type ReadWriter interface {
    Reader
    Writer 
}
type ReadWriter interface {
    Read(p []byte) (n int, err error)
    Write(p []byte) (n int, err error)
}
type ReadWriter interface {
    Read(p []byte) (n int, err error)
    Writer
}
// 上述3个 ReadWriter 等价
type ReadWriteCloser interface {
    Reader
    Writer
    Closer 
}
```

http.Handler interface
```go
package http
type Handler interface {
    ServeHTTP(w ResponseWriter, r *Request)
}
func ListenAndServe(address string, h Handler) error

//定义一个实现了ServeHTTP方法的结构体就可以放入ListenAndServe
type database map[string]dollars
func (db database) ServeHTTP(w http.ResponseWriter, req *http.Request) { switch req.URL.Path {
case "/list":
        for item, price := range db {
            fmt.Fprintf(w, "%s: %s\n", item, price)
        }
    case "/price":
        item := req.URL.Query().Get("item")
        price, ok := db[item]
        if !ok {
            w.WriteHeader(http.StatusNotFound) // 404
            fmt.Fprintf(w, "no such item: %q\n", item)
            return
}
        fmt.Fprintf(w, "%s\n", price)
    default:
        w.WriteHeader(http.StatusNotFound) // 404
        fmt.Fprintf(w, "no such page: %s\n", req.URL)
    }
}
// net/http provides ServeMux, a request multiplexer, to simplify the association between URLs and handlers
// A ServeMux aggregates a collection of http.Handlers into a single http.Handler
func main() {
    db := database{"shoes": 50, "socks": 5}
    mux := http.NewServeMux()
    mux.Handle("/list", http.HandlerFunc(db.list))
    mux.Handle("/price", http.HandlerFunc(db.price))
    log.Fatal(http.ListenAndServe("localhost:8000", mux))
}

func (db database) list(w http.ResponseWriter, req *http.Request) {
    for item, price := range db {
        fmt.Fprintf(w, "%s: %s\n", item, price)
    }
}

func (db database) price(w http.ResponseWriter, req *http.Request) {
    item := req.URL.Query().Get("item")
    price, ok := db[item]
    if !ok {
        w.WriteHeader(http.StatusNotFound) // 404
        fmt.Fprintf(w, "no such item: %q\n", item)
        return
}
    fmt.Fprintf(w, "%s\n", price)
}
// The expression http.HandlerFunc(db.list) is a conversion, not a function call, since http.HandlerFunc is a type.
// 本质就是把所有传入函数转换成 HandlerFunc 类型然后因为 HandlerFunc 实现了 ServeHTTP 所以可以放入mux.Handle 中 然后因为他的 ServeHTTP的实现 其实就是调用他自己接收到的函数 有点绕...

type HandlerFunc func(w ResponseWriter, r *Request)
func (f HandlerFunc) ServeHTTP(w ResponseWriter, r *Request) {
    f(w, r)
}

// how to understand above, take a look at below example
type Greeting func(name string) string

func (g Greeting) say(n string) {
    fmt.Println(g(n))
}

func english(name string) string {
    return "Hello, " + name
}

func french(name string) string {
    return "Bonjour, " + name
}

func main() {
    g := Greeting(english)
    g.say("World")
    g = Greeting(french)
    g.say("World")
}

// Because registering a handler this way is so common, ServeMux has a convenience method called HandleFunc that does it for us, so we can simplify the handler registration code to this:
mux.HandleFunc("/list", db.list)
mux.HandleFunc("/price", db.price)

// net/http provides a global ServeMux instance called DefaultServeMux and package-level functions called http.Handle and http.HandleFunc. To use Default- ServeMux as the server’s main handler, we needn’t pass it to ListenAndServe; nil will do
func main() {
    db := database{"shoes": 50, "socks": 5}
    http.HandleFunc("/list", db.list)
    http.HandleFunc("/price", db.price)
    log.Fatal(http.ListenAndServe("localhost:8000", nil))
}
// the web server invokes each handler in a new goroutine, so handlers must take precautions such as locking when accessing variables that other goroutines, including other requests to the same handler, may be access- ing
```

error interface
```go
// error interface is defined in builtin.go
type error interface {
    Error() string
}
// The entire errors package is only four lines long:
// the reason that the pointer type *errorString, not errorString alone, satisfies the error interface is so that every call to New allocates a distinct error instance that is equal to no other.
// Calls to errors.New are relatively infrequent because there’s a convenient wrapper function, fmt.Errorf, that does string formatting too
package errors

type errorString struct { text string }
func (e *errorString) Error() string { return e.text }
func New(text string) error { return &errorString{text} }
```

tcp example 
```go
// The Listen function creates a net.Listener, an object that listens for incoming connections on a network port, in this case TCP port localhost:8000. The listener’s Accept method blocks until an incoming connection request is made, then returns a net.Conn object rep- resenting the connection.
func main() {
	listener, err := net.Listen("tcp", "localhost:8000")

	if err != nil {
		log.Fatal(err)
	}
	for {
		conn, err := listener.Accept()
		fmt.Print("123")
		if err != nil {
			log.Print(err) // e.g., connection aborted
			continue
		}
		handleConn(conn) // handle one connection at a time
	}
}
```
Channel
```go 
for {
    x, ok := <-naturals
    if !ok {
        break // channel was closed and drained
    }
    squares <- x * x
}
close(squares)
// 有些啰嗦 下面是golang语法糖
// It’s only necessary to close a channel when it is important to tell the receiving goroutines that all data have been sent. A channel that the garbage collector determines to be unreachable will have its resources reclaimed whether or not it is closed.
for x := 0; x < 100; x++ {
    naturals <- x
}
close(naturals)

```
并发请求
```go
// It makes parallel requests to three mirrors, that is, equivalent but geographically distributed servers.
// In this particular case, the two remaining goroutines will continue to execute the request() function and send their responses to the channel, but since there is no one waiting to receive the messages from the channel, the messages will be discarded. Once the goroutines finish their work, they will exit automatically.
// Had we used an unbuffered channel, the two slower goroutines would have gotten stuck trying to send their responses on a channel from which no goroutine will ever receive. This sit- uation, called a goroutine leak, would be a bug. Unlike garbage variables, leaked goroutines are not automatically collected, so it is important to make sure that goroutines terminate them- selves when no longer needed.
func mirroredQuery() string {
    responses := make(chan string, 3)
    go func() { responses <- request("asia.gopl.io") }()
    go func() { responses <- request("europe.gopl.io") }()
    go func() { responses <- request("americas.gopl.io") }()
    return <-responses // return the quickest response
}
```

Looping in Parallel
```go
// NOTE: incorrect!
//  makeThumbnails returns before it has finished doing what it was supposed to do. It starts all the goroutines, one per file name, but doesn’t wait for them to finish.
func makeThumbnails2(filenames []string) {
    for _, f := range filenames {
        go thumbnail.ImageFile(f) // NOTE: ignoring errors
    }
}
// final version
// wg.Done() <==>wg.Add(-1)
func makeThumbnails6(filenames <-chan string) int64 {
	sizes := make(chan int64)
	var wg sync.WaitGroup // number of working goroutines
	for f := range filenames {
		wg.Add(1)
		// worker
		go func(f string) {
			defer wg.Done()
			thumb, err := thumbnail.ImageFile(f)
			if err != nil {
				log.Println(err)
				return
			}
			info, _ := os.Stat(thumb) // OK to ignore error
			sizes <- info.Size()
		}(f)
	}
	// closer
	go func() {
		wg.Wait()
		close(sizes)
	}()
	var total int64
	for size := range sizes {
		total += size
	}
	return total
}
```

Multiplex with Select
```go
func main() {
    fmt.Println("Commencing countdown.")
    tick := time.Tick(1 * time.Second)
    for countdown := 10; countdown > 0; countdown-- {
        fmt.Println(countdown)
        j<-tick 
    }
    launch() 
}

abort := make(chan struct{})
go func() {
    os.Stdin.Read(make([]byte, 1)) // read a single byte
    abort <- struct{}{}
}()
// Now each iteration of the countdown loop needs to wait for an event to arrive on one of the two channels: the ticker channel if everything is fine (‘‘nominal’’ in NASA jargon) or an abort event if there was an ‘‘anomaly.’’ We can’t just receive from each channel because whichever operation we try first will block until completion. We need to multiplex these operations, and to do that, we need a select statement
// A select waits until a communication for some case is ready to proceed. It then performs that communication and executes the case’s associated statements; the other communications do not happen. A select with no cases, select{}, waits forever.

ch := make(chan int, 1)
for i := 0; i < 10; i++ {
    select {
    case x := <-ch:
        fmt.Println(x) // "0" "2" "4" "6" "8"
    case ch <- i:
    } 
}
// 0的时候 0入ch
// 1 的时候 ch有东西 打印0
// 2 的时候 2入ch

// 无缓冲的通道 <==> 同步操作 
// 所以下面会变成死锁
ch := make(chan int) // 无缓冲的通道
for i := 0; i < 10; i++ {
    select {
    case x := <-ch:
        fmt.Println(x) // "0" "2" "4" "6" "8"
    case ch <- i:
    }
}
// Sometimes we want to try to send or receive on a channel but avoid blocking if the channel is not ready—a non-blocking communication. A select statement can do that too. A select may have a default, which specifies what to do when none of the other communications can proceed immediately.
select {
    case <-abort:
        fmt.Printf("Launch aborted!\n")
        return
    default:
// do nothing
}
// The zero value for a channel is nil. Because send and receive operations on a nil channel block forever, a case in a select statement whose channel is nil is never selected. This lets us use nil to enable or disable cases that cor- respond to features like handling timeouts or cancellation, responding to other input events, or emitting output

// The time.Tick function behaves as if it creates a goroutine that calls time.Sleep in a loop, sending an event each time it wakes up. When the countdown function above returns, it stops receiving events from tick, but the ticker goroutine is still there, trying in vain to send on a channel from which no goroutine is receiving—a goroutine leak 

func main() {
    // ...create abort channel...
    fmt.Println("Commencing countdown.  Press return to abort.")
    tick := time.Tick(1 * time.Second)
    for countdown := 10; countdown > 0; countdown-- {
        fmt.Println(countdown)
        select {
        case <-tick:
            // Do nothing.
        case <-abort:
            fmt.Println("Launch aborted!")
            return
        } 
    }
    launch() 
}

// The Tick function is convenient, but it’s appropriate only when the ticks will be needed throughout the lifetime of the application. Otherwise, we should use this pattern:
ticker := time.NewTicker(1 * time.Second)
<-ticker.C    // receive from the ticker's channel
ticker.Stop() // cause the ticker's goroutine to terminate
```

Stops a goroutine
1. Using a shared variable: One way to stop a goroutine is to use a shared variable that indicates whether the goroutine should continue running or stop. The goroutine can periodically check this variable and exit if it is set to a certain value. For example:
```go
var stop bool
var wg sync.WaitGroup

func main() {
    wg.Add(1)
    go foo()
    // Wait for some time before stopping the goroutine
    // Here, we wait for 5 seconds
    fmt.Println("Waiting for 5 seconds...")
    wg.Wait()
    stop = true
    fmt.Println("Stopped the goroutine")
}

func foo() {
    defer wg.Done()
    for {
        // Do some work
        fmt.Println("Working...")
        // Check if the stop variable is set
        if stop {
            fmt.Println("Stopping...")
            return
        }
    }
}
```
2. Using a channel: Another way to stop a goroutine is to use a channel to signal it to stop. The goroutine can wait for a value on the channel and exit if it receives a certain value. For example:
```go 

func main() {
    // Create a channel to signal the goroutine to stop
    stopCh := make(chan struct{})
    go foo(stopCh)
    // Wait for some time before stopping the goroutine
    // Here, we wait for 5 seconds
    fmt.Println("Waiting for 5 seconds...")
    time.Sleep(5 * time.Second)
    close(stopCh)
    fmt.Println("Stopped the goroutine")
}

func foo(stopCh <-chan struct{}) {
    for {
        // Do some work
        fmt.Println("Working...")
        // Wait for a value on the stop channel
        select {
        case <-stopCh:
            fmt.Println("Stopping...")
            return
        default:
            // Continue working
        }
    }
}
```

Close Channel
```go
// Behind the scenes, when a channel is closed in Go, the runtime sets an internal flag on the channel to indicate that it's closed. This flag is used to signal to any goroutines that are blocked on sending or receiving from the channel that the channel has been closed. When a goroutine tries to send a value on a closed channel, it will immediately panic. When a goroutine tries to receive a value from a closed channel, it will receive a zero value of the channel's element type, and the second return value of the receive operation will be false to indicate that the channel is closed.

```