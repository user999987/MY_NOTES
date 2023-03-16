## Read
1. spark.read.
csv, jdbc, json, orc, parquet, textFile ...

2. spark.read.format("...")[.option("...")].load("...")
    * format 指定加载类型, 比如csv json etc 可以参考 1 里面的那些
    * load 指定文件路径
    * option 是在 jdbc 格式下 需要传入的相应参数: url,user,password

## Write
1. df.write.
csv, jdbc, json, orc, parquet, textFile ...

2. df.write.format("...")[.option("...")][.mode("...")].save("...")
mode 有  append, overwrite, errorifexists, ignore

## Default data format
Spark 默认数据格式是 parquet /pɑrˈkeɪ/  Apache 的列式存储格式

spark.read.load("...") & df.write.save("...") 默认为 parquet

## RW MySql
1. Read
```python
>>>dataframe = spark.read.format("jdbc").option("url", "jdbc:mysql://hadoop102/3306").option("dbtable", "emp").option("user", "root").option("password", "12345").load()
>>>dataframe.show()
# Register the data as a temp table for future SQL queries
>>>dataframe_mysql.registerTempTable("trips")
>>>spark.sql("select * from trips where dispatching_base_number like '%2512%'").show()
```
2. Write
* 
```
properties={"user": "username", "password": "password"}
df.write.mode("append").jdbc("jdbc:mysql://hadoop102/3306", "emp", properties)
```
* 
```
dbcDF.write \
    .format("jdbc") \
    .option("url", "jdbc:postgresql:dbserver") \
    .option("dbtable", "schema.tablename") \
    .option("user", "username") \
    .option("password", "password") \
    .save()
```