



# Shared-Nothing Architectures
一种计算机系统和分布式系统的设计范式在这种架构下，系统中的不同组件或节点之间不共享任何资源，每个节点都是独立的，并且在处理数据和请求时相互隔离。这种设计方式主要用于构建高可扩展性、高性能和容错性的分布式系统。

通常用于以下场景:
* 分布式数据库系统:
* 大规模web服务:
* 数据分析系统:


There are various reasons why you might want to distribute a database across multiple machines
1. Scalability<br>
If your data volume, read load, or write load grows bigger than a single machine can handle, you can potentially spread the load across multiple machines.
2. Fault tolerance/high availability<br>
If your application needs to continue working even if one machine (or several machines, or the network, or an entire datacenter) goes down, you can use multi‐ ple machines to give you redundancy. When one fails, another one can take over.
3.  Latency<br>
If you have users around the world, you might want to have servers at various locations worldwide so that each user can be served from a datacenter that is geo‐ graphically close to them. That avoids the users having to wait for network pack‐ ets to travel halfway around the world.

Each machine or virtual machine running the database software is called a node.

All of the difficulty in replication lies in handling changes to replicated data.

We will discuss three popular algorithms for replicating changes between nodes:<br> 
1. single-leader
2. multi-leader
3. leaderless  

Replication. Almost all distributed databases use one of these three approaches.

## Leaders and Followers
存储了数据库拷贝的每个节点被称为 副本(replica). 
主从 or leader-based replication
1. write 走主库
2. 其他副本为 follower, also called read replica, slaves. 当领导者将新数据写入本地存储时，它也会将数据变更发送给所有的追随者，称之为 复制日志（replication log） 或 变更流（change stream）。每个跟随者从领导者拉取日志，并相应更新其本地数据库副本，方法是按照与领导者相同的处理顺序来进行所有写入.
3. 当客户想要从数据库中读取数据时，它可以向领导者或任一追随者进行查询。但只有领导者才能接受写入操作（从客户端的角度来看从库都是只读的）
这种复制模式是许多关系数据库的内置功能, 如PostgreSQL, MySQL etc. Kafka and RabbitMQ also use it.

### 同步复制与异步复制
如果同步从库没有响应（比如它已经崩溃，或者出现网络故障，或其它任何原因），主库就无法处理写入操作。主库必须阻止所有写入，并等待同步副本再次可用。因此实际上，如果在数据库上启用同步复制，通常意味着其中 一个 从库是同步的，而其他的从库则是异步的。如果该同步从库变得不可用或缓慢，则将一个异步从库改为同步运行。这保证你至少在两个节点上拥有最新的数据副本：主库和同步从库。 这种配置有时也被称为 半同步(semi-synchronous)。通常情况下，基于领导者的复制都配置为完全异步。缺点: 主库失效数据丢失. 优点: 主库可以一直处理写入. 

synchronous: The leader waits until follower has confirmed that it received the write before reporting success to the user<br>
asynchronous: The leader sends the message, but doesn’t wait for a response from the follower

The advantage of synchronous replication is that the follower is guaranteed to have an up-to-date copy of the data that is consistent with the leader. If the leader sud‐ denly fails, we can be sure that the data is still available on the follower. The disadvantage is that if the synchronous follower doesn’t respond (because it has crashed, or there is a network fault, or for any other reason), the write cannot be processed. The leader must block all writes and wait until the synchronous replica is available again.

For that reason, it is impractical for all followers to be synchronous: any one node outage would cause the whole system to grind to a halt. In practice, if you enable synchronous replication on a database, it usually means that one of the followers is synchronous, and the others are asynchronous. If the synchronous follower becomes unavailable or slow, one of the asynchronous followers is made synchronous. This guarantees that you have an up-to-date copy of the data on at least two nodes: the leader and one synchronous follower. This configuration is sometimes also called semi-synchronous.

