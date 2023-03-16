1. leader election
每个节点有一个 timeout 监听 leader 心跳包 没有收到则申请成为 新的 leader term更新(就是+1)
2. log replication 
内容随 heartbeat 一起发送，有 2 阶段 1- log entry 2- commit
3. safty
safty 包含 2 个问题
* 竞选失败- 随机一个 timeout 再次竞选
* 发生分区- 奇数个节点 总能有一个分区取到 majority，除非分区成 3 块，那也没辙