replication</br>
主从：</br>
同步- 主等所有从确认写成功</br>
异步- 主给从发message但是不等从的回应</br>
同步的缺点在于一个从节点崩溃不给回应，则主会block所有写入直到从再次可用. 鉴于此 一般 synchronous replication 都是一个从同步 其他异步。这种配置有时也被称为 semi-synchronous.</br>
follower failure - recovery
1. leader snapshot 拷贝给 新的 follower node
2. follower 从 snapshot获取replication log(bin log) 的准确位置 
3. When the follower has processed the backlog of data changes since the snapshot, we say it has caught up
leader failure - failover
1. 确定leader是不是挂了(心跳)
2. 选择新 leader(raft)
3. 重新配置系统使用新leader


read-through/write-through (rt/wt): this is where the application treats cache as the main data store and reads data from it and writes data to it. the cache is responsible for reading and writing this data to the database, thereby relieving the application of this responsibility.
Cache-Aside cache missing app will go to DB
Write-behind 写入缓存 等缓存自己 flush 到DB