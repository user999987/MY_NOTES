Garbage collection in Go is primarily focused on managing heap-allocated objects, but it also has some impact on the stack. Specifically, objects that "escape" from the stack to the heap (i.e., are allocated on the stack but persist beyond the scope of the function in which they were declared) may be subject to garbage collection.

In other words, while the Go garbage collector does not explicitly manage the stack, it can indirectly affect stack-allocated objects that escape to the heap. 

The stack in Go is managed by the Go runtime. Each Go routine has its own stack allocated when it is created. The stack is used to store local variables, function arguments and return values, and other data. The size of the stack is fixed at the time the Go routine is created and cannot be resized during its execution. When the Go routine completes, its stack is reclaimed by the runtime.

In the context of garbage collection, lower latency means that the application will be able to respond to requests more quickly since it spends less time paused for garbage collection. However, lower latency may also come at the cost of lower throughput if the garbage collector is less efficient at reclaiming memory. Conversely, higher throughput means that the application can handle more requests in a given period of time, which can be achieved by reducing the overhead of the garbage collector or making it more efficient. \

gc STW <=> memory peak & latency<=>throughput
fewer gc STW, more requests processed by CPU, but when memory hit limit and gc do not work, even if your CPU is free you have no more memory to allocate to process the request