### 设置新从库
有时候需要设置一个新的从库：也许是为了增加副本的数量，或替换失败的节点。如何确保新的从库拥有主库数据的精确副本？\
可以通过锁定数据库即暂停写入来使磁盘文件保持一致, 但违背高可用. 一般来讲设置新从库通常不需要停机:
1. 获取主库的一致性快照
2. 快照复制到新的从库节点
3. 从库连接到主库, 并拉取快照之后发生的所有数据变更. 这要求快照与主库复制日志中的位置精确关联。该位置有不同的名称，例如 PostgreSQL 将其称为 日志序列号（log sequence number，LSN），MySQL 将其称为 二进制日志坐标（binlog coordinates）。
4. 当从库处理完快照之后积累的数据变更，我们就说它 赶上（caught up） 了主库，现在它可以继续及时处理主库产生的数据变化了。
### Handling Node Outages

#### Leader failure: Failover
Handling a failure of the leader is trickier: one of the followers needs to be promoted to be the new leader, clients need to be reconfigured to send their writes to the new leader, and the other followers need to start consuming data changes from the new leader. This process is called <span style="color:red">failover</span>.

1. Determining that the leader has failed. (通常情况 心跳检测)
2. Choosing a new leader. (好多算法比如 raft)
3. Reconfiguring the system to use the new leader.

切换过程中有很多地方可能会出错:
* 异步复制-新主库可能没有收到老朱库宕机前最后的写入. 选出新主库后, 老主库重新加入集群, 新主库再次期间可能会收到写入冲突. 最简单的解决方案是丢弃老主库未复制的写入, 但是会打破客户对于数据持久性的期望.
* 如果数据库需要和其他外部存储相协调，那么丢弃写入内容是极其危险的操作。在 GitHub 的一场事故中，一个过时的 MySQL 从库被提升为主库。数据库使用自增 ID 作为主键，因为新主库的计数器落后于老主库的计数器，所以新主库重新分配了一些已经被老主库分配掉的 ID 作为主键。这些主键也在 Redis 中使用，主键重用使得 MySQL 和 Redis 中的数据产生不一致，最后导致一些私有数据泄漏到错误的用户手中。
* 发生某些故障时可能会出现两个节点都以为自己是主库的情况。这种情况称为 脑裂（split brain），非常危险：如果两个主库都可以接受写操作，却没有冲突解决机制（请参阅 “多主复制”），那么数据就可能丢失或损坏。一些系统采取了安全防范措施：当检测到两个主库节点同时存在时会关闭其中一个节点，但设计粗糙的机制可能最后会导致两个节点都被关闭
* 主库被宣告死亡之前的正确超时应该怎么配置？在主库失效的情况下，超时时间越长意味着恢复时间也越长。但是如果超时设置太短，又可能会出现不必要的故障切换。例如，临时的负载峰值可能导致节点的响应时间增加到超出超时时间，或者网络故障也可能导致数据包延迟。如果系统已经处于高负载或网络问题的困扰之中，那么不必要的故障切换可能会让情况变得更糟糕

以上问题再ch8和ch9有详细讨论

### Implementation of Replication Logs
基于领导者的复制在底层是如何工作的？实践中有好几种不同的复制方式
#### 基于语句的复制 Statement-based replication

The leader logs every write request (statement) that it executes and sends that statement log to its followers. 主库记录下它执行的每个写入请求（语句，即 statement）并将该语句日志发送给从库。对于关系数据库来说，这意味着每个 INSERT、UPDATE 或 DELETE 语句都被转发给每个从库，每个从库解析并执行该 SQL 语句，就像直接从客户端收到一样\
There are various ways in which this approach to replication can break down. 虽然听上去很合理，但有很多问题会搞砸这种复制方式:
* such as NOW() to get the current date and time or RAND() to get a random number, is likely to generate a different value on each replica.
* If statements use an autoincrementing column, or if they depend on the existing data in the database (e.g., UPDATE ... WHERE <some condition>), they must be executed in exactly the same order on each replica, or else they may have a differ‐ ent effect. This can be limiting when there are multiple concurrently executing transactions. 如果语句使用了 自增列（auto increment），或者依赖于数据库中的现有数据（例如，UPDATE ... WHERE <某些条件>），则必须在每个副本上按照完全相同的顺序执行它们，否则可能会产生不同的效果。当有多个并发执行的事务时，这可能成为一个限制。
* Statements that have side effects (e.g., triggers, stored procedures, user-defined functions) may result in different side effects occurring on each replica, unless the side effects are absolutely deterministic. 有副作用的语句（例如：触发器、存储过程、用户定义的函数）可能会在每个副本上产生不同的副作用，除非副作用是绝对确定性的

