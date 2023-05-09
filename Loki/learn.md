# Distributor
The distributor service is responsible for handling incoming streams by clients. It’s the first stop in the write path for log data. Once the distributor receives a set of streams, each stream is validated for correctness and to ensure that it is within the configured tenant (or global) limits. Valid chunks are then split into batches and sent to multiple ingesters in parallel.

They act like the bouncer at the front door, ensuring everyone is appropriately dressed and has an invitation. It also allows us to fan-out writes according to our replication factor.
## Validation 
ensure that all incoming data is according to specification
## Preprocessing
sorting the labels. This allows Loki to cache and hash them deterministically
## Rate limiting
allows the rate limit to be specified per tenant at the cluster level and enables us to scale the distributors up or down and have the per-distributor limit adjust accordingly. For instance, say we have 10 distributors and tenant A has a 10MB rate limit. Each distributor will allow up to 1MB/second before limiting. Now, say another large tenant joins the cluster and we need to spin up 10 more distributors. The now 20 distributors will adjust their rate limits for tenant A to (10MB / 20 distributors) = 500KB/s \
<b>Note: The distributor uses the ring component under the hood to register itself amongst it’s peers and get the total number of active distributors. This is a different “key” than the ingesters use in the ring and comes from the distributor’s own ring configuration.
</b>

## Forwarding
Once the distributor has performed all of it’s validation duties, it forwards data to the ingester component which is ultimately responsible for acknowledging the write.
### Replication Factor
In order to mitigate the chance of losing data on any single ingester, the distributor will forward writes to a replication_factor of them
### Hashing
Distributors use consistent hashing in conjunction with a configurable replication factor to determine which instances of the ingester service should receive a given stream.
### Quorum consistency
Since all distributors share access to the same hash ring, write requests can be sent to any distributor.
To ensure consistent query results, Loki uses Dynamo-style quorum consistency on reads and writes

# Ingester
The ingester service is responsible for writing log data to long-term storage backends (DynamoDB, S3, Cassandra, etc.) on the write path and returning log data for in-memory queries on the read path.

Ingesters contain a lifecycler which manages the lifecycle of an ingester in the hash ring. Each ingester has a state of either PENDING, JOINING, ACTIVE, LEAVING, or UNHEALTHY