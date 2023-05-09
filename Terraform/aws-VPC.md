https://docs.aws.amazon.com/vpc/latest/userguide/vpc-ip-addressing.html

VPC->subnet(resources are inside subnet, usually they have private ip address, for public ip address, one way is NAT:network address translation)

IPv4 Up to 5 CIDRs from /16 to /28 \
Subnet Size from /16 to /28
205.123.196.183/25 First 25 digits are network address, the rest are machine address.

Subnet CIDR: 10.0.0.0/24, it supports 256 IP address. 10.0.0.0/25 (10.0.0.0 - 10.0.0.127). The other block is 10.0.0.128/25 (10.0.0.128-10.0.0.255)

A default VPC comes with a public subnet in each Availability Zone, an internet gateway, and settings to enable DNS resolution

 A VPC must have additional resources, such as subnets, route tables, and gateways, before you can create AWS resources in the VPC.