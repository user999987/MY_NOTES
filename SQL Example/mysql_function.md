```
DELIMITER $$
drop function if exists generate_customer_number;
create function generate_customer_number(customer_name varchar(45))
returns varchar(10)
begin
	declare total int;
    # extract first 3 letters from customer_name 
	DECLARE cn_three_letters varchar(3);
    set cn_three_letters = left(customer_name,3);
    
    SELECT count(*) FROM xiaoming.customers where left(customer_number,3) like cn_three_letters into total;
    return CONCAT(cn_three_letters,'-', total+1);
END $$
 
DELIMITER ;
```
select generate_customer_number('woca')