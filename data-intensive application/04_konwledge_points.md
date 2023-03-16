# Encoding and Evolution
In this chapter we will look at several formats for encoding data, including JSON, XML, Protocol Buffers, Thrift, and Avro. In particular, we will look at how they han‐ dle schema changes and how they support systems where old and new data and code need to coexist. We will then discuss how those formats are used for data storage and for communication: in web services, Representational State Transfer (REST), and remote procedure calls (RPC), as well as message-passing systems such as actors and message queues.

## Formats for Encoding Data
Programs usually work with data in (at least) two different representations:
1. In memory, data is kept in objects, structs, lists, arrays, hash tables, trees, and so on.
2. write data to a file or send it over the network, it is self-contained sequence of bytes.(for example, a JSON document).

The translation from the in-memory representation to a byte sequence is called encoding (also known as serialization or marshalling), and the reverse is called decoding (parsing, deserialization, unmarshalling)

### Thrift(Facebook) ProtocolBuffer(Google) Dubbo(Alibaba)
Q: 为啥有了RPC要用HTTP?<br>
A: RPC在1984年就被人用来做分布式系统的通信,而HTTP协议在1990年才开始作为主流协议出现，而且HTTP发明的场景是用于web架构，而不是分布式系统间通信，这导致了在很长一段时间内，HTTP都是浏览器程序和后端web系统通信用的东西，上面的文档格式都是HTML（非常啰嗦），没有人会把HTTP作为分布式系统通信的协议. 之后AJAX技术和JSON文档在前端界逐渐成为主流，HTTP调用才摆脱HTML，开始使用JSON这一相对简洁的文档格式。<br>
既然有RPC了，为什么还要有HTTP请求？这个问题不难回答，因为现在大部分的系统都是给浏览器使用的，因此HTTP协议必不可少，而这大部分系统中的绝大部分，对于后端系统间调用的性能都是要求不高的，毕竟走的都是内网，它们关心的是前端和后端的性能，因此后端系统间调用如果能够采用和前端一样的技术栈，那无疑是维护成本最低的，而这时HTTP的技术生态也刚好满足这个条件，所以就星星之火可以燎原了。那么对于少数的部分系统，他们需要使用RPC，一可能是老架构，也不敢动这块，二是性能要求可能只有RPC可以满足 （gRPC用的就是HTTP2协议）


gRPC is based on ProtocolBuffer


### Models of Dataflow
1. Dataflow through Database
2. Dataflow through Service: REST vs RPC
3. Message-Passing Dataflow (Message Queue, message is sent to broker)
    * RabbitMQ
    * ActiveMQ
    * Apache Kafka
    * etc

Message brokers are used as follows: one process sends a message to a named queue or topic, and the broker ensures that the message is delivered to one or more consumers of or subscribers to that queue or topic. There can be many producers and many consumers on the same topic.
