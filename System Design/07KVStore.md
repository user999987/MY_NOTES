### Data Partition
2 problems need to solve:
1. Distribute data across multiple servers evenly
2. minimize the data movement when nodes are added or removed

Answer is consistent hashing. 

### Data replication
after a key is mapped to a position on the hash ring, walk clockwise and choose the first N servers on the ring to store data copies. With virtual nodes, the first n nodes on the ring may be owned by fewer than N physical servers. To avoid this issue, we only choose unique servers while performing the clockwise walk logic.

### Consistency
Since data is replicated at multiple nodes, it must be synchronized across replicas. Quorum consensus:
* N = number of replicas
* W = For a write operation to be considered as successful, write operation must be acknowledged from W replicas.
* R = For a read operation to be considered as successful, read operation must wait for responses from at least R replicas.

W = 1 does not mean data is written on one server. When N is 3, W=1 means that the coordinator must receive at least one acknowledgement before the write operation is considered as successful. 

The configuration of W, R and N is a typical tradeoff between latency and consistency.
* W + R > N, strong consistency is is guaranteed because there must be at least one overlapping node that has the latest data to ensure consistency.
* R = 1, W = N, fast read
* R = N, W = 1, fast write