We can have work around with these issues, but there are so many edge cases.  Other replication methods are now generally preferred.

#### 传输预写式日志 WAL (Write ahead log)
写操作追加到日志中
* 对于日志结构存储引擎（请参阅 “SSTables 和 LSM 树”），日志是主要的存储位置。日志段在后台压缩，并进行垃圾回收。
* 对于覆写单个磁盘块的 B 树，每次修改都会先写入 预写式日志（Write Ahead Log, WAL），以便崩溃后索引可以恢复到一个一致的状态。
Leader sends log to followers.   \
The main disadvantage is that the log describes the data on a very low level: a WAL contains details of which bytes were changed in which disk blocks. This makes replication closely coupled to the storage engine

#### 逻辑日志复制(基于行)
复制和存储引擎使用不同的日志格式，这样可以将复制日志从存储引擎的内部实现中解耦出来。这种复制日志被称为逻辑日志（logical log），以将其与存储引擎的（物理）数据表示区分开来。
* 对于插入的行，日志包含所有列的新值。
* 对于删除的行，日志包含足够的信息来唯一标识被删除的行，这通常是主键，但如果表上没有主键，则需要记录所有列的旧值。
* 对于更新的行，日志包含足够的信息来唯一标识被更新的行，以及所有列的新值（或至少所有已更改的列的新值）。

修改多行的事务会生成多条这样的日志记录，后面跟着一条指明事务已经提交的记录。 MySQL 的二进制日志（当配置为使用基于行的复制时）使用了这种方法

对于外部应用程序来说，逻辑日志格式也更容易解析。如果要将数据库的内容发送到外部系统，例如复制到数据仓库进行离线分析，或建立自定义索引和缓存，这一点会很有用。这种技术被称为 数据变更捕获（change data capture），第十一章 将重新讲到它。
#### 基于触发器的复制
基于触发器的数据库复制是一种特定的数据复制技术，它通过使用触发器（Triggers）来捕捉数据库上的数据变更，并将这些变更传递到其他数据库实例，从而实现数据的复制和同步。
1. 创建触发器：在源数据库中，创建触发器以监视表上的数据变更（如插入、更新、删除操作）
2. 触发器响应：当在源数据库上进行数据操作时，触发器会被激活，并执行相应的操作。
3. 数据传递：触发器执行后，它会将数据变更的信息（例如，哪些数据被插入、更新或删除）传递给目标数据库
4. 目标数据库上执行相应操作：目标数据库接收到数据变更的信息后，执行与源数据库上相同的数据操作，从而使目标数据库的数据与源数据库保持同步。

## Problems with Replication Lag
基于领导者的复制要求所有写入都由单个节点处理，但只读查询可以由任何一个副本来处理。所以对于读多写少的场景（Web 上的常见模式），一个有吸引力的选择是创建很多从库，并将读请求分散到所有的从库上去。这样能减小主库的负载，并允许由附近的副本来处理读请求。

在这种读伸缩（read-scaling）的体系结构中，只需添加更多的从库，就可以提高只读请求的服务容量。但是，这种方法实际上只适用于异步复制 —— 如果尝试同步复制到所有从库，则单个节点故障或网络中断将导致整个系统都无法写入。而且节点越多越有可能出现个别节点宕机的情况，所以完全同步的配置将是非常不可靠的

当应用程序从异步从库读取时，如果从库落后，它可能会看到过时的信息。这会导致数据库中出现明显的不一致：同时对主库和从库执行相同的查询，可能得到不同的结果，因为并非所有的写入都反映在从库中。这种不一致只是一个暂时的状态 —— 如果停止写入数据库并等待一段时间，从库最终会赶上并与主库保持一致。出于这个原因，这种效应被称为 最终一致性（eventual consistency）

