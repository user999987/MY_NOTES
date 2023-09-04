docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres
same as mysql, but you can ignore password. When password is ignored, psql -U username will connect to the postgres inside container.
\dt will show all tables
\q will exit the psql

ref :https://hub.docker.com/_/postgres

docker run --name some-mysql -e MYSQL_ROOT_PASSWORD=1234 -d mysql
--name is the container name
-e is the password you assign to the mysql running inside the container 
-d is the image

ref: https://hub.docker.com/_/mysql

SHOW DATABASES;
CREATE DATABASE mine;
USE mine;
SHOW TABLES;