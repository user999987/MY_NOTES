When we say Redis is single-threaded, it means that all network IO and read/write operations are handled by a single thread. Other Redis functions, such as persistence and data replication, are handled by other threads. So we can say Redis is single-threaded for critical path operations. 

After Redis 6.0, it uses multi-threading to handle network I/O requests.  However, Redis still uses a single-threaded model for read/write operations on data structures.