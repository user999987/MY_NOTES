### Client-Server Model
Client:\
A machine or process that requests data or service form a server.\
Server:\
A machine or process that provides data or service for a client, usually by listening for ainoming network calls.
```
      getip   returnip
Client---->DNS----->Client----->server
```
Port:\
The TCP protocol provides 16 bits for the port number, so 2power(16)-1 ports.\
Typically, ports 0-1023 are reserved for system ports.\
Also there are some ports are taken:
* 22: secure shell
* 53: DNS lookup
* 80: HTTP
* 443: HTTPS

### Network Protocols
```
 HTTP
  ^
  |
 TCP
  ^
  |
  IP
```
IP Packet:\
Smallest unit used to describe data being sent over IP\
* IP Header: contains source, destination IP address and other info(like size of packet)

TCP handshake: 1.连 2.好 3.连上了\
If you do not send message for a period of time, timeout the disconnect. Or either part can disconnect

### Storage
Disk:\
Application write data to a file
Memory:\
Temporary, like list or dict in the application. Data will be lost when outage happens 

### Latency and Throughput
Latency:\
Time it takes for a certain operation to complete in a system.\
Throughput:\
Number of operations that a system can handle properly per time unit.\
Latency and throughput are not necessarility corelated.

### Availability
High availability solution --  redundancy