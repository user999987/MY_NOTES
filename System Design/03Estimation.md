## 壹 Power of Two
10 1 Thousand 1 KB
20 1 Million 1 MB
30 1 Billion 1 GB
40 1 Trillion 1 TB
50 1 Quadrillion 1 PB

## 贰 Latency
L1 0.5ns
L2 7ns
Mutex lock/unlock 100ns
Main memory 100ns
Compress 1KB with Zippy 10µs
Send 2KB over 1 Gbps network 20µs
Read 1MB sequentially from memory 250µs
Round trip within the data center 500µs
Disk seek 10ms
Read 1MB sequentially from disk 30ms
Send a packet CA->Netherlands->CA 150ms

## 叁 Service Level agreement SLA
4 nines 99.99% downtime 

## 肆
Assumptions:
- 300 million monthly active users.
- 50% of users use Twitter daily.
- Users post 2 tweets per day on average.
- 10% of tweets contain media.
- Data is stored for 5 years. 
Estimations:
- QPS:
    - DAU = 300m * 50% = 150m
    - Tweets query per second = 150m * 2 tweets / 24 hour / 3600 seconds = ~3.5k
    - Peek QPS = 2 * QPS = ~7k
- Storage:
    - tweet_id 64B
    - text 140B
    - media 1MB
    - Media total: 150m * 2 * 10% * 1MB = 30TB per day
    - 5 year storage: 30TB * 365 * 5 = ~55PB
