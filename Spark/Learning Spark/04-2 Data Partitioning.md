Partitioning will not be helpful in all applications - for example, if a given RDD is scanned only once, there is no point in partitioning it in advance. It is useful only when a data set is reused ***multiple times*** in key-oriented operations such as joins.

Spark's partitioning is available on all RDDs of key/value pairs, and causes the system to group elements based on a function of each key.

Spark does not give explicit control of which worker node each key goes to, it lets the program ensure that a set of keys will appear together on some node. It lets the program ensure that a set of keys will appear together on some node. 
For example:
* you might choose to has-partition an RDD into 100 partitions so that keys that have the same hash value modulo 100 appear on the same node.
* you might range-partition the RDD into sorted ranges of keys so that elements with keys in the same range appear on the same node.

Example- large table of user information in memory, an RDD of (UserID, UserInfo) pairs, where UserInfo contains a list of topics the user is subscribed to. The applications periodically combines this table with a smaller file representing events that happened in the past five minutes, table of (UserID, LinkInfo). We may want to count how many users visitied a link that was not to one of their subscribed topics. Can do join operation to group the UserInfo and LinkInfo by key UserID

```
Scala example
val sc = new SparkContext(...)
val userData = sc.sequenceFile[UserID, UserInfo]("hdfs://...").persist()
// Function called periodically to process a logfile of events in the past 5 minutes;
// we assume that this is a SequenceFile containing (UserID, LinkInfo) pairs.
def processNewLogs(logFileName: String) {
    val events = sc.sequenceFile[UserID, LinkInfo](logFileName)
    val joined = userData.join(events)// RDD of (UserID, (UserInfo, LinkInfo)) pairs 
    val offTopicVisits = joined.filter {
        case (userId, (userInfo, linkInfo)) => // Expand the tuple into its components 
            !userInfo.topics.contains(linkInfo.topic)
        }.count()
println("Number of visits to non-subscribed topics: " + offTopicVisits) }
```
join() operation do not know anything about how the keys are partitioned in the datasets. 
By default this operation will hash all the keys of both datasets, sending elements with the same key hash across the network to the same machine, and then join together the elements with the same key on that machine.

userData table is hashed and shuffled across the network on every call, it is a waste.
```
Scala example
val sc = new SparkContext(...)
val userData = sc.sequenceFile[UserID, UserInfo]("hdfs://...")
    .partitionBy(new HashPartitioner(100)) // Create 100 partitions 
    .persist()
```
Spark will now know that is is hash-partitioned, and calls to join() on it will take advantage of this information. In particular, when we call userData.join(events), Spark will shuffle only the events RDD, sending events with each particular UserID to the machine that contains the corresponding hash partition of userData. The result is that a lot less data is communicated over the network, and the program runs significantly faster.


sortByKey() and groupByKey() will result in range-partitioned and hash-partitioned RDDs, which means it can take advantage of above operations.
On the other hand, operations like ***map()*** cause the New RDD to forget the parent's partitioning information, because such operations could thoeoretically modify the key for each record.

To maximize the potential for partitioning-related optimizations, you should use mapValues() or flatMapValues() whenever you are not changing an element’s key.