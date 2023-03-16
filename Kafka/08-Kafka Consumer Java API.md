## High level API
```java
// 创建配置对象
Prpoerties prop = new Properties();
// Kafka 集群
prop.setProperty("bootstrap.server", "ip1:9092");
// K，V 序列化对象
prop.setProperty("key.deserializer","org.apache.kafka.common.serilization.StringDeserilizer");
prop.setProperty("value.deserializer","org.apache.kafka.common.serilization.StringDeserilizer");

// unique string that identifies the consumer group this consumer belongs to. 
// This property is required if the consumer uses either the group management functionality by using  subscribe(topic)  or the Kafka-based offset management strategy
prop.setProperty("group.id","true");
prop.setProperty("enable.auto.commit","true");
prop.setProperty("auto.commit.interval.ms","1000");
// 创建消费者对象
KafkaConsumer<String, String> consumer = new KafkaConsumer<String, String>(prop);

// 订阅主题
consumer.subscribe(Arrays.asList("first"));

while (true){
    // kafka 对 poll loop 行为提供了两个控制参数
    // max.poll.interval.ms 允许 两次调用 poll 方法的最大间隔，即设置每一批任务最大的处理时间。
    // max.poll.records 每一次 poll 最大拉取的消息条数。默认为100
    ConsumerRecords<String, String> records = consumer.poll(timeout: 500);

    for (ConsumerRecord<String, String> record: records){
        System.out.println(record);
    }
}
```

官网还罗列了配置的可选参数 和 重要性



## Low level API
```java
public static void main(String [] args) throws Excception{

    BrokerEndpoint leader = null;

    //创建简单消费者
    String host = "hostname";
    int port = 9092;

    // 获取分区的leader
    SimpleConsumer metaConsumer = new SimpleConsumer(host, port, soTimeout: 500, bufferSize: 10*1024, clientId:"metadata");
    
    //获取元数据
    TopicMetadataRequest request = new TopicMetadataRequest(Arrays.asList("first"));
    TopicMetadataResponse response = metaConsumer.send(request);

    leaderLable:
    for (TopicMetadata topicMetadata: response.topicsMetadata()){
        if ("first".equals(topicMetadata.topic())){
            for (PartitionMetadata partitionMetada: topicMetadata.partitionsMetadata()){
                int partid = partitionMetadata.partitionId();
                if (partid==1){
                    leader = partitionMetadata.leader();
                    break leaderLable;
                }
            }
        }
    }

    if (leader == null){
        System.out.println("分区信息不正确");
        return;
    }

    // host, port 为指定分区 leader 所在地
    SimpleConsumer consumer = new SimpleConsumer(leader.host(), leader.port()), soTimeout: 500, bufferSize: 10*1024, cliendId: "accessLeader");

    // 抓取数据
    FetchRequest req = new FetchRequestBuilder().addFetch(topic:"first", partition:1, offset:5, fetchSize: 10*1024).build();
    FetchResponse resp = consumer.fetch(req);

    ByteBufferMessageSet messageSet = resp.messageSet(topic:"first", partition:1);

    for (MessageAndOffset messageAndOffset: messageSet){
        ByteBuffer buffer = messageAndOffset.message().payload();
        byte[] bs = new byte[buffer.limit()];
        buffer.get(bs)
        String value = new String(bs, s:"UTF-8")
        System.out.println(value);
    }
}