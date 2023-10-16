### Compute Layer
The compute layer, or the processing layer, allows various applications to communicate with Kafka brokers via APIs. 
### Storage Layer
This layer is composed of Kafka brokers. Kafka brokers run on a cluster of servers. The data is stored in partitions within different topics. A topic is like a database table, and the partitions in a topic can be distributed across the cluster nodes.

Kafka brokers are deployed in a cluster mode, there are two necessary components to manage the nodes: the control plan and the data plane:
1. The control plane manages the metadata of the Kafka cluster. 
2. The data plane handles the data replication.