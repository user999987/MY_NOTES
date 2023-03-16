# Faults and Partial Failures
In distributed systems, suspicion, pessimism, and paranoia pay off.

## Cloud Computing and Supercomputing
There is a spectrum of philosophies on how to build large-scale computing systems:
* high-performance computing (HPC)
* cloud computing
* Traditional enterprise datacenters lie somewhere between above two

Variable delays in networks are not a law of nature, but simply the result of a cost/ benefit trade-off.

# Unreliable Clocks
## Monotonic Versus Time-of-Day Clocks
### Time-of-Day Clocks
Time-of-day clocks are usually synchronized with NTP, which means that a timestamp from one machine (ideally) means the same as a timestamp on another machine. n particular, if the local clock is too far ahead of the NTP server, it may be forcibly reset and appear to jump back to a previous point in time. These jumps, as well as the fact that they often ignore leap seconds (Leap seconds result in a minute that is 59 seconds or 61 seconds long), make time-of-day clocks unsuitable for measuring elapsed time

### Monotonic clocks
A monotonic clock is suitable for measuring a duration (time interval), such as a timeout or a service’s response time. The name comes from the fact that they are guaranteed to always move forward.

## Clock Synchronization and Accuracy
Hardware clocks and NTP can be fickle beasts.
* The quartz clock in a computer is not very accurate: it drifts (runs faster or slower than it should). Clock drift varies depending on the temperature of the machine
* If a computer’s clock differs too much from an NTP server, it may refuse to syn‐ chronize, or the local clock will be forcibly reset
* The best way of handling leap seconds may be to make NTP servers “lie,” by performing the leap second adjustment gradually over the course of a day (this is known as smearing). Although actual NTP server behavior varies in practice

It is possible to achieve very good clock accuracy by using GPS receivers, the Precision Time Protocol (PTP), and careful deployment and monitoring

## Relying on Synchronized Clocks
### Timestamps for ordering events
Logical clocks do not measure the time of day or the number of seconds elapsed, only the relative ordering of events (whether one event happened before or after another), is a safer alternative for ordering event

### Clock readings have a confidence interval
With an NTP server on the public internet, the best pos‐ sible accuracy is probably to the tens of milliseconds, and the error may easily spike to over 100 ms when there is network congestion

Thus, it doesn’t make sense to think of a clock reading as a point in time—it is more like a range of times, within a confidence interval: for example, a system may be 95% confident that the time now is between 10.3 and 10.5 seconds past the minute
# Knowledge, Truth and Lies
## The Truth Is Defined by the Majority
Many distributed algorithms rely on a quorum, that is, voting among the nodes: decisions require some minimum number of votes from several nodes in order to reduce the dependence on any one particular node.
### Fencing tokens
客户端1以33的令牌获得租约，但随后进入一个长时间的停顿并且租约到期。客户端2以34的令牌（该数字总是增加）获取租约，然后将其写入请求发送到存储服务，包括34的令牌。稍后，客户端1恢复生机并将其写入存储服务，包括其令牌值33.但是，存储服务器会记住它已经处理了一个具有更高令牌编号（34）的写入，因此它会拒绝带有令牌33的请求。

## Byzantine Faults
Fencing tokens can detect and block a node that is inadvertently acting in error (e.g., because it hasn’t yet found out that its lease has expired). However, if the node deliberately wanted to subvert the system’s guarantees, it could easily do so by sending messages with a fake fencing token.

If there is a risk that nodes may “lie”, such behavior is known as a Byzantine fault, and the problem of reaching consensus in this untrusting environment is known as the Byzantine Generals Problem.

A system is Byzantine fault-tolerant if it continues to operate correctly even if some of the nodes are malfunctioning and not obeying the protocol, or if malicious attack‐ ers are interfering with the network. 