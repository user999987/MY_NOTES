Three common sets of data sources:
1. File formats and filesystems
    * For data stored in a local or distributed filesystem, such as NFS, HDFS, or Ama‐ zon S3, Spark can access a variety of file formats including text, JSON, SequenceFiles, and protocol buffers. 
2. Structured data sources through Spark SQL
    * The Spark SQL module, covered in 9xxx.md, provides a nicer and often more efficient API for structured data sources, including JSON and Apache Hive.
3. Databases and key/value stores
    * Will sketch built-in and third-party libraries for connecting to Cassandra, HBase, Elasticsearch, and JDBC databases.

### ***File Formats***

***Text Files***
1. textFile() # read a text file, collect的结果是一个数组 每个元素对应文件的一行
2. wholeTextFiles() # read a directory of text files, collect 的结果是一个tuple(key, value)数组, tuple[0]是文件名 tuple[1]是文件内容
3. rdd.saveAsTextFile(outputFile)

***JSON***
Load the data as a text file and then mapping over the values with a JSON parser.
* load
```
input = sc.wholeTextFiles()
data = input.map(lambda x: json.loads(x))
```
* save
```
(data.filter(lambda x: x['lovesPandas']).map(lambda x: json.dumps(x)) .saveAsTextFile(outputFile))
```

***CSV***
Same as JOSN
* load
```
def loadRecord(line):
    """Parse a CSV line"""
    input = StringIO.StringIO(line)
    reader = csv.DictReader(input, fieldnames=["name", "favouriteAnimal"]) return reader.next()
input = sc.textFile(inputFile).map(loadRecord)
```
* save
```
def writeRecords(records):
    """Write out CSV lines"""
    output = StringIO.StringIO()
    writer = csv.DictWriter(output, fieldnames=["name", "favoriteAnimal"]) 
    for record in records:
        writer.writerow(record) 
    return [output.getvalue()]
pandaLovers.mapPartitions(writeRecords).saveAsTextFile(outputFile)
```

***sequenceFile***
* load
> sequenceFile()

* save
> saveAsSequenceFile()


### ***File Systems***
***Local/"Regular"FS***

If your file isn’t already on all nodes in the cluster, you can load it locally on the driver without going through Spark and then call parallelize to distribute the con‐ tents to workers. This approach can be slow, however, so we recommend putting your files in a shared filesystem like HDFS, NFS, or S3.

***Amazon S3***

S3 is especially fast when your compute nodes are located inside of Amazon EC2, but can easily have much worse performance if you have to go over the public Internet.
Pass a path start‐ ing with s3n:// to Spark’s file input methods, of the form s3n://bucket/path- within-bucket. As with all the other filesystems, Spark supports wildcard paths for S3, such as s3n://bucket/my-files/*.txt.

***HDFS***

The Hadoop Distributed File System (**HDFS**)


### ***Structured Data with Spark SQL***

***Hive***

To connect Spark SQL to an existing Hive installation, you need to provide a Hive configuration. You do so by copying your hive-site.xml file to Spark’s ./conf/ direc‐ tory. Once you have done this, you create a HiveContext object, which is the entry point to Spark SQL, and you can write Hive Query Language (HQL) queries against your tables to get data back as RDDs of rows.
```
from pyspark.sql import HiveContext
hiveCtx = HiveContext(sc)
rows = hiveCtx.sql("SELECT name, age FROM users") 
firstRow = rows.first()
print firstRow.name
```

***JSON***

To load JSON data, first create a HiveContext as when using Hive. (No installation of Hive is needed in this case, though—that is, you don’t need a hive- site.xml file.)
```
tweets = hiveCtx.jsonFile("tweets.json") 
tweets.registerTempTable("tweets")
results = hiveCtx.sql("SELECT user.name, text FROM tweets")
```

***小样Demo***

```
from pyspark import SparkContext
from pyspark.sql import SQLContext
import sys
 
if __name__ == "__main__":
    sc = SparkContext(appName="mysqltest")
    sqlContext = SQLContext(sc)
    df = sqlContext.read.format("jdbc").options(url="jdbc:mysql://localhost:3306/employees?user=root&password=appleyuchi",dbtable="salaries").load()
    df.show()
    df.stop()
```

> splitSize = max(1, min( goalSize, blockSize )) # 1的unit是bytes 所以 33554432 是32Mb blockSize
预估分区 帮助 load时候核数选择
