
go mod init modulename 初始化一个go module <br>
modulename 是 module path 大多数情况下 是 repository 比如 github.com/mymodule<br>
如果你的代码中引入了 新的module 比如
```go
import "rsc.io/quote"
```
这时 你可以使用 go mod tidy
```
$ go mod tidy
go: finding module for package rsc.io/quote
go: found rsc.io/quote in rsc.io/quote v1.5.2
```
go.mod file 内容如下:
```
module localhost/hello

go 1.16

require(
    localhost/greetings v0.0.0-000101010000000-0000000000
    rsc.io/quote v1.5.2
)

replace localhost/greetings => absolute path
```

module 路径默认在 $GOROOT /usr/local/go/src/modulepath
or $GOPATH /Users/wwl/go/src/localhost/greetings

go mod edit -replace example.com/greetings=/Users/wwl/go/src/localhost/greetings