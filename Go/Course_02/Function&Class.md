## Function
```go
func sum(a int, b int) int{
    return a+b
}
```

## Functions as Arguments
```go
func main(){
    applyIt(area, 2, 4)
}
/* fname-name
   func (int, int) int-type
*/
func applyIt(fname func (int, int) int, val1, val2 int) int{
    return fname(val1, val2)
}
func area(a,b int) int{
    return a*b
}
```

You cannot put applyIt and area inside of main the way like you define them like usual, if you want to do it
```go
func main(){
    applyIt := func (fname func (int, int) int, val1, val2 int) int{
    return fname(val1, val2)
}
    area := func (a,b int) int{
        return a*b
    }
    applyIt(area, 2, 4)
}
```

## Functions as returns
```go 
/*
func (float64, float64) float64-type
*/
func makeDistOrigin (ox, oy, float64) func (float64, float64) float64{
    fn:=func(x,y float64) float64{
        return math.Sqrt(math.Pow(x-ox,2) + math.Pow(y-oy, 2))
    }
    return fn
}
```
## Environment of a Function
Environment includes names defined in  block where the function is defined
<pre>
var <span style="color:red">x</span> int 
func foo( <span style="color:red">y</span> int){
    <span style="color:red">z</span> := 1
    ...
}
</pre>

When pass functions as arguments, environment go along with the function.</br>
Closure 
1. function + environment
2. When functions are passed/returned, their environment comes with them

```go
func MakeDistOrigin(ox, oy, float64) func(float64, float64) float64{

    fn:=func(x,y float64) float{
        return math.Sqrt(math.Pow(x-ox, 2)) + math.Sqrt(math.Pow(y-oy, 2))
    }
    return fn
}

func main(){
    Dist1:=MakeDistOrigin(0,0)
    Dist2:=MakeDistOrigin(2,2)
    fmt.Println(Dist1(2,2))
    fmt.Println(Dist2(2,2))
}
// 0,0 and 2,2 are in the closure of Dist1 and Dist2
```

```go
func getMax(vals ...int) int{
    maxV:=-1
    for _, v:=range vals{
        if v>maxV{
            maxV=v
        }
    }
    return maxV
}
// Treated as slice inside function

vslice:=[]int{1,2,34,5}
fmt.Println(getMax(vslice...))
// Need the ... suffix
```

## Copy by value
copy by value really make a copy of parameters to the function, if the arguments is large, it will take a lot of time like type Image [100][100]int

## Deferred Function Calls
* Call can be deferred until the surrouding function completes
* Typically used for cleanup activities (like close file)
* Arguments of deferred call are evaluated immediately
```go
func main(){
    i:=1
    defer fmt.Println(i+1)
    i++
    fmt.Print("Hello!")
}
// output is 2
```

## Associating Methods with Data
* method has a receiver type that is associated with
```go
type MyInt int

func (name MyInt) Double () int{
    return int(name*2)
}

func main(){
    v:=MyInt(3)
    fmt.Println(v.Double())
}
```
```go
func (p Point) DistToOrig(){
    t:=math.Pow(p.x,2) + math.Pow(p.y,2)
    return math.Sqrt(t)
}
func main(){
    p1:=Point(3,4)
    fmt.Println(p1.DistToOrig())
}
```
* Receiver is passed implicitly as an argument to the method
* Method cannot modify the data inside the receiver
```go
func main(){
    p1 := Point(3,4)
    p1.OffsetX(5)
}
// OffsetX()should increase X but it did not 
```

## Pointer Receiver
```go
func (p *Point) OffsetX(v float64){
    p.x = p.x + v
}
// Point is referenced as p, not *p
// Dereferencing is automatic with .operator (*p is called dereferencing)
```
```go
func main(){
    p := Point(3,4)
    p.OffsetX(5)
    fmt.Println(p.x)
}
// Do not need to reference when calling the method
// ampersand is not needed here &p.OffsetX is not needed.
```

## Good programming practice
Either ALL methods use pointer receivers or NONE methods use pointer receivers.
