eth- a physical interface representing Ethernet network card. It’s used for communication with other computers on the network and on the Internet\
lo- a special virtual network interface called loopback device. Loopback is used mainly for diagnostics and troubleshooting, and to connect to services running on local host.
```bash
lo0: flags=8049<UP,LOOPBACK,RUNNING,MULTICAST> mtu 16384 # UP表示开启 LOOPBACK 回环地址 RUNNING网卡的网线被接上 MULTICAST支持组播 MTU最大传输单元
	options=1203<RXCSUM,TXCSUM,TXSTATUS,SW_TIMESTAMP>
	inet 127.0.0.1 netmask 0xff000000 
	inet6 ::1 prefixlen 128 
	inet6 fe80::1%lo0 prefixlen 64 scopeid 0x1 
	inet 127.94.0.2 netmask 0xff000000 
	inet 127.94.0.1 netmask 0xff000000 
	nd6 options=201<PERFORMNUD,DAD>
```
docker0- a virtual bridge interface created by Docker. This bridge creates a separate network for docker containers and allows them to communicate with each other



In arbitrary order of my familarity / widespread relevance:

lo0 is loopback.

en0 at one point "ethernet", now is WiFi (and I have no idea what extra en1 or en2 are used for).

fw0 is the FireWire network interface.

stf0 is an IPv6 to IPv4 tunnel interface to support the transition from IPv4 to the IPv6 standard.

gif0 is a more generic tunneling interface [46]-to-[46].

awdl0 is Apple Wireless Direct Link

p2p0 is related to AWDL features. Either as an old version, or virtual interface with different semantics than awdl.