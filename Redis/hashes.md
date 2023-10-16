```redis
HSET key field value [field value ...]

HGET key field

HMSET key field value [field value ...]
HMGET key field value [field value ...]

HGETALL key
1) "name"
2) "wocao"
3) "age"
4) "12"

HINCRBY key field increment # Incrementing a field in a hash by a specified value
```