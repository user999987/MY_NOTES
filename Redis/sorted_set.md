```redis
Sorted sets in Redis are an ordered collection of elements, where each element is associated with a score (a double-precision floating-point number)


ZADD sset score member [score member ...]

ZRANGE sset 0 -1 # ascending order
ZREVRANGE sset 0 -1 # descending order

ZRANGEBYSCORE key min max
ZREMRANGEBYSCORE key min max

ZRANK sset field # return the rank of field (0-based index)
```