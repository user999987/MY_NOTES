## 弱隔离
读已提交 read committed 最基本的 保证了没有 
* 脏读 row level lock: 只能看到已经提交的数据
* 脏写 旧值保留