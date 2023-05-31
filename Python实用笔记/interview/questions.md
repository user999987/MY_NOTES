1. zip
```python
//zip(*iterables) --> A zip object yielding tuples until an input is exhausted.
list(zip('abcdefg', range(3), range(4)))
[('a', 0, 0), ('b', 1, 1), ('c', 2, 2)]
a=[1,2,3]
b=[2,3,4,5]
c=zip(a,b)
list(c)
// [(1,2),(2,3),(3,4)]
```
2. 参数传递
函数收到的是一个可变对象(dict or list)的引用, 就能修改对象的原始值\
如果函数收到一个不可变对象(num, char or tuple)的引用, 就不能改变原是对象
3. __inti__()重载会显示错误
4. remove and del difference
remove: It is list function, remove first occurrence of value.
    Raises ValueError if the value is not present.
del: It is a statement that used to remove a reference to an object(assignment is binding, del is like unbinding)
5. swapcase()
反转所有大小写
6. 删除空格
strip()前后, lstrip()前, rstrip()后
7. join()
提供一个分隔符串联字符串
```python
iter=["left","right"]
"".join(iter)
// leftright
```
8. random.shuffle()
打乱数组元素
```python
x=["wo","shi","ni","die"]
>>> random.shuffle(x)
>>> x
['ni', 'shi', 'die', 'wo']
```