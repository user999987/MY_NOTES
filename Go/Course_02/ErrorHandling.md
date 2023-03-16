## Error interface
```go
type error interface{
    Error() string
}
// Correct operation: error ==nil
// Incorrect operation: Error() prints error message

f, err := os.Open("name.txt")
if err != nil{
    fmt.Println(err)
    // fmt package calls the error() method to generate string to print
    return
}
```