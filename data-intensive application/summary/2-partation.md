## 键值数据的分区
一些分区比其他分区有更多的数据或查询 称之为 偏斜(skew) 不均衡导致的高负载分区称为热点
### 键的范围分区 Key Range
键的范围不一定均匀分布因为数据可能不均匀分布 为了均匀分配数据 分区边界需要依据数据调整 比如字典 中的 A-Z 每个字母下的单词数是不一样的

 如果主键是时间戳，则分区对应于时间范围，例如，给每天分配一个分区。 不幸的是，由于我们在测量发生时将数据从传感器写入数据库，因此所有写入操作都会转到同一个分区（即今天的分区），这样分区可能会因写入而过载，而其他分区则处于空闲状态。 可以在每个时间戳前添加传感器名称，这样会首先按传感器名称，然后按时间进行分区。 假设有多个传感器同时运行，写入负载将最终均匀分布在不同分区上。 现在，当想要在一个时间范围内获取多个传感器的值时，你需要为每个传感器名称执行一个单独的范围查询。

 ### Hash
 一致性哈希 consistent hashing

 ### 负载偏斜与热点消除
 哈希分区可以帮助减少热点 但是不能完全消除 celebrity 一样会引起同一个键的大量写入

 如果一个主键被认为是非常火爆的，一个简单的方法是在主键的开始或结尾添加一个随机数。只要一个两位数的十进制随机数就可以将主键分散为 100 种不同的主键，从而存储在不同的分区中。将主键进行分割之后，任何读取都必须要做额外的工作，因为他们必须从所有 100 个主键分布中读取数据并将其合并。此技术还需要额外的记录：只需要对少量热点附加随机数；对于写入吞吐量低的绝大多数主键来说是不必要的开销。因此，你还需要一些方法来跟踪哪些键需要被分割。

 ## 分区与次级索引
分区之后 次级索引的问题是不能整齐的映射到分区 有两种用次级索引对数据库进行分区的方法：基于文档的分区（document-based） 和 基于关键词（term-based）的分区。
### Document based
```
Partition 0:
    primary key index:
        191 -> {color:"red", make:"Honda", location:"Palo alto"}
        214 -> {color: "black", make:"Dodge", location:"san jose"}
        306 -> {color: "red", make:"Ford", location:"sunnyvale"}
    secondary indexes (Partitioned by document)
        color: black -> [214]
        color: red -> [191,306]
        color: yellow -> []
        make: Dodge -> [214]
        make: Ford -> [306]
        make: Honda -> [191]
Partition 1: (same structure)
    primary key index:
        515 -> {color: "silver", make: "Ford", location:"Milpitas"}
        768 -> {color: "red", make:"Volvo", location:"Cupertino"}
        893 -> {color: "silver", make:"Audi", location:"Santa Clara"}
    secondary indexes
        color: silver -> [515, 893]
        color: black -> []
        color: red -> [768]
        make: Audi -> [893]
        make: Volvo -> [768]
        make: Ford -> [515]
```
每个分区独立 维护自己的次级索引 仅覆盖该分区中的文档 也被称为 本地索引 因为特定品牌或者特定颜色的汽车没有放在同一个分区 查询的时候需要将请求发送到所有分区 合并所有返回结果 被称为 分散/聚集 (scatter/gather) 即使并行查询分区 分散/聚集也容易导致尾部延迟放大

然而, 它被广泛使用：MongoDB, Riak, Cassandra, Elasticsearch, SolrCloud 和 VoltDB 都使用文档分区次级索引

### Term based
创建一个覆盖所有分区数据的 全局索引 而不是给每个分区创建自己的 本地索引 

但是把这个索引存储在一个节点上 会成为瓶颈 违背了分区的目的 所以要对全局索引也进行分区 不过可以采用与主键不同的方式

```
Partition 0:
    primary key index:
        191 -> {color:"red", make:"Honda", location:"Palo alto"}
        214 -> {color: "black", make:"Dodge", location:"san jose"}
        306 -> {color: "red", make:"Ford", location:"sunnyvale"}
    secondary indexes (Partitioned by document)
        color: black -> [214]
        color: red -> [191,306,768]
        make: Dodge -> [214]
        make: Ford -> [306]
        make: Audi -> [893]
Partition 1: (same structure)
    primary key index:
        515 -> {color: "silver", make: "Ford", location:"Milpitas"}
        768 -> {color: "red", make:"Volvo", location:"Cupertino"}
        893 -> {color: "silver", make:"Audi", location:"Santa Clara"}
    secondary indexes
        color: silver -> [515, 893]
        color: yellow -> []
        make: Honda -> [191]
        make: Volvo -> [768]
```
描述了这可能是什么样子：来自所有分区的红色汽车在红色索引中，并且索引是分区的，首字母从 a 到 r 的颜色在分区 0 中，s 到 z 的在分区 1。汽车制造商的索引也与之类似（分区边界在 f 和 h 之间）

关键词分区的全局索引优于文档分区索引的地方点是它可以使读取更有效率 客户端只需要向包含关键词的分区发出请求 缺点在于写入速度较慢且较为复杂 文档中的每个关键词可能位于不同的分区或者不同的节点上 

在实践中，对全局次级索引的更新通常是 异步 的（也就是说，如果在写入之后不久读取索引，刚才所做的更改可能尚未反映在索引中）

## 分区再平衡
1. hash mod N - 成本过高
2. 固定数量的分区 - 创建比节点更多的分区，并为每个节点分配多个分区。例如，运行在 10 个节点的集群上的数据库可能会从一开始就被拆分为 1,000 个分区，因此大约有 100 个分区被分配给每个节点。 如果分区非常大，再平衡和从节点故障恢复变得昂贵。但是，如果分区太小，则会产生太多的开销。
3. 动态分区 - 键范围分区的数据库 具有固定边界的固定数量的分区将非常不便 如果出现边界错误 则可能会导致一个分区中的所有数据或者其他分区中的所有数据为空 所以动态创建分区 当分区增长到超过配置的大小时（在 HBase 上，默认值是 10GB），会被分成两个分区，每个分区约占一半的数据。与之相反，如果大量数据被删除并且分区缩小到某个阈值以下，则可以将其与相邻分区合并。此过程与 B 树顶层发生的过程类似。如果开始数据库是空的 可以 pre-splitting
4. 节点比例分区 - 每个节点具有固定数量的分区，也就是数据集变大分区也变大但是不增加节点数。 新节点加入集群 随机选择固定数量的现有分区进行拆分 然后占有这些拆分分区中每个分区的一半

手动or自动 再平衡 有人参与可以防止运维意外 - 假设一个节点过载，并且对请求的响应暂时很慢。其他节点得出结论：过载的节点已经死亡，并自动重新平衡集群，使负载离开它。这会对已经超负荷的节点，其他节点和网络造成额外的负载，从而使情况变得更糟，并可能导致级联失败。

## 请求路由 
分区完成后 需要知道连接哪个 ip 和 端口号 来读取数据 这个被称为服务发现 service discovery