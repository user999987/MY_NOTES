1. create vpc
resources to create: vpc only(实验给的)\
tag - optional\ 
IPv4 CIDR: 10.0.0.0/16\
Actions->Edit VPC settings->DNS settings->Enable DNS hostname\

2. create public subnet
AZ: choose one\
IPv4 CIDR block: 10.0.0.0/24\
Create\
Edit subnet settings-> Enable auto-assign public IPv4 address\

3. create private subnet
AZ: choose one\
IPv4 CIDR block: 10.0.2.0/23\

4. IGW
provide a name and create\
actions->attach to vpc\

5. transfer public subnet data to IGW/create route table
create\
edit routes->add route->destination(0.0.0.0/0)/target(IGW)\
subnet association\

6. SG
SG name\
Description\
VPC\
Inbound rules->type(http)/source(anywhere-ipv4)\
tag - optional

7. Launch Ec2
ec2->dashboard\
Launch instance\
name/AMI/instance type/key pair\
network settings->edit->vpc/subnet/enable auto-assign public/SG(select existing SG)\
configure storage can add EBS\
Advanced details->IAM instance profile(EC2InstProfile)/User data(开机启动脚本)\
Instance->specific instance->networking -> Public DNS(公网访问)\

8. session manager
Instance->connect->session manager(连接ec2)\

9. NAT网关并在私有子网中配置路由(允许private subnet连接到互联网)
VPC->NAT gateways-> create(name/subnet-public/allocate elastic ip)-> Create\
create route table(name/VPC)\
select most recently created route->edit routes->add route(destination:0.0.0./0 / target: NAT GW)\
subnet association\

10. private subnet SG
create sg(name/description/vpc)\
inbound rules(type:https/source: under custom,search sg choose public SG)\
tag(key:Name/value:Private SG)

11. launch an ec2 in private subnet
same as launch an ec2 in public subnet