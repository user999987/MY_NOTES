```redis
SADD myset m1 m2 m3
SREM myset m2 # Set Remove

SCARD myset # Set Cardinality
SISMEMBER myset m1 # checks if member exists in a set

SINTER set1 set2 set3 ... # Set Intersection returns intersections of given sets
SUNION set1 set2 set3 ...

SMEMBERS myset # read  all elements in set
```