因为滞后时间太长引入的不一致性，不仅仅是一个理论问题，更是应用设计中会遇到的真实问题。本节将重点介绍三个在复制延迟时可能发生的问题实例，并简述解决这些问题的一些方法。
### read-after-write consistency (also called read-your-writes consistency)
如果用户在写入后马上就查看数据，则新数据可能尚未到达副本。对用户而言，看起来好像是刚提交的数据丢失了
1. 对于用户 可能修改过 的内容，总是从主库读取. 比如: 社交网络上的用户个人资料信息通常只能由用户本人编辑，而不能由其他人编辑。因此一个简单的规则就是：总是从主库读取用户自己的档案，如果要读取其他用户的档案就去从库。
2. 如果应用中的大部分内容都可能被用户编辑，那这种方法就没用了，因为大部分内容都必须从主库读取（读伸缩就没效果了）。在这种情况下可以使用其他标准来决定是否从主库读取。例如可以跟踪上次更新的时间，在上次更新后的一分钟内，从主库读。还可以监控从库的复制延迟，防止向任何滞后主库超过一分钟的从库发出查询。
3. 客户端可以记住最近一次写入的时间戳，系统需要确保从库在处理该用户的读取请求时，该时间戳前的变更都已经传播到了本从库中。如果当前从库不够新，则可以从另一个从库读取，或者等待从库追赶上来。这里的时间戳可以是逻辑时间戳（表示写入顺序的东西，例如日志序列号）或实际的系统时钟
4. 如果你的副本分布在多个数据中心（为了在地理上接近用户或者出于可用性目的），还会有额外的复杂性。任何需要由主库提供服务的请求都必须路由到包含该主库的数据中心

### Monotonic Reads 单调读
用户首先从新副本读取，然后从旧副本读取。时间看上去回退了。为了防止这种异常，我们需要单调的读取。
Make sure that each user always makes their reads from the same replica.<br>
这是一个比 强一致性（strong consistency） 更弱，但比 最终一致性（eventual consistency） 更强的保证。\
实现单调读的一种方式是确保每个用户总是从同一个副本进行读取（不同的用户可以从不同的副本读取）。例如，可以基于用户 ID 的散列来选择副本，而不是随机选择副本。但是，如果该副本出现故障，用户的查询将需要重新路由到另一个副本

### Consistent Prefix Reads
This guarantee says that if a sequence of writes happens in a certain order, then anyone reading those writes will see them appear in the same order.


## Multi-Leader Replication
In this setup, each leader simultaneously acts as a follower to the other leaders.

### Use Cases for Multi-Leader Replication
### Multi-datacenter operation
如果使用常规的基于领导者的复制设置，主库必须位于其中一个数据中心，且所有写入都必须经过该数据中心。\
between datacenters, each datacenter’s leader replicates its changes to the leaders in other datacenters asynchronously.\
单主和多主在多个数据中心时:
1. 性能 - 在单主配置中，每个写入都必须穿过互联网，进入主库所在的数据中心。这可能会增加写入时间，并可能违背了设置多个数据中心的初心。在多主配置中，每个写操作都可以在本地数据中心进行处理，并与其他数据中心异步复制。因此，数据中心之间的网络延迟对用户来说是透明的，这意味着感觉到的性能可能会更好。
2. 容忍数据中心停机 - 在单主配置中，如果主库所在的数据中心发生故障，故障切换必须使另一个数据中心里的从库成为主库。在多主配置中，每个数据中心可以独立于其他数据中心继续运行，并且当发生故障的数据中心归队时，复制会自动赶上。
3. 容忍网络问题 - 数据中心之间的通信通常穿过公共互联网，这可能不如数据中心内的本地网络可靠。单主配置对数据中心之间的连接问题非常敏感，因为通过这个连接进行的写操作是同步的。采用异步复制功能的多主配置通常能更好地承受网络问题：临时的网络中断并不会妨碍正在处理的写入。

尽管多主复制有这些优势，但也有一个很大的缺点：两个不同的数据中心可能会同时修改相同的数据，写冲突是必须解决的

由于多主复制在许多数据库中都属于改装的功能，所以常常存在微妙的配置缺陷，且经常与其他数据库功能之间出现意外的反应。比如自增主键、触发器、完整性约束等都可能会有麻烦。因此，多主复制往往被认为是危险的领域，应尽可能避免
#### Clients with offline operation
Calendar apps on your mobile phone, your laptop, and other devices. You need to be able to see your meetings (make read requests) and enter new meetings (make write requests) at any time, regardless of whether your device currently has an internet connection

多设备的离线模式，每个设备被看作一个 datacenter，本地一个小的数据库 存放calendar app 的信息。 有网络连接的时候就把信息同步到其他设备。 从架构来看是一个 multi-leader 的架构， 每个设备都是一个 datacenter 并且也是唯一的leader

