```
DELIMITER $$
DROP TRIGGER IF EXISTS customer_number_trigger ;
CREATE TRIGGER customer_number_trigger before INSERT ON customers FOR EACH ROW
BEGIN
	declare cn_number varchar(10);
    select generate_customer_number(new.customer_name) into cn_number;
	set new.customer_name = new.customer_name;
    set new.customer_number = cn_number;
END $$
DELIMITER ;
```
-- select generate_customer_number('woca')

Within the trigger body, the OLD and NEW keywords enable you to access columns in the rows affected by a trigger. OLD and NEW are MySQL extensions to triggers; they are not case-sensitive.

In an INSERT trigger, only NEW.col_name can be used; there is no old row. In a DELETE trigger, only OLD.col_name can be used; there is no new row. In an UPDATE trigger, you can use OLD.col_name to refer to the columns of a row before it is updated and NEW.col_name to refer to the columns of the row after it is updated.