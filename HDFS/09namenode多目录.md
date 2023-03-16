## namenode 的本地目录可以配置多个 且每隔目录存放内容相同 增加了可靠性
datanode 的操作也差不多 区别在于每个目录存储的数据不一样。即：数据不是副本。
1. hdfs-site.xml
    ```xml
    <property>
        <name>dfs.namenode.name.dir<name>
        <value>file:///${hadoop.tmp.dir}/dfs/name1,file:///${hadoop.tmp.dir}/dfs/name2</value>
    </property>
2. stop cluster, delete all data in data and logs
    ```bash
    sbin/stop-dfs.sh
    rm -rf data/ logs/
    ```
3.  格式化集群并启动
    ```bash
    bin/hdfs namenode -format
    sbin/start-dfs.sh
    ```