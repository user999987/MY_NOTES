## Requests for Comments - Definitions of Internet protocols and formats </br>
Example protocols
* HTML - Hypertext Markup Language
* URI - Uniform Resource Identifier
* HTTP - Hypertext Transfer Protocol
```
RFC始于1969年，由当时就读加州大学洛杉矶分校（UCLA）的斯蒂芬·克罗克（Stephen D. Crocker）用来记录有关ARPANET开发的非正式文档，他是第一份RFC文档的撰写者。最终演变为用来记录互联网规范、协议、过程等的标准文件
```

Protocol Packages</br>

```go
//"net/http"
http.Get("www.uci.ed")

//"net"
net.Dial("tcp", "uci.eud:80:")
```
JSON Marshalling
```go
p1 := Person{name:"joe", addr:"a st", phone:"123"}

barr, err1 := json.Marshal(p1)
// Marshal() returns JSON representation as []byte
// And barr will be an empty struct, json only export fields that initials get capitalized.

type Person struct{
  Name string `json:"name"`
  Addr string
  Phone int
  }
p11 := Person{Name:"joe", Addr:"a st", Phone:123}
arr1, _ := json.Marshal(p11)
// {"name":"joe", "Addr":"a st", "Phone":123}

var p2 Person
// barr is a JSON object
err2 := json.Unmarshal([]byte(barr), &p2)
// barr is supposed to be []byte 
// pointer to go object is passed to Unmarshal()
```

Files
```go
// basic operations
// "io/ioutil"
dat, e := ioutil.ReadFile("filename.txt")
// dat is []byte filled with contents of entire file

dat = "Hello, World!"

err :=  ioutil.WriteFile("filename.txt", dat, 0777)
// writes []byte to file and unix style file permission
```

```go
// more control
// "os"
f, err := os.Open("filename.txt")
// returns a file descriptor

barr := make([]byte,10)
nb, err := f.Read(barr)
// fill barr 10byte everytime it runs
f.Close()
```

```go
f, err := os.Create("filename.txt")

barr := []byte{1,2,3}
nb, err := f.Write(barr)
nb, err := f.WriteString("Hi")
```
