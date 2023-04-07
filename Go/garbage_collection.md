1. mark and sweep(shortcoming: fragments)
2. mark and compact(multiple times for looping to implement compact)
3. semispace copy(waste memory)
4. reference counting
5. golang (root object,堆栈, span, prtmask, heaparena)

https://juejin.cn/post/6919005994966056968

1. Pages
TCMalloc(Thread-Caching Malloc) basic memory management unit, default size is 8kb