user_name = "xiaoming liuliu"
insert_query="insert into customers (customer_name) values ({user_name})".format(user_name=user_name)
retrieve_cn = "select * from customers where customer_name like \"%{customer_number}%\" ".format(customer_number=user_name[:3])
user_number = ""
for row in retrieve_cn:
    if user_name == row['customer_name']:
        user_number =  row['customer_number']
        break
inser_contact = "insert into customer_contact (last_name, first_name, email, customer_number) values ({}, {}, {}, {})".format(
    last_name, first_name, email, user_number
)