#### Collaborative editing  (Online Document Editing)
We don’t usually think of collaborative editing as a database replication problem, but it has a lot in common with the previously mentioned offline editing use case. When one user edits a document, the changes are instantly applied to their local replica (the state of the document in their web browser or client application) and asynchronously replicated to the server and any other users who are editing the same document.

### Handling Write Conflicts
多主复制的最大问题是可能发生写冲突，这意味着需要解决冲突。\
俩人同时修改 wiki 页面 title 一个改 B 一个改 C conflict 发生
#### Synchronous versus asynchronous conflict detection
synchronous detection 会退化到 single leader replication
#### Conflict avoidance
用户只到指定的 datacenter。 Different user have different home datacenters, but from any one user’s point of view the configuration is essentially single-leader.

However, sometimes you might want to change the designated leader for a record.
Perhaps because one datacenter has failed and you need to reroute traffic to another datacenter, or perhaps because a user has moved to a different location and is now closer to a different datacenter. In this situation, conflict avoidance breaks down, and you have to deal with the possibility of concurrent writes on different leaders.

#### Converging toward a consistent state
If each replica simply applied writes in the order that it saw the writes, the database would end up in an inconsistent state: the final value would be C at leader 1 and B at leader 2.

Thus, the database must resolve the conflict in a convergent way, which means that all replicas must arrive at the same final value when all changes have been replicated.
1. 给每个写入一个唯一的 ID（例如时间戳、长随机数、UUID 或者键和值的哈希），挑选最高 ID 的写入作为胜利者，并丢弃其他写入。如果使用时间戳，这种技术被称为 最后写入胜利（LWW, last write wins）。虽然这种方法很流行，但是很容易造成数据丢失
2. 为每个副本分配一个唯一的ID，ID编号更高的写入具有更高的优先级
3. 合并 比如(B/C)
4. 用一种可保留所有信息的显式数据结构来记录冲突，并编写解决冲突的应用程序代码

#### 自定义冲突解决逻辑
解决冲突的最合适的方法可能取决于应用程序，大多数多主复制工具允许使用应用程序代码编写冲突解决逻辑。该代码可以在写入或读取时执行
* 写时执行 - 只要数据库系统检测到复制更改日志中存在冲突，就会调用冲突处理程序。例如，Bucardo 允许你为此编写一段 Perl 代码。这个处理程序通常不能提示用户 —— 它在后台进程中运行，并且必须快速执行。
* 读时执行 - 当检测到冲突时，所有冲突写入被存储。下一次读取数据时，会将这些多个版本的数据返回给应用程序。应用程序可以提示用户或自动解决冲突，并将结果写回数据库。例如 CouchDB 就以这种方式工作。

### multi-leader topology 多主复制拓扑
![topology](./pic/topology.png)
A problem with circular and star topologies is that if just one node fails, it can interrupt the flow of replication messages between other nodes, causing them to be unable to communicate until the node is fixed.

All-to-all topology has issue as well. Assume client A inserts a row into a table on leader 1, client B updates that row on leader 3. However leader 2 receives update first, then receives insert. 这是一个因果关系的问题，类似于我们在 “一致前缀读” 中看到的：更新取决于先前的插入，所以我们需要确保所有节点先处理插入，然后再处理更新。仅仅在每一次写入时添加一个时间戳是不够的，因为时钟不可能被充分地同步，所以主库 2 就无法正确地对这些事件进行排序（见 第八章）。要正确排序这些事件，可以使用一种称为 版本向量（version vectors） 的技术，本章稍后将讨论这种技术

## Leaderless Replication
我们在本章到目前为止所讨论的复制方法 —— 单主复制、多主复制 —— 都是这样的想法：客户端向一个主库发送写请求，而数据库系统负责将写入复制到其他副本。主库决定写入的顺序，而从库按相同顺序应用主库的写入

Amazon used leaderless for its in-house Dynamo system. Riak, Cassandra, and Voldemort are open source datastores with leaderless replication models inspired by Dynamo, so this kind of database is also known as Dynamo-style.

在一些无主复制的实现中，客户端直接将写入发送到几个副本中，而另一些情况下，由一个 协调者（coordinator） 节点代表客户端进行写入。但与主库数据库不同，协调者不执行特定的写入顺序。我们将会看到，这种设计上的差异对数据库的使用方式有着深远的影响。

