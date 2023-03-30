```go
//As with maps, a channel is a reference to the data structure created by make. When we copy a channel or pass one as an argument to a function, we are copying a reference, so caller and callee refer to the same data structure. As with other reference types, the zero value of a chan- nel is nil.
ch : =make(chan int)
```

```go
ch <- x  // a send statement
x = <-ch // a receive expression in an assignment statement
<-ch     // a receive statement; result is discarded
```


```go
// A send operation on an unbuffered channel blocks the sending goroutine until another goroutine executes a corresponding receive on the same channel, at which point the value is transmitted and both goroutines may continue. Conversely, if the receive operation was attempted first, the receiving goroutine is blocked until another goroutine performs a send on the same channel.
// Communication over an unbuffered channel causes the sending and receiving goroutines to synchronize.
func main() {
    conn, err := net.Dial("tcp", "localhost:8000")
    if err != nil {
        log.Fatal(err)
    }
    done := make(chan struct{})
    go func() {
        io.Copy(os.Stdout, conn) // NOTE: ignoring errors
        log.Println("done")
        done <- struct{}{} // signal the main goroutine
    }()
    mustCopy(conn, os.Stdin)
    conn.Close()
    <-done // wait for background goroutine to finish
}
// Messages sent over channels have two important aspects. Each message has a value, but sometimes the fact of communication and the moment at which it occurs are just as important. We call messages events when we wish to stress this aspect. When the event car- ries no additional information, that is, its sole purpose is synchronization, we’ll emphasize this by using a channel whose element type is struct{}, though it’s common to use a channel of bool or int for the same purpose since done <- 1 is shorter than done <- struct{}{}.
```

```go
close(ch)
chval , ok := <-ch
if !ok{
    // do something
}


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
// the syntax above is clumsy and this pattern is common, the language lets us use a range loop to iterate over channels too.
go func() {
    for x := range naturals {
        squares <- x * x
    }
    close(squares)
}()
```
Unidirectional Channel

```go
// When a channel is supplied as a function parameter, it is nearly always with the intent that it be used exclusively for sending or exclusively for receiving.
// The type chan<- int, a send-only channel of int, allows sends but not receives. Conversely, the type <-chan int, a receive-only channel of int, allows receives but not sends. (The position of the <- arrow relative to the chan keyword is a mnemonic.)
// Since the close operation asserts that no more sends will occur on a channel, only the send- ing goroutine is in a position to call it, and for this reason it is a compile-time error to attempt to close a receive-only channel.
```

Buffered channel
```go
func mirroredQuery() string {
    responses := make(chan string, 3)
    go func() { responses <- request("asia.gopl.io") }()
    go func() { responses <- request("europe.gopl.io") }()
    go func() { responses <- request("americas.gopl.io") }()
    return <-responses // return the quickest response
}
func request(hostname string) (response string) { /* ... */ }
// Had we used an unbuffered channel, the two slower goroutines would have gotten stuck trying to send their responses on a channel from which no goroutine will ever receive. This sit- uation, called a goroutine leak, would be a bug. Unlike garbage variables, leaked goroutines are not automatically collected, so it is important to make sure that goroutines terminate themselves when no longer needed. Goroutines leak can lead to excessive memory usage and eventually result in a program crash.
```

Looping in Parallel
```go
// makeThumbnails returns before it has finished doing what it was supposed to do. It starts all the goroutines, one per file name, but doesn’t wait for them to finish.
func makeThumbnails2(filenames []string) {
    for _, f := range filenames {
        go thumbnail.ImageFile(f) // NOTE: ignoring errors
    }
}
// There is no direct way to wait until a goroutine has finished, but we can change the inner goroutine to report its completion to the outer goroutine by sending an event on a shared channel. Since we know that there are exactly len(filenames) inner goroutines, the outer goroutine need only count that many events before it returns

func makeThumbnails3(filenames []string) {
    ch := make(chan struct{})
    for _, f := range filenames {
        go func(f string) {
            thumbnail.ImageFile(f) // NOTE: ignoring errors
            ch <- struct{}{}
        }(f) 
    }
    // Wait for goroutines to complete.
    for range filenames {
        <-ch
    } 
}
// 以上代码有循环变量快照问题 简化正确规范

func makeThumbnails3(filenames []string){
    ch :=make(chan struct{})
    for _, f := range filenames {
        copyf:=f
        go func(){
            thumbnail.ImageFile(copyf)
            ch <- struct{}{}
        }()
    }
    for range filenames{
        <-ch
    }
}

// 或者
for _, f := range filenames {
    go func(f string){
        thumbnail.ImageFile(f)
        ch <- struct{}{}
    }(f)
}
```

```go
// What if we want to return values from each worker goroutine to the main one? If the call to thumbnail.ImageFile fails to create a file, it returns an error.
func makeThumbnails4(filenames []string) error {
	errors := make(chan error)
	for _, f := range filenames {
		go func(f string) {
			_, err := thumbnail.ImageFile(f)
			errors <- err
		}(f)
	}
	for range filenames {
		if err := <-errors; err != nil {
			return err // NOTE: incorrect: goroutine leak!
		}
	}
	return nil
}
// When it encounters the first non-nil error, it returns the error to the caller, leaving no goroutine draining the errors channel. Each remaining worker goroutine will block forever when it tries to send a value on that channel, and will never terminate. This situation, a goroutine leak (§8.4.4), may cause the whole program to get stuck or to run out of memory.
// The simplest solution is to use a buffered channel with sufficient capacity that no worker goroutine will block when it sends a message. (An alternative solution is to create another goroutine to drain the channel while the main goroutine returns the first error without delay.)
```

```go
// makeThumbnails6 makes thumbnails for each file received from the channel.
// It returns the number of bytes occupied by the files it creates.
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