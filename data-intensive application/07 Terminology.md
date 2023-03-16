Dirty reads<br>
One client reads another client’s writes before they have been committed. The read committed isolation level and stronger levels prevent dirty reads.

Dirty writes<br>
One client overwrites data that another client has written but not yet committed. Almost all transaction implementations prevent dirty writes.

Read skew (nonrepeatable reads)<br>
A client sees different parts of the database at different points in time. This issue is most commonly prevented with snapshot isolation, which allows a transaction to read from a consistent snapshot at one point in time. It is usually implemented with multi-version concurrency control (MVCC).

Write skew<br>
A transaction reads something, makes a decision based on the value it saw, writes the decision to the database. However, by the time the write is made, the premise of the decision is no longer true. Only serializable isolation prevents this anomaly.

Lost updates<br>
Two clients concurrently perform a read-modify-write cycle. One overwrites the other’s write without incorporating its changes, so data is lost. Some implemen‐ tations of snapshot isolation prevent this anomaly automatically, while others require a manual lock (SELECT FOR UPDATE).

Phantom reads<br>
A transaction reads objects that match some search condition. Another client makes a write that affects the results of that search. Snapshot isolation prevents straightforward phantom reads, but phantoms in the context of write skew require special treatment, such as index-range locks.