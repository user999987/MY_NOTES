结构化数据 二维表 结构来逻辑表达和实现的 数据
Spark SQL 是 Spark 用来处理结构化数据的 一个模块 提供了2个编程 抽象 DataFrame和DataSet 皆为 分布式数据集 建立在RDD之上
写 Spark SQL 而非 Spark Core 语句, 降低开发成本

Hive 有一个所谓的 谓词下推 select something from t1 join t2 on t2.something = some condition
以上语句 会先执行 后面的 condition 然后在做join select

Spark SQL 也一样 有查询优化
users.join(events, user("id") === event("uid)).filter( events("date") > "2015-01-01")
此语句会先之后filter 在做join
如果直接用 RDD 做这个逻辑 并不会发生优化

老版本 Spark SQL 有两种起点 SQLContext 和 HiveContext
之后 SparkSession 出现作为两者的结合





## DataFrame
DataFrame 以 RDD 为基础的分布式数据集, 带有 schema meta 信息, 类似传统数据库的 二维表格. (A DataFrame is a Dataset organized into named columns.)
Throughout the documentation, we will often refer to Scala/Java Datasets of Rows as DataFrames.
https://spark.apache.org/docs/latest/sql-programming-guide.html

scala:
```
> df = spark.read.json("path")
返回一个dataframe 
> df.createTempView("people")
> spark.sql("select * from people where age > 20")
返回还是一个 dataframe res4:
> res4.show
返回结果和mysql的查询结果类似
+---+----+
|age|name|
+---|----+
|30 |Andy|
+---+----+
```


sparkSession.createTempView 是为当前 session创建一个表 如果 spark.NewSession.sql 去读之前的表就会报错, 可以使用 createGlobalTempView('person') 此时访问 全局表使用 global_temp.person

### UDF - User Defined Function
spark.udf.register(name, f, returnType=None)
```
>>> strlen = spark.udf.register("stringLengthString", lambda x: len(x))
>>> spark.sql("SELECT stringLengthString('test')").collect()
[Row(stringLengthString(test)='4')]
```

### UDAF
registerJavaUDAF(name, javaClassName)[source]
Register a Java user-defined aggregate function as a SQL function.
Parameters:
* name – name of the user-defined aggregate function
* javaClassName – fully qualified name of java class
```
>>> spark.udf.registerJavaUDAF("javaUDAF", "test.org.apache.spark.sql.MyDoubleAvg") 
# test.org.apache.spark.sql has MyDoubleAvg, MyDoubleSum and something else. you can find it on https://github.com/apache/spark/tree/master/sql/core/src/test/java/test/org/apache/spark/sql
>>> df = spark.createDataFrame([(1, "a"),(2, "b"), (3, "a")],["id", "name"])
>>> df.createOrReplaceTempView("df")
>>> spark.sql("SELECT name, javaUDAF(id) as avg from df group by name").collect()
[Row(name='b', avg=102.0), Row(name='a', avg=102.0)]
```


### DataFrame 和 RDD转换
1. df.rdd
```
> res19.collect
Array[(String, Int)] = Array( (Mich, 29), (Andy,30), (Jus,19))
> res19.toDF("name", "age")
res21: xxxxx = [name: string, age: int]
> res21.show
+---+----+
|age|name|
+---|----+
|30 |Andy|
+---+----+
|29 |Mich|
+---+----+
|19 | Jus|
+---+----+
```
2. createDataFrame
```
l = [('Alice', 1)]
spark.createDataFrame(l).collect()
[Row(_1='Alice', _2=1)]
spark.createDataFrame(l, ['name', 'age']).collect()
[Row(name='Alice', age=1)]
```

## DataSet
DataSet 是 DataFrame 的一个扩展
In Scala and Java, a DataFrame is represented by a Dataset of Rows. In the Scala API, DataFrame is simply a type alias of Dataset[Row]. 


However, Python does not have the support for the Dataset API. But due to Python’s dynamic nature, many of the benefits of the Dataset API are already available (i.e. you can access the field of a row by name naturally row.columnName).
### Language Type
* 动态类型语言：在运行期进行类型检查的语言，也就是在编写代码的时候可以不指定变量的数据类型，比如Python和Ruby
* 静态类型语言：它的数据类型是在编译期进行检查的，也就是说变量在使用前要声明变量的数据类型，这样的好处是把类型检查放在编译期，提前检查可能出现的类型错误，典型代表C/C++和Java
* 强类型语言，一个变量不经过强制转换，它永远是这个数据类型，不允许隐式的类型转换。举个例子：如果你定义了一个double类型变量a,不经过强制类型转换那么程序int b = a无法通过编译。典型代表是Java。
* 弱类型语言：它与强类型语言定义相反,允许编译器进行隐式的类型转换，典型代表C/C++

