Transformation of RDD is lazy execution
当使用转换操作时候只是建立了连接(list of dependencies on other RDDs, 往这里面加东西) 
而没有真正运行 所以 sc.textFile("/word.tst") 不会报错 直到使用action算子 比如 collect

RDD的创建
1. 集合中创建 
    - parallelize 和 makeRDD(主要区别再约makeRDD可以指定切片所在节点hostname)
    - RDD.partitions.length 获取分区数
2. 外部文件
    * sc.xxxxFile
3. 从其他RDD创建 (10分区 1000数据)
    - 假设文件 word.txt 
    -  hadoop spark
    - give hive hdfs
```
    rdd.
        map()
        mapPartition() # map会调用1000次(作用在每一行) mapPartitions会调用10次(作用在每个分区) 注意 此处的mapPartition是Spark的mapPartition
        mapPartitionWithIndex()
        flatMap() # sc.textFile("./word.txt").collect 返回 Array(hadoop spark, give hive hdfs)
                  # sc.textFile("./word.txt").flatMap(_.split(" ")).collect返回 Array(hadoop, spark, give, hive, hdfs)
        glom() # rdd = sc.parallelize(Array(1,2,3,4)), rdd.glom.collect 返回  Array(Array(1,2), Array(3,4))
        groupBy() # rdd.groupBy(x=>2%2).collect 返回 Array((0, CompactBuffer(2,4)), (1,CompactBuffer(1,3)))
                  # This operation may be expensive. If you are grouping in order to perfome an aggregation (such as a sum or average) over 
                  # each key, using PairRDDFunctions.aggregateByKey
        filter() # rdd.filter(_%2==0) 返回 Array(2,4)
        sample(withReplacement, fraction, seed) # withReplacement 为true(泊松分布) or false(伯努利吩咐) 表示是否进行放回取样
                                                # 根据 fraction 指定的比例，对数据进行采样，可以选择是否用随机数进行替换，seed 用于指定随机数生成器种子
        distinct() # rdd = sc.parallelize(Array(1,2,3,4,5,6,7,7,8,8,8,9))
                   # rdd.distinct.collect 返回 Array(4,6,8,2,1,3,7,9,5)
        coalesce(numPartitions, shuffle: Boolean = false) # 
        repartition(numPartitions) # 其实际内部调用了 coalesce(numPartitions, ture)
```
