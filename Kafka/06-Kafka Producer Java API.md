```java
// 创建配置对象
Prpoerties prop = new Properties();
// Kafka 集群
prop.setProperty("bootstrap.server", "ip1:9092");
// K，V 序列化对象
prop.setProperty("key.serializer","org.apache.kafka.common.serilization.StringSerilizer");
prop.setProperty("value.serializer","org.apache.kafka.common.serilization.StringSerilizer");
// 应答机制
prop.setProperty("acks","1");

// 自定义分区 具体实现可以用 hashcode 然后 异或 取模
// prop.setProperty("partitioner.class","project.path.MyCustomePartitioner");


// 创建生产者
Producer<String, String> producer = new KafkaProducer<String, String>(prop);

// 准备数据
String topic = "first";
String value = "Hello Kafka";

for (int i=0; i < 50; i++){
    // 发送默认为异步 可以加回调方法 如果想同步 可以在最后加 .get() 会等应答机制的回复
    producer.send(new ProducerRecord<String, String>(topic, value+i));
}

// callback 的写法
// producer.send(record, new Callback(){
//     public void onCompletion(RecordMetadata recordMetadata, Exception e){
//         System.out.println(recordMetadata.topic());
//         etc
//     }
// });

// 也可以指定分区
// ProducerRecord record = new ProducerRecord(topic, partition:1, key:null, value);


// 关闭生产者
producer.close();
```

官网还罗列了配置的可选参数 和 重要性