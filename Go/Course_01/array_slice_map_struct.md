Array
```go
var x [5]int
x[0] = 2

var x [5]int = [5]int{1,2,3,4,5}

x := [...]int{1,2,3,4}

for i,v := range x{
    fmt.Printf("ind %d, val %d", i, v)
}
// range 在数组和切片中它返回元素的索引和索引对应的值，在集合中返回 key-value 对。

```

Slices<br>
A window on an underlying array<br>
3 porperties of slice<br>
1. Pointer indicates the start of the slice
2. Length is the number of elements in the slice
3. Capacity is maximum number of elements
```go
a1 := [3]string("a","b","c")
sli1 := a1[0:1]
fmt.Printf(len(sli1), cap(sli1))
// result is "1 3" the slice could go up to 3 so capacity is 3
sli2 := a2[1:3]
fmt.Printf(len(sli2), cap(sli2))
// result is "2, 2" the slice only can go up to 2 so capacity is 2. the underlying array and slice start pointer determines its capacity
```

Slice Literals<br>
Slice literals can be used to initialize a slice. However when you create a slice, you actually create a underlying array and reference it. Slice points the start of the array lenght is capacity
```go
sli := []int{1,2,3}
// above is slice literal
//below is an array
arr := [...]int{1,2,3}
```

Make
```go
sli = make([]int, 10)
// length = capacity
sli = make([]int, 10, 15)
// lenght is 10 capacity is 15
```

Append<br>
Adds elements to the end of a slice, at the same time inserts into underlying array.
It will increase the size of array if necessary
```go
sli := make([]int,1)
sli = append(sli, 1)
// [0 1]
```

Maps
```go
var idMap map[string]int
//            keytype valuetype
// map[]
var idMap = make(map[string]int)
// initialize an empty map
// map[]

idMap := map[string]int {
    "joe":123, "ri":321
}
// [joe:123 ri:321]

delete(idMap, "joe")
// [ri:321]

id, p := idMap["joe"]
// id is value, p is presence of key. value of p is True or False

for key, val := range idMap{
    fmt.Println(key, val)
}
```

Struct
```go
type Person struct {
    name string
    addr string
    phone string
}

var p1 Person

p1 := new(Person)
// initialize structs with zero value
p1 :=Person{name:"joe", addr:"a st.", phone:"123"}
```
