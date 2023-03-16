With a clustered index the rows are stored physically on the disk in the same order as the index. Therefore, there can be only one clustered index.(leaf node of B+ tree stores real data)\
With a non clustered index there is a second list that has pointers to the physical rows. You can have many non clusterted indices, although each new index will the time it takes to write new records. (leaf node of B+ tree store ref to primary key)\
Innodb uses clustered index for primay key, secondary key uses non-clustered index.\
It is generally faster to read from a clusterd index if you want to get back all the columns. You do not have to go first to the index and then to the table.\
Writting to a table with a clusterted index can be slower, if there is a need to rearrange the data.