### Writing to the Database When a Node Is Down 当节点故障时写入数据库
如果是带主的副本复制, 在你有3个副本的时候, 其中一个副本不可用 或者 正在重新启动以安装系统更新, 如果要继续处理写入, 可能需要执行故障切换. 

无主配置不存在故障转移, 当其中2个可用副本接受写入, 可以认为写入成功. 不可用的节点重新联机，客户端开始读取它。节点关闭期间发生的任何写入都不在该节点上。因此，如果你从该节点读取数据，则可能会从响应中拿到陈旧的（过时的）值. 为了解决这个问题，当一个客户端从数据库中读取数据时，它不仅仅把它的请求发送到一个副本：读请求将被并行地发送到多个节点。客户可能会从不同的节点获得不同的响应，即来自一个节点的最新值和来自另一个节点的陈旧值。版本号将被用于确定哪个值是更新的. 

Client sends write to all replicas in parallel, if client receive major (often more than half) ok responses, we consider write to be successful.
#### 读修复和反熵
What happens to the node when it comes back online? 
Two mechanisms are often used in Dynamo-style datastores:

1. Read repair<br>
User gets a version 6 value from replica 1 and version 7 value from replica 2 and replica 3. The client sees that replica 1 has a stale value and writes the newer value back to that replica. This approach works well for values that are frequently read.
2. Anti-entropy process<br>
Some datastores have a background process that constantly looks for differences in the data between replicas and copies any missing data from one replica to another. Unlike the replication log in leader-based replication, this anti-entropy process does not copy writes in any particular order, and there may be a significant delay before data is copied.

#### 读写的法定人数
Quorums |ˈkwɔrəm| for reading and <br>
n total nodes<br>
w nodes to confirm write success<br>
r nodes to make sure your query has at least 1 up-to-date value<br>
Usually w=r=(n+1)/2 (rounded up, and n usually is odd number)

w + r > n, at least one of the r replicas you read from must have seen the most recent successful write



### 法定人数一致性的局限性

However w + r > is not the universal key:
1. If a sloppy quorum is used, write 可能发生在 n 个节点之外的节点, 这时候的读操作 读不到写入的值
2. If two writes occur concurrently, 不清楚哪一个先发生。在这种情况下，唯一安全的解决方案是合并并发写入. 如果根据时间戳（最后写入胜利）挑选出一个胜者，则写入可能由于时钟偏差【35】而丢失。我们将在 “检测并发写入” 继续讨论此话题。 
3. If a write happens concurrently with a read, the write may be reflected on only some of the replicas. In this case, it’s undetermined whether the read returns the old or the new value.
4. If a write succeeded on some replicas but failed on others, 写成功不到 w 失败. 但是已经被写入的节点不会回滚。This means that if a write was reported as failed, subsequent reads may or may not return the value from that write
5. If a node carrying a new value fails, and its data is restored from a replica carrying an old value, the number of replicas storing the new value may fall below w, breaking the quorum condition.

如果可用的节点少于所需的 w 或 r，则写入或读取将返回错误。节点可能由于多种原因而不可用，比如：节点关闭（异常崩溃，电源关闭）、操作执行过程中的错误（由于磁盘已满而无法写入）、客户端和服务器节点之间的网络中断或任何其他原因。我们只需要关心节点是否返回了成功的响应，而不需要区分不同类型的错误。

### Sloppy Quorums and Hinted Handoff
合理配置的法定人数可以使数据库无需故障切换即可容忍个别节点的故障。它也可以容忍个别节点变慢，因为请求不必等待所有 n 个节点响应 —— 当 w 或 r 个节点响应时它们就可以返回。对于需要高可用、低延时、且能够容忍偶尔读到陈旧值的应用场景来说，这些特性使无主复制的数据库很有吸引力

然而，法定人数（如迄今为止所描述的）并不像它们可能的那样具有容错性。网络中断可以很容易地将客户端从大量的数据库节点上切断。虽然这些节点是活着的，而其他客户端可能也能够连接到它们，但是从数据库节点切断的客户端来看，它们也可能已经死亡。在这种情况下，剩余的可用节点可能会少于 w 或 r，因此客户端不再能达到法定人数。


In a large cluster (with significantly more than n nodes, 意思是20个replicas 但是只指定n=10, 特指在宽松法定人数环境下?) it’s likely that the client can connect to some database nodes during the network interruption, just not to the nodes that it needs to assemble a quorum for a particular value. 网络中断期间客户端可能仍能连接到一些数据库节点，但又不足以组成一个特定的法定人数. In that case, database designers face a trade-off:
* Is it better to return errors to all requests for which we cannot reach a quorum of w or r nodes?
* Or should we accept writes anyway, and write them to some nodes that are reachable but aren’t among the n nodes on which the value usually lives? 如果允许写入继续，那么这些写入请求将被发送到一些仍然可达的节点上，即使这些节点并不是通常情况下数据所存储的那 n 个节点。

The latter is known as a <span style="color:red">sloppy quorum</span>: writes and reads still require w and r successful responses, but those may include nodes that are not among the designated n “home” nodes for a value. Once the network interruption is fixed, any writes that one node temporarily accepted on behalf of another node are sent to the appropriate “home” nodes. This is called <span style="color:red">hinted handoff</span>

Sloppy quorums are particularly useful for increasing write availability: as long as any w nodes are available, the database can accept writes. However, this means that even when w + r > n, you cannot be sure to read the latest value for a key, because the latest value may have been temporarily written to some nodes outside of n.

因此，在传统意义上，宽松的法定人数实际上并不是法定人数。它只是一个持久性的保证，即数据已存储在某处的 w 个节点。但不能保证 r 个节点的读取能看到它，除非提示移交已经完成。

在所有常见的 Dynamo 实现中，宽松的法定人数是可选的。在 Riak 中，它们默认是启用的，而在 Cassandra 和 Voldemort 中它们默认是禁用的


#### Multi-datacenter leaderless replica
Cassandra and Voldemort: the number of replicas n includes nodes in all datacenters, and in the configuration you can specify how many of the n replicas you want to have in each datacenter.

Riak keeps all communication between clients and database nodes local to one data‐ center, so n describes the number of replicas within one datacenter. Cross-datacenter replication between database clusters happens asynchronously in the background, in a style that is similar to multi-leader replication

Cassandra 和 Voldemort 在正常的无主模型中实现了他们的多数据中心支持：副本的数量 n 包括所有数据中心的节点，你可以在配置中指定每个数据中心所拥有的副本的数量。无论数据中心如何，每个来自客户端的写入都会发送到所有副本，但客户端通常只等待来自其本地数据中心内的法定节点的确认，从而不会受到跨数据中心链路延迟和中断的影响。对其他数据中心的高延迟写入通常被配置为异步执行，尽管该配置仍有一定的灵活性。

Riak 将客户端和数据库节点之间的所有通信保持在一个本地的数据中心，因此 n 描述了一个数据中心内的副本数量。数据库集群之间的跨数据中心复制在后台异步发生，其风格类似于多主复制。


### Detecting Concurrent Writes
the server can determine whether two operations are concurrent by looking at the version numbers—it does not need to interpret the value itself (so the value could be any data structure). The algorithm works as follows:
#### 最后写入胜利（丢弃并发写入）
可以为每个写入附加一个时间戳，然后挑选最大的时间戳作为 “最近的”，并丢弃具有较早时间戳的任何写入。这种冲突解决算法被称为 最后写入胜利（LWW, last write wins），是 Cassandra 唯一支持的冲突解决方法, 也是 Riak 中的一个可选特征. 此外，LWW 甚至可能会丢弃不是并发的写入，我们将在 “有序事件的时间戳” 中进行讨论. 

在类似缓存的一些情况下，写入丢失可能是可以接受的。但如果数据丢失不可接受，LWW 是解决冲突的一个很烂的选择。

在数据库中使用 LWW 的唯一安全方法是确保一个键只写入一次，然后视为不可变，从而避免对同一个键进行并发更新。例如，Cassandra 推荐使用的方法是使用 UUID 作为键，从而为每个写操作提供一个唯一的键

