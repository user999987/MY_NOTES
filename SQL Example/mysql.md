## execution order
```
(8) SELECT (9)DISTINCT<Select_list>
(1) FROM <left_table> (3) <join_type>JOIN<right_table>
(2) ON<join_condition>
(4) WHERE<where_condition>
(5) GROUP BY<group_by_list>
(6) WITH {CUBE|ROLLUP}
(7) HAVING<having_condtion>
(10) ORDER BY<order_by_list>
(11) LIMIT<limit_number>
```

## inner join or join
![alt text](pic/join.png)
## left join
![alt text](pic/left_join.png)
## right join
![alt text](pic/right_join.png)
## full join
![alt text](pic/full_join.png)
## cross join
![alt text](pic/cross_join.png)