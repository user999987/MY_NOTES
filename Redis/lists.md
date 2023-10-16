```redis
LPUSH mylist alice
LPUSH mylist bob arron # mylist:["arron","bob","alice"] redis list用的linked list 放头部, there is RPUSH

LLEN mylist # 3

LPOP mylist 

LRANGE mylist 0 -1 # LRANGE key start stop
LINDEX mylist 0 # LINDEX key index

DEL mylist
```