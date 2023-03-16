Goroutine, Machine(worker thread), Processor(a resource that is required to execute Go code)
```
1. We create a goroutine through Go func ();

2. There are two queues that store G, one is the local queue of local scheduler P, one is the global G queue. The newly created G will be saved in the local queue in the P, and if the local queues of P are full, they will be saved in the global queue;

3. G can only run in m, one m must hold a P, M and P are 1: 1 relationship. M will pop up a executable G from the local queue of P. If the local queue is empty, you will think that other MP combinations steals an executable G to execute;

4. A process executed by M Scheduling G is a loop mechanism;

5. When M executes syscall or the remaining blocking operation, M will block, if there are some g in execution, Runtime will remove this thread M from P, then create one The new operating system thread (if there is an idle thread available to multiplex idle threads) to serve this P;

6. When the M system call ends, this G will try to get an idle P execute and put it into this P's local queue. If you get P, then this thread m becomes a sleep state, add it to the idle thread, and then this G will be placed in the global queue.
```

https://www.programmersought.com/article/79557885527/
https://go.cyub.vip/gmp/gmp-model.html

context: https://segmentfault.com/a/1190000040917752
channel&select: https://juejin.cn/post/6844903940190912519