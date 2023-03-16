## Series

Series是一种类似于一维数组的对象，它由一组数据（各种NumPy数据类型）以及一组与之相关的数据标签（即索引）组成。
可以把 Series 堪称一个有定长的有序字典, 因为他是 index 到 value的一个映射, index 可以不是 unique
```
import pandas as pd
from pandas import Series
obj = Series([5,9,2,8])
print(obj)
0   5
1   9
2   2
3   -8
dtype: int64
```

```
obj2 = Series([6,-1,7,3], index=['a','b', 'c', 'd'])
print(obj2)
a   6
b   -1
c   7
d   3
dtype: int64
```

```
province = {'A': 10999, 'B': 9999.98, 'C': 8989, 'D':11211}
obj3 = Series(province)
print(obj3)

A   10999
B   9999
C   8999
D 11211
dtype: float64
```
If both a dict and index sequence are used, the index will override the keys found in the dict.
```
provinces = ['A','B','C','E']
obj4 = Series(province, index=provinces)
print(obj4)

A    10999.00
B     9999.98
C     8989.00
E         NaN
dtype: float64
```


## DataFrame
DataFrame是一种表格型数据结构，它含有一组有序的列，每列可以是不同的值。DataFrame既有行索引，也有列索引，它可以看作是由Series组成的字典，不过这些Series公用一个索引。
```
data = {
    'state':['Ohio','Ohio','Ohio','Nevada','Nevada'],
    'year':[2000,2001,2002,2001,2002],
    'pop':[1.5,1.7,3.6,2.4,2.9]
}
frame = pd.DataFrame(data)
frame

#输出
    pop state   year
0   1.5 Ohio    2000
1   1.7 Ohio    2001
2   3.6 Ohio    2002
3   2.4 Nevada  2001
4   2.9 Nevada  2002
```
DataFrame的行索引是index，列索引是columns，我们可以在创建DataFrame时指定索引的值：
```
frame2 = pd.DataFrame(data,index=['one','two','three','four','five'],columns=['year','state','pop','debt'])
frame2

#输出
    year    state   pop debt
one 2000    Ohio    1.5 NaN
two 2001    Ohio    1.7 NaN
three   2002    Ohio    3.6 NaN
four    2001    Nevada  2.4 NaN
five    2002    Nevada  2.9 NaN
```
使用嵌套字典也可以创建DataFrame，此时外层字典的键作为列，内层键则作为索引:
```
pop = {'Nevada':{2001:2.4,2002:2.9},'Ohio':{2000:1.5,2001:1.7,2002:3.6}}
frame3 = pd.DataFrame(pop)
frame3
#输出
    Nevada  Ohio
2000    NaN 1.5
2001    2.4 1.7
2002    2.9 3.6
```
我们可以用index，columns，values来访问DataFrame的行索引，列索引以及数据值，数据值返回的是一个二维的ndarray
```
frame2.values
#输出
array([[2000, 'Ohio', 1.5, 0],
       [2001, 'Ohio', 1.7, 1],
       [2002, 'Ohio', 3.6, 2],
       [2001, 'Nevada', 2.4, 3],
       [2002, 'Nevada', 2.9, 4]], dtype=object)
```

在 DataFrame 中 axis = 0 意味着 沿着 column 或者 row index 从上往下执行, axis = 1 表示 沿着 row 或者 column index 横向从左到右执行
