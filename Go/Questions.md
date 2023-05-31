1. rune: unicode code point
2. check if map has key:
```go
var mapp map[int]string
if _, ok := mapp[10]; ok{

}else{

}
```
3. default para and optional para are not supported in golang but can use ellipsis (...)
```go 
// 这个函数可以传入任意数量的 []int 
// []int is slice [1]int is array
func mergeSlices(slices ...[]int) []int {}
```
4. defer 执行顺序: 倒序
5. 指明返回值和不指明
```go
// 返回i为0
func test() int {
	i := 0
	defer func() {
		i += 1
		fmt.Println("defer")
	}()
	return i
}
// 返回i为1
func testi() (i int) {
	i = 0
	defer func() {
		i += 1
		fmt.Println("defer2")
	}()
	return i
}
```
test()不是有名返回, return执行后Go会创建一个临时变量保存返回值, 直到所有defer运行完然后返回. 如果是有名返回 testi() 执行return时并不会再创建临时变量保存,  因此 defer 修改了 i 就会对 返回值产生影响. 从函数体就能看出 test() i:=0, 而testi() i=0
6. Go语言的tag用处: json 序列化和db 映射字段名字, 总的来说就是结构体到目标样式字段的映射关系
7. 