#### “此前发生”的关系和并发
只要有两个操作A和B, 就有三种可能: A 在 B 之前发生, 或者 B 在 A 之前发生 或者 A 和 B 并发. 我们需要的是一个算法来告诉我们两个操作是否是并发的。如果一个操作发生在另一个操作之前，则后面的操作应该覆盖前面的操作，但是如果这些操作是并发的，则存在需要解决的冲突。
```
如果两个操作 “同时” 发生，似乎应该称为并发 —— 但事实上，它们在字面时间上重叠与否并不重要。由于分布式系统中的时钟问题，现实中是很难判断两个事件是否是 同时 发生的，这个问题我们将在 第八章 中详细讨论。

为了定义并发性，确切的时间并不重要：如果两个操作都意识不到对方的存在，就称这两个操作 并发，而不管它们实际发生的物理时间
```

#### 捕获"此前发生"关系
* 服务器为每个键保留一个版本号，每次写入键时都增加版本号，并将新版本号与写入的值一起存储。
* 当客户端读取键时，服务器将返回所有未覆盖的值以及最新的版本号。客户端在写入前必须读取。
* 客户端写入键时，必须包含之前读取的版本号，并且必须将之前读取的所有值合并在一起。 （来自写入请求的响应可以像读取一样，返回所有当前值，这使得我们可以像购物车示例那样连接多个写入。）
* 当服务器接收到具有特定版本号的写入时，它可以覆盖该版本号或更低版本的所有值（因为它知道它们已经被合并到新的值中），但是它必须保持所有值更高版本号（因为这些值与传入的写入同时发生）。

当一个写入包含前一次读取的版本号时，它会告诉我们的写入是基于之前的哪一种状态。如果在不包含版本号的情况下进行写操作，则与所有其他写操作并发，因此它不会覆盖任何内容 —— 只会在随后的读取中作为其中一个值返回。

![concurrency_detect](./pic/concurrency_detect.png)

#### 合并并发写入的值
这种算法可以确保没有数据被无声地丢弃，但不幸的是，客户端需要做一些额外的工作：客户端随后必须合并并发写入的值。 Riak 称这些并发值为 兄弟（siblings）。

合并并发值，本质上是与多主复制中的冲突解决问题相同，我们先前讨论过（请参阅 “处理写入冲突”）。一个简单的方法是根据版本号或时间戳（最后写入胜利）来选择一个值，但这意味着丢失数据。所以，你可能需要在应用程序代码中额外做些更聪明的事情。

以购物车为例，一种合理的合并值的方法就是做并集。在 图 5-14 中，最后的两个兄弟是 [牛奶，面粉，鸡蛋，熏肉] 和 [鸡蛋，牛奶，火腿]。注意牛奶和鸡蛋虽然同时出现在两个并发值里，但他们每个只被写过一次。合并的值可以是 [牛奶，面粉，鸡蛋，培根，火腿]，不再有重复了。

如果你合并了两个客户端的购物车，并且只在其中一个客户端里面移除了一个项目，那么被移除的项目将会重新出现在这两个客户端的交集结果中。为了防止这个问题，要移除一个项目时不能简单地直接从数据库中删除；相反，系统必须留下一个具有适当版本号的标记，以在兄弟合并时表明该项目已被移除。这种删除标记被称为 墓碑（tombstone）

#### 版本向量
图 5-13 中的示例只使用了一个副本。当有多个副本但又没有主库时，算法该如何修改？相反，除了对每个键，我们还需要对 每个副本 使用版本号。每个副本在处理写入时增加自己的版本号，并且跟踪从其他副本中看到的版本号。这个信息指出了要覆盖哪些并发值，以及要保留哪些并发值或兄弟值。

所有副本的版本号集合称为 版本向量（version vector）【56】。这个想法的一些变体正在被使用，但最有趣的可能是在 Riak 2.0 【58,59】中使用的 虚线版本向量（dotted version vector）【57】。我们不会深入细节，但是它的工作方式与我们在购物车示例中看到的非常相似。

与 图 5-13 中的版本号一样，当读取值时，版本向量会从数据库副本发送到客户端，并且随后写入值时需要将其发送回数据库。（Riak 将版本向量编码为一个字符串，并称其为 因果上下文，即 causal context）。版本向量允许数据库区分覆盖写入和并发写入。

另外，就像在单个副本中的情况一样，应用程序可能需要合并并发值。版本向量结构能够确保从一个副本读取并随后写回到另一个副本是安全的。这样做虽然可能会在其他副本上面创建数据，但只要能正确合并就不会丢失数据。