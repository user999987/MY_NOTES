## String, Rune, Bytes
string就是只读的采用utf8编码的字节切片(slice) 因此用len函数获取到的长度并不是字符个数，而是字节个数
for 循环遍历输出的是各个字节 range是各个字符
```go
str1:="卧槽"
for i:=0;i<len(str1);i++{
    fmt.Println(i,str1[i])
}
//
0 229
1 141
2 167
3 230
4 167
5 189
//
for k, v := range str1 {
    fmt.Println(k, v, string(v))
}
//
0 21351 卧
3 27133 槽
//
```

rune是int32的别名，代表字符的Unicode编码，采用4个字节存储，将string转成rune就意味着任何一个字符都用4个字节来存储其unicode值，这样每次遍历的时候返回的就是unicode值
```go
runes := []rune(str1)
fmt.Println(len(runes))//2
fmt.Printf("v",runes[1])// 27133
fmt.Printf("%c", runes[1])// "槽"
fmt.Println(string(runes[1]))//"槽"
```
bytes操作的对象也是字节切片，与string的不可变不同，byte是可变的，因此string按增量方式构建字符串会导致多次内存分配和复制，使用bytes就不会因而更高效一点
```go
var b bytes.Buffer
b.WriteString("中国")
for i:=0;i<10;i++{
    b.WriteString("a")
}
fmt.Println(b.String())//中国aaaaaaaaaa
```


### "1"==string(1)
integer 1 与字符串 "1" 本身就是不同类型值,直接比较会返回false。
string(1) 实际上是整数1的Unicode码点表示,值是49,而不是字符串"1"。



## Defer
defer的顺序是个stack 后入先出, 其调用的参数的值 在 defer 定义时就确定了 
```go
i:=10
defer func(){
    fmt.Println("defer:",i)
}()
i=20 // defer: 10
```

### defer and return

```go
func FieldDefer1() string {
	x := "a"
	defer func() {
		x = "b"
	}()
	return x
} // a

func FieldDefer2() (x string) {
	x = "a"
	defer func() {
		x = "b"
	}()
	return x
} // b
```
区别在于 匿名返回值 和 有名返回值
1. defer延迟执行发生在return语句执行之后
2. defer语句访问到的返回值是在该语句执行时的值

匿名返回值是在return执行时才被隐式声明，而具名返回值则是在函数声明的时候被声明

## For loop start goroutine
```go
for _, val := range values {
    go func(val interface{}) {
        fmt.Println(val)
    }(val) // immediately invoked anonymous function
}
```
"循环变量捕获" 问题。在循环中使用匿名函数和 goroutine 时，因为 goroutine 可能在循环结束后才开始执行，它们会捕获循环变量的最终值，而不是每次迭代的值。这通常不是您所期望的行为

## Channel
常见场景
1. 同步协程: 某个协程完成了某些操作之后，可以通过向特定的通道发送数据来通知另一个协程
2. 限制并发: 某个协程执行之前，可以从通道中读取一个数据来获得执行许可，而在执行完成后，可以再次向通道中写入数据来释放执行许可。
3. 协程间数据传递: 某个协程中生成了某些数据，可以通过向通道中写入数据来传递给其他协程

5 operations
1. 关闭一个通道
```go
close(ch)
```
2. 通道发送一个值
```go
ch <- v
```
3. 从ch接收一个值
```go
<- ch
```
4. 查通道容量
```go
cap(ch)
```
5. 查通道长度
```go
len(ch)
```

3种通道
1. nil通道
2. non-nil but closed 
3. non-nil and open

关闭 1-panic 2-panic 3-close \
发送 1-block forever 2-panic 3-block&success \
接收 1-block forever 2-never block 3-block&success 

what is Channel exactly?\
它的底层是一个叫做hchan的结构体
```go
type hchan struct {
   //channel分为无缓冲和有缓冲两种。
   //对于有缓冲的channel存储数据，借助的是如下循环数组的结构
     qcount   uint           // 循环数组中的元素数量
     dataqsiz uint           // 循环数组的长度
     buf      unsafe.Pointer // 指向底层循环数组的指针
     elemsize uint16 //能够收发元素的大小
   
 ​
     closed   uint32   //channel是否关闭的标志
     elemtype *_type //channel中的元素类型
   
   //有缓冲channel内的缓冲数组会被作为一个“环型”来使用。
   //当下标超过数组容量后会回到第一个位置，所以需要有两个字段记录当前读和写的下标位置
     sendx    uint   // 下一次发送数据的下标位置
     recvx    uint   // 下一次读取数据的下标位置
   
   //当循环数组中没有数据时，收到了接收请求，那么接收数据的变量地址将会写入读等待队列
   //当循环数组中数据已满时，收到了发送请求，那么发送数据的变量地址将写入写等待队列
     recvq    waitq  // 读等待队列
     sendq    waitq  // 写等待队列
 ​
 ​
     lock mutex //互斥锁，保证读写channel时不存在并发竞争问题
 }
```
G1 send G2 receive, 当 ch 的 buf 满了的时候, 会通知 scheduler, G1会变成 waiting, 此时会创建一个代表自己的 sudog 的结构 放到 sendq, sudog结构中保存了channel相关的变量的指针(如果该Goroutine是sender，那么保存的是待发送数据的变量的地址，如果是receiver则为接收数据的变量的地址，之所以是地址，前面我们提到在传输数据的时候使用的是copy的方式)

Why channel 是 线程 安全 因为 buf 中的数据 enque deque 的时候使用了 mutex lock

### channel done?
```go
done:=make(chan struct{})
/*
struct{} is an empty struct, it is often used as channel type because it does not use extra memory
This kind of channel is often used for signal delivery in goroutines to inform a goroutine when exit or something happens at what time. For example have a `done` channel in main goroutine, other goroutines send signals to indicate the exit
*/
done <- struct{}{}
/*
send an empty struct `{}` to channel done as a signal
*/
```
###  garbage collection of channel and goroutine 
一个 channel 被 sendq 和 recvq 中的 所有 goroutines 引用着. 如果一个 channel 的这两个队列只要一个不为空, 则此协程不会被垃圾回收. 

## Channel Use Case
### Timer
```go
func AfterDuration(d time.Duration) <- chan struct{} {
	c := make(chan struct{}, 1)
	go func() {
		time.Sleep(d)
		c <- struct{}{}
	}()
	return c
}
```
```go
func main() {
	done := make(chan struct{})
	go func() {
		for i := 1; i < 500; i++ {
			time.Sleep(time.Second * 2)
			fmt.Println("hello")

		}
		done <- struct{}{}
	}()
	<-done
}
```

### mutex
通道可以用做互斥锁 但是不如 sync 标准库的 互斥锁高效
### timeout
可以用来处理超时 实际上 context 的超时底层实现就是用了 channel
## Functions & Structs
Functions are first-class values in Go, just like other types. They can be assigned to variables, passed as arguments, returned from other functions etc

However, functions in Go are analogous to pointers - they do not copy the whole function code, just a reference/address to the function.

make() allocates memory for the struct and initializes all fields to their zero values.
```go
p := make(Person)
```


## sync 包
### sync.WaitGroup
请注意
```go
wg.Add(delta) - (&wg).Add(delta)
wg.Done() - (&wg).Done()
wg.Wait() - (&wg).Wait()
简写形式
```
一个sync.WaitGroup值用来让某个协程等待其它若干协程都先完成它们各自的任务

```go
func main() {
	rand.Seed(time.Now().UnixNano()) // Go 1.20之前需要

	const N = 5
	var values [N]int32

	var wg sync.WaitGroup
	wg.Add(N)
	for i := 0; i < N; i++ {
		i := i
		go func() {
			values[i] = 50 + rand.Int31n(50)
			fmt.Println("Done:", i)
			wg.Done() // <=> wg.Add(-1)
		}()
	}

	wg.Wait()
	// 所有的元素都保证被初始化了。
	fmt.Println("values:", values)
}
```
### sync.Once

## 引用？
只有切片、映射、通道和函数类型属于引用类型。