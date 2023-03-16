### Load(负载)
Load can be described with a few numbers which we call load parameters. The best choice of parameters depends on the architecture of your system: it may be requests per second to a web server, the ratio of reads to writes in a database, the number of simultaneously active users in a chat room, the hit rate on a cache, or something else. Perhaps the average case is what matters for you, or perhaps your bottleneck is dominated by a small number of extreme cases.

### Describing the performance
You can look at it in two ways:
* When you increase a load parameter and keep the system resources (CPU, mem‐ ory, network bandwidth, etc.) unchanged, how is the performance of your system affected?
* When you increase a load parameter, how much do you need to increase the resources if you want to keep performance unchanged?

### P50
If you take your list of response times and sort it from fastest to slowest, then the median is the halfway point. For example, if your median response time is 200 ms, that means half your requests return in less than 200 ms, and half your requests take longer than that.  为了弄清异常值有多糟糕，可以看看更高的百分位点，例如第95、99和99.9百分位点（缩写为p95，p99和p999）。它们意味着95％，99％或99.9％的请求响应时间要比该阈值快，例如：如果第95百分位点响应时间是1.5秒，则意味着100个请求中的95个响应时间快于1.5秒，而100个请求中的5个响应时间超过1.5秒。响应时间的高百分位点（也称为尾部延迟（tail latencies））非常重要，因为它们直接影响用户的服务体验。

### Abstraction 
Making a system simpler does not necessarily mean reducing its functionality; it can also mean removing accidental complexity. Moseley and Marks define complex‐ ity as accidental if it is not inherent in the problem that the software solves (as seen by the users) but arises only from the implementation.
One of the best tools we have for removing accidental complexity is abstraction. A good abstraction can hide a great deal of implementation detail behind a clean, simple-to-understand façade. A good abstraction can also be used for a wide range of different applications. Not only is this reuse more efficient than reimplementing a similar thing multiple times, but it also leads to higher-quality software, as quality improvements in the abstracted component benefit all applications that use it.
For example, high-level programming languages are abstractions that hide machine code, CPU registers, and syscalls.

### Declarative vs Imperative
```
function getSharks() { var sharks = [];
for (var i = 0; i < animals.length; i++) { if (animals[i].family === "Sharks") {
sharks.push(animals[i]); }
}
return sharks; }
```
An imperative language tells the computer to perform certain operations in a certain order.<br>
```
SELECT * FROM animals WHERE family = 'Sharks';
```
In a declarative query language, like SQL or relational algebra, you just specify the pattern of the data you want—what conditions the results must meet, and how you want the data to be transformed (e.g., sorted, grouped, and aggregated)—but not how to achieve that goal. It is up to the database system’s query optimizer to decide which indexes and which join methods to use, and in which order to execute various parts of the query.

### Log-Structured Indexes - SSTables and LSM Tree(Log-Structured Merge-Tree)
SSTables = Sorted String Tables
大致意思是 每个segment最先保存在内存中 在写入内存中的时候用平衡树保证有序 segment中的 数据量达到一定程度 压缩 写入硬盘
每个segment有自己的key 并在内存中有一个index保存有segment的key
Merging several SSTable segments, retaining only the most recent value for each key.

Storage engines that are based on this principle of merging and compacting sorted files are often called LSM storage engines.

Lucene, an indexing engine for full-text search used by Elasticsearch and Solr, uses a similar method for storing its term dictionary <br>
term dictionary: list of document id

性能优化-bloom filters 布隆过滤器 <br>
A Bloom filter is a memory-efficient data structure for approximating the contents of a set. It can tell you if a key does not appear in the database, and thus saves many unnecessary disk reads for nonexistent keys

