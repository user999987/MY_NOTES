0.10 版本引入 使得用户在消息发送前 以及 回调逻辑前有机会对消息做一些 customize。 可指定多个 interceptor 按序作用于同一条消息 形成一个 interceptor chain
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
```
<span style="color:red">
//拦截器 拦截器 拦截器 拦截器 拦截器

List<String> interceptors = new ArrayList<String>();
interceptors.add("project.path.Cutomized.MyInterceptorClass1");
interceptors.add("project.path.Cutomized.MyInterceptorClass2");
prop.put(ProducerConfig.INTERCEPTOR_CLASSES_CONFIG, interceptors)
</span>

```java
// 创建生产者
Producer<String, String> producer = new KafkaProducer<String, String>(prop);

// 准备数据
String topic = "first";
String value = "Hello Kafka";

for (int i=0; i < 50; i++){
    // 发送默认为异步 可以加回调方法 如果想同步 可以在最后加 .get() 会等应答机制的回复
    producer.send(new ProducerRecord<String, String>(topic, value+i));
}


// 也可以指定分区
// ProducerRecord record = new ProducerRecord(topic, partition:1, key:null, value);


// 关闭生产者
producer.close();
```



## interceptor 主要 4 个方法
```java
public class TimeInterceptor implements ProducerInterceptor<String, String>{
    public ProducerRecord<String, String> onSend(ProducerRecord<String, String> record){
        String oldValue = record.value();
        String newValue = System.currentTimeMillis()+"_"+oldValue;

        return new ProducerRecord<String, String>(record.topic(), newValue);
    }

    public void onAcknowledgement(RecordMetadata metadata, Exception exception){

    }

    public void close(){
        
    }

    public void configure(Map<String, ?> configs){

    }
}
```




```java
public class CounterInterceptor implements ProducerInterceptor<String, String>{

    private int errorCounter = 0;
    private int successCounter = 0;

    public ProducerRecord<String, String> onSend(ProducerRecord<String, String> record){
        return record;
    }

    public void onAcknowledgement(RecordMetadata metadata, Exception exception){
        if (exception == null){
            successCounter++;
        }else{
            errorCounter++;
        }
    }

    public void close(){
        System.out.println("成功的数量"+successCounter);
        System.out.println("失败的数量"+errorCounter);
    }

    public void configure(Map<String, ?> configs){

    }
}
```