```kotlin
val mockedList = mock<MutableList<Any>>()

        //stubbing

        //stubbing
        whenever(mockedList[0]).thenReturn("first")
        whenever(mockedList[1]).thenThrow(RuntimeException())

        //following prints "first"

        //following prints "first"
        println(mockedList[0])

        //following throws runtime exception

        //following throws runtime exception
        println(mockedList[1])

        //following prints "null" because get(999) was not stubbed

        //following prints "null" because get(999) was not stubbed
        println(mockedList[999])

        //Although it is possible to verify a stubbed invocation, usually it's just redundant
        //If your code cares what get(0) returns, then something else breaks (often even before verify() gets executed).
        //If your code doesn't care what get(0) returns, then it should not be stubbed.

        //Although it is possible to verify a stubbed invocation, usually it's just redundant
        //If your code cares what get(0) returns, then something else breaks (often even before verify() gets executed).
        //If your code doesn't care what get(0) returns, then it should not be stubbed.
        verify(mockedList)[0]
```


```kotlin
 when(mock.someMethod("some arg"))
   .thenThrow(new RuntimeException())
   .thenReturn("foo");

 when(mock.someMethod("some arg"))
   .thenReturn("one", "two", "three");

   
//All mock.someMethod("some arg") calls will return "two"
 when(mock.someMethod("some arg"))
   .thenReturn("one")
 when(mock.someMethod("some arg"))
   .thenReturn("two")
```
If instead of chaining .thenReturn() calls, multiple stubbing with the same matchers or arguments is used, then each stubbing will override the previous one