### B-Tree
The log-structured indexes we saw earlier break the database down into variable-size segments, typically several megabytes or more in size, and always write a segment sequentially. By contrast, B-trees break the database down into fixed-size blocks or pages, traditionally 4 KB in size (sometimes bigger), and read or write one page at a time. This design corresponds more closely to the underlying hardware, as disks are also arranged in fixed-size blocks.<br>
The number of references to child pages in one page of the B-tree is called the branching factor
```
| ref | 100 | ref | 200 | ref | 300 | ref | 400 | ref | 500 | ref |
The branching factor is 6
```
In practice, the branching factor depends on the amount of space required to store the page refer‐ ences and the range boundaries, but typically it is several hundred.<br>
If you want to add a new key, you need to find the page whose range encompasses the new key and add it to that page. If there isn’t enough free space in the page to accommodate the new key, it is split into two half-full pages, and the parent page is updated to account for the new subdi‐ vision of key ranges
![b-tree](./pic/b_tree.png)
Most databases can fit into a B-tree that is three or four levels deep, so you don’t need to follow many page references to find the page you are look‐ ing for. (A four-level tree of 4 KB pages with a branching factor of 500 can store up to 256 TB.)

### B-tree optimizations
WAL (write-ahead log) - This is an append-only file to which every B-tree modification must be written before it can be applied to the pages of the tree itself. When the data‐ base comes back up after a crash, this log is used to restore the B-tree back to a con‐ sistent state<br>


latches (lightweight locks) - Protect tree's data structures from concurrent updating on pages

### Write Amplification
one write to the database resulting in multiple writes to the disk over the course of the database’s lifetime—is known as write amplification.<br>
Write amplification (WA) is an undesirable phenomenon associated with flash memory and solid-state drives (SSDs), where the actual amount of information physically-written to the storage media is a multiple of the logical amount intended to be written.

### Other index tech
The key in an index is the thing that queries search for, but the value can be one of two things: it could be the actual row (document, vertex) in question, or it could be a reference to the row stored elsewhere. In the latter case, the place where rows are stored is known as a heap file.<br>
When updating a value without changing the key, the heap file approach can be quite efficient<br>
In some situations, the extra hop from the index to the heap file is too much of a per‐ formance penalty for reads, so it can be desirable to store the indexed row directly within an index. This is known as a clustered index<br>
A compromise between a clustered index (storing all row data within the index) and a nonclustered index (storing only references to the data within the index) is known as a covering index or index with included columns, which stores some of a table’s col‐ umns within the index <br>

http://www.mathcs.emory.edu/~cheung/Courses/554/Syllabus/3-index/R-tree.html
R-tree


https://tech.meituan.com/2014/06/30/mysql-index.html
mysql 文章 就结论简单来说最左匹配 遇到 "<" or ">"就不使用索引了


### OLTP & OLAP
online transaction processing<br>
online analytic processing<br>
![olap_oltp](./pic/olap_oltp.png)
At first, the same databases were used for both transaction processing and analytic queries. SQL turned out to be quite flexible in this regard: it works well for OLTP- type queries as well as OLAP-type queries. Nevertheless, in the late 1980s and early 1990s, there was a trend for companies to stop using their OLTP systems for analytics purposes, and to run the analytics on a separate database instead. This separate data‐ base was called a data warehouse.

### Data Warehouse
A data warehouse, by contrast, is a separate database that analysts can query to their hearts’ content, without affecting OLTP operations. The data warehouse con‐ tains a read-only copy of the data in all the various OLTP systems in the company. Data is extracted from OLTP databases (using either a periodic data dump or a con‐ tinuous stream of updates), transformed into an analysis-friendly schema, cleaned up, and then loaded into the data warehouse. This process of getting data into the warehouse is known as Extract–Transform–Load (ETL).

### Schema Analytics
At the center of the schema is a so-called fact table (in this example, it is called fact_sales). Each row of the fact table represents an event that occurred at a particular time (here, each row represents a customer’s purchase of a product). If we were analyzing website traffic rather than retail sales, each row might represent a page view or a click by a user.
![fact_table](./pic/fact_table.png)
Some of the columns in the fact table are attributes, such as the price at which the product was sold and the cost of buying it from the supplier (allowing the profit mar‐ gin to be calculated). Other columns in the fact table are foreign key references to other tables, called dimension tables. As each row in the fact table represents an event, the dimensions represent the who, what, where, when, how, and why of the event.


The name “star schema” comes from the fact that when the table relationships are visualized, the fact table is in the middle, surrounded by its dimension tables; the connections to these tables are like the rays of a star.

A variation of this template is known as the snowflake schema, where dimensions are further broken down into subdimensions. For example, there could be separate tables for brands and product categories, and each row in the dim_product table could ref‐ erence the brand and category as foreign keys, rather than storing them as strings in the dim_product table. Snowflake schemas are more normalized than star schemas, but star schemas are often preferred because they are simpler for analysts to work with

## Column Storage

### Column storage enginee
The idea behind column-oriented storage is simple: don’t store all the values from one row together, but store all the values from each column together instead. If each col‐ umn is stored in a separate file, a query only needs to read and parse those columns that are used in that query, which can save a lot of work.

The column-oriented storage layout relies on each column file containing the rows in the same order. Thus, if you need to reassemble an entire row, you can take the 23rd entry from each of the individual column files and put them together to form the 23rd row of the table.

### Column Compression
Often, the number of distinct values in a column is small compared to the number of rows (for example, a retailer may have billions of sales transactions, but only 100,000 distinct products). We can now take a column with n distinct values and turn it into n separate bitmaps: one bitmap for each distinct value, with one bit for each row. The bit is 1 if the row has that value, and 0 if not.


```
Example of bitmap but it is different from the description above
[0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
这是24位, 这个时候假如我们要存放2 4 6 8 9 10 17 19 21这些数字到我们的BitMap里，我们只需把对应的位设置为1就可以了
[0 0 0 1 0 1 0 1 0 0 0 0 0 0 1 1 1 0 1 0 1 0 1 0]
```

### Sort Order in Column Storage
列 order sort 一般是排列一个列中的属性根据排列好的 order 在进行下一个属性的sort<br>
如果每列各自排各自的那row就乱掉了<br>


Having multiple sort orders in a column-oriented store is a bit similar to having mul‐ tiple secondary indexes in a row-oriented store. But the big difference is that the row- oriented store keeps every row in one place (in the heap file or a clustered index), and secondary indexes just contain pointers to the matching rows. In a column store, there normally aren’t any pointers to data elsewhere, only columns containing values.



### Writing to Column-Oriented Storage
An update-in-place approach, like B-trees use, is not possible with compressed columns. If you wanted to insert a row in the middle of a sorted table, you would most likely have to rewrite all the column files. As rows are identified by their position within a column, the insertion has to update all columns consistently.<br>
Fortunately, we have already seen a good solution earlier in this chapter: LSM-trees.All writes first go to an in-memory store, where they are added to a sorted structure and prepared for writing to disk.


### Aggregation: Data Cubes and Materialized Views
Another aspect of data warehouses that is worth mentioning briefly is materialized aggregates. As discussed earlier, data warehouse queries often involve an aggregate function, such as COUNT, SUM, AVG, MIN, or MAX in SQL. If the same aggregates are used by many different queries, it can be wasteful to crunch through the raw data every time. We can cache the result.

One way of creating such a cache is a materialized view. In a relational data model, it is often defined like a standard (virtual) view: a table-like object whose contents are the results of some query. The difference is that a materialized view is an actual copy of the query results, written to disk, whereas a virtual view is just a shortcut for writ‐ ing queries. When you read from a virtual view, the SQL engine expands it into the view’s underlying query on the fly and then processes the expanded query.

When the underlying data changes, a materialized view needs to be updated, because it is a denormalized copy of the data. The database can do that automatically, but such updates make writes more expensive, which is why materialized views are not often used in OLTP databases. In read-heavy data warehouses they can make more sense (whether or not they actually improve read performance depends on the indi‐ vidual case).

A common special case of a materialized view is known as a data cube or OLAP cube. 
```
For example, there are five dimensions: date, product, store, prmotion and customer in fact table. each cell contains the sales for a particular date-product-store-promotion- customer combination.
```

The advantage of a materialized data cube is that certain queries become very fast because they have effectively been precomputed. 

The disadvantage is that a data cube doesn’t have the same flexibility as querying the raw data. 

Most data warehouses try to keep as much raw data as possible, and use aggregates such as data cubes only as a performance boost for certain queries.
