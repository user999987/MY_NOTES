Key-Value type RDD has partitioner only
非 key-value 
rdd.partitioner = None

hash-parititoner容易造成数据倾斜
range-partitioner key要可比较
custom-partitioner 

spark只能按key分区 因为 getPartition 只有 key 被传入
```
Scala
class CustomPartitioner(parititions: Int) extends Partitioner{
    
    override def numPartitions: Int = partitions

    override def getPartition(key: Any): Int = ???
}

rdd.partitionBy(new CustomPartitioner(3))
```
