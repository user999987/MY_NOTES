To enable dependency tracking for your code(sort of like python requirements.txt):
```
go mod init module_name
```

To install new required packages:
```
go mod tidy
```

By default, under your home directory, you will see a "go" folder, there are "bin" and "pkg". packages are under `~/go/pkg/mod`


A package is a directory of .go files, and it is the basic building block of a Go program. Packages help to organize code into reusable components. On the other side, a module is a collection of packages with built-in dependencies and versioning. A module comes with two additional files go. mod and go.
package is folder.
package name is folder name.
package path is folder path

for non-production use, you define your module locally, you can run 
```
go mod edit -replace example.com/greetings=../greeting
```
run above command, your go.mod will be updated, you will see below in the file
```
replace example.com/greeting => ../greetings
```
after running `go mod edit`, file will be looked like below
```
require (
	example.com/greetings v0.0.0-00010101000000-000000000000
	rsc.io/quote v1.5.2
)
```

string, rune & bytes \
byte is an alias for the uint8 data type and is used to represent ASCII characters or 8-bit binary data. It is the smallest addressable unit of memory in Go.

rune, on the other hand, is an alias for the int32 data type and is used to represent Unicode code points. It can hold any valid Unicode code point, which ranges from 0 to 0x10FFFF.

When dealing with strings, it is common to use rune instead of byte to ensure that the program can handle Unicode characters.

```
https://juejin.cn/post/6844903743524175879
```


Common format
```go
%v: prints the value in a default format. It can be used with any type of value.
%d: prints an integer in decimal format.
%f: prints a floating-point number in decimal format.
%s: prints a string of characters.
%t: prints a boolean value as "true" or "false".
%p: prints a pointer value in hexadecimal format.
%x, %X: prints an integer in hexadecimal format.
```

Defer recover
```

func main() {
	panic("Oh Yes! Come on!")//程序直接over
	defer func() {
		if err := recover(); err != nil {
			fmt.Println("Recovered from panic:", err)
		}
	}()

	panic("Oh no! Something went wrong.")//defer可会跑
}
```
When a panic() is called, the program stops execution at that point and begins to unwind the call stack(通俗来讲就是从错误发生的地方stack开始弹出 从代码来看就是如果有defer写在panic之前defer中的代码是可以跑的 之后的则不行)

Gin 
```go
router := gin.Default()
router.Run(":8080")
// in essence, inside rounter.Run(), http.ListenAndServe(address, engine.Handler()) is get called
```


Toml read \
1. no need to use struct tag
2. how to read below code? whne you have `[]`, you need nest a struct, when you have `[[]]`, type of nested struct is an array
```toml 
name = "xcloud"
[rabbit]
server = "104.233.212.25"
port = 5672
user = "god"
address = "CN"
[[arr]]
first=1
[[arr]]
first=11
```
```go
type RabbitConfig struct {
	Server   string //`toml:"server"`
	User     string `toml:"user"`
	Port     int    `toml:"port"`
	Location string `tmol:"location"`
}
type Config struct {
	Name   string
	Rabbit RabbitConfig
	Arr    []ArrConfig
}
type ArrConfig struct {
	First int
}


func main() {
	var config Config
	if _, err := toml.DecodeFile("config.toml", &config); err != nil {
		fmt.Println("Error decoding config file:", err)
		return
	}

	fmt.Println(config.Rabbit)
	fmt.Println(config.Rabbit.User)
	fmt.Println(config.Rabbit.Port)
	fmt.Println(config.Rabbit.Location)
	fmt.Println(config.Rabbit.Server)
	fmt.Println(config.Name)
	fmt.Println(config.Arr[0].First)
	fmt.Println(config.Arr[1].First)
	}
```



In Go, when a struct field is declared as a pointer type (i.e. *Type), the field is stored as a memory address that points to the actual value stored somewhere else in memory. On the other hand, when a struct field is declared as a non-pointer type (i.e. Type), the actual value is stored directly in the field itself.

The main difference between using a pointer type versus a non-pointer type for a struct field is in how the value is passed and copied between functions and methods.

If a non-pointer type is used, a copy of the value is made whenever the struct is passed to a function or method. This means that any changes made to the copy do not affect the original struct. On the other hand, if a pointer type is used, only the memory address is copied, not the value itself. This means that changes made to the copy affect the original struct.

Another difference is in how nil values are handled. A nil pointer field means that it doesn't point to any value. On the other hand, a nil non-pointer field means that the value is not initialized yet.

In general, pointers are used when the struct field needs to be mutable or when the struct is very large and copying it would be inefficient. Non-pointer types are used when the struct field is immutable or when the struct is small and copying it is not a performance issue.


```go
app/
  cmd/
    main.go
  internal/
    config/
      config.go
    domain/
      model/
        user.go
        product.go
      repository/
        user_repository.go
        product_repository.go
      service/
        user_service.go
        product_service.go
      event/
        event.go
      errors/
        domain_error.go
    infrastructure/
      database/
        database.go
      logging/
        logging.go
      router/
        router.go
      http/
        handler/
          user_handler.go
          product_handler.go
        middleware/
          auth.go
    presentation/
      rest/
        user_controller.go
        product_controller.go
      grpc/
        user_server.go
        product_server.go
```
Here's a brief explanation of each folder:

cmd: Contains the main entry point of the application.\
internal: Contains the code that is not exposed to the outside world. This folder is further divided into:\
1. config: Contains the configuration code.
2. domain: Contains the domain models, repositories, services, events, and error codes.
3. infrastructure: Contains the code for the infrastructure layer. This includes the database, logging, router, and HTTP layer.
4. presentation: Contains the presentation layer. This includes the REST and gRPC controllers.\

The domain layer contains the domain models, repositories, services, events, and error codes. The infrastructure layer contains the database, logging, router, and HTTP layer. The presentation layer contains the REST and gRPC controllers.

The domain layer is at the heart of the application and should contain the business logic. The infrastructure layer should contain the implementation details of the infrastructure. The presentation layer should contain the code that interacts with the outside world.

In summary, the DDD approach in a Gin project involves organizing the codebase around the business domain and keeping the implementation details separate from the business logic.