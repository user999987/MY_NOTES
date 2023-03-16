## Polymorphism
* ability for an object to have different "forms" depending on the context
```go
type Shape interface {
    area() float64
}
type Rectangle struct{
    width, height float64
}
type Circle struct{
    radius flost64
}
func (r Rectangle) area() float64{
    return r.width*r.height
}
func (c Circle) area() float64{
    return 3.14*c.radius*c.radius
}
func main(){
    r:=Rectangle{width:5, height:10}
    c:=Circle{radius:7}

    shapes:=[]Shape{r,c}

    for _, s :=range shapes{
        fmt.Println(s.area())
    }
}
*/
```




## Interface with Nil Dynamic Value
```go
var s1 Speaker
var d1 *Dog
s1=d1
s1.Speak()
// s1.Speak() is still legal because s1 know its dynamic type it can call Dog Speak mechod. But Speak need do some changes

// recommand passing by ref
func (d *Dog) Speak(){
    if d == nil{
        fmt.Println("noise")
    }else{
        fmt.Println(d.name)
    }
}
```

## Using interfaces as parameter
```go
type Shape2D interface{
    Area() float64
    Perimeter() float64
}

type Triangle{...}
func (t Triangle) Area() float64{...}
func (t Triangle) Perimeter() float64{...}

type Rectangle{...}
func (t Rectangle) Area() float64{...}
func (t Rectangle) Perimeter() float64{...}
// Rectangle and Triangle satisfy the Shape2D interface

func FitInYard(s Shape2D) bool{
    if (s.Area() > 100 && s.perimeter() > 100){
        return true
    }
    return false
}
// Parameter is any type that satisfies the interface
```

## Empty Interface
* Empty interface specifies no methods
* All types satisfy the empty interface
* Use it to have a function accept any type as a prameter
```go
type Any interface{}
func DrawShape(s Shape2D) bool{
    switch sh := s.(type) {
        case Rectangle:
            DrawRect(sh) 
        case Triangle:
            DrawTriangle(sh)
        default:
            fmt.Println("unknown")
        }
}
// version 1
func add(a, b Any) string {
	switch reflect.TypeOf(a).Kind() {
	case reflect.String:
		return "string"
	case reflect.Float32, reflect.Float64:
		return "float"
	default:
		return "not supported"
	}    
}
// version 2
func add(x Any) string{
    switch x.(type){
        case string:
        return "string"
        default:
        return "int"
    }
}

func Printme(val interface{}){
	fmt.Print(val)
}
func main() {
    x:=X{Name:"wo",Age:123,Gender:"cao"}
	Printme(x)
    // {wo 123 cao}
    Printme(1)
    //1
    Printme("ri")
    //ri
}
```

## Type Assertions for Disambiguation
```go

// declare interface and assign
var i interface{} = "a string"
// or type Any interface{}
var j Any = "another string"
//type-assertion
vi, ok := i.(string)    // "a string"
if ok{
	fmt.Println(vi)
}
vj, ok :=j.(string)
if ok{
	fmt.Println(vj)
}



func DrawShape(s Shape2D) bool{
    rect, ok := s.(Rectangle)
    if ok {
        DrawRect(rect)
    }
    tri, ok := s.(Triagnle)
    if ok{
        DrawRect(tri)
    }
}
```


## Reflection
```go
import reflect
type Any interface{}
var x Any = []int{1,2,3}
xType := reflect.TypeOf(x)
xValue:= reflect.ValueOf(x)
fmt.Println(xType, xValue)
// []int [1,2,3]
type List []int
var y = List{3,2,1}
yType:=reflect.TypeOf(y)
yValue:=reflect.TypeOf(y)
fmt.Println(yType,yValue)
// package.List, [3,2,1]
```
