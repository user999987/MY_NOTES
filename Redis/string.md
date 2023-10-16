SDS: simple dynamic strings\
Redis SDS stores sequences of bytes. It operates the data stored in buf array in a binary way, so SDS can store not only text but also binary data like audio, video, and images.



```redis
SET name1 "Alice"
GET name1

SET name2 "Arron"
SET name3 "Alpha"
MGET name1 name2 name3

APPEND name1 "Wong" 

SET myString "This is a long sentence" 
SUBSTR myString 8 10 # retrieve a substring from position 8 to 10

STRLEN STRLEN myString # 23
```