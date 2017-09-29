# Automating Connectivity

This creates two hosts with Open vSwitch installed to demonstrate
the general principles of automating switches and evaluating
that they are able to connect to each other when a container
network is created.

The code serves as an example for those who want to automate
actions in their network. It is not required.



## References
* [Multi-Host Networking](http://docker-k8s-lab.readthedocs.io/en/latest/docker/docker-ovs.html)



## Pre-Requisites
1. Mininet Docker image
1. Run the mininet docker image.
```
docker run -it --rm --privileged -v ~/personal/2017-demo-ato/mininet:/scripts -v /lib/modules:/lib/modules mininet:latest
```

mn --custom switch.py --topo mytopo


mn --topo linear,1 --mac --switch ovsk --controller remote

mininet> s1 ip addr add 172.16.20.10/24 dev s1-eth1
mininet> s1 ip route add default via 172.16.20.1
RTNETLINK answers: File exists
mininet> s1 ip route
default via 172.17.0.1 dev eth0
172.19.0.0/16 dev s1-eth1  proto kernel  scope link  src 172.19.0.0
172.17.0.0/16 dev eth0  proto kernel  scope link  src 172.17.0.2



s1 ip route del 172.19.0.0/16 dev eth1  proto kernel  scope link  src 172.19.0.2

```
root@c21d883bc552:/scripts# python switch.py -h
usage: switch.py [-h] [--subnet SUBNET] [--interface INTERFACE] [--ip IP]

Topology that removes default route to Docker network

optional arguments:
  -h, --help            show this help message and exit
  --subnet SUBNET       subnet & mask (e.g., 172.17.0.0/16)
  --interface INTERFACE
                        interface (e.g., eth0)
  --ip IP               ip address (e.g., 172.17.0.3)
root@c21d883bc552:/scripts# python switch.py --subnet 172.19.0.0/16 --interface eth1 --ip 172.19.0.2
*** Error setting resource limits. Mininet's performance may be affected.
*** Creating network
*** Adding controller
*** Adding hosts:

*** Adding switches:
s1
*** Adding links:

*** Configuring hosts

*** Starting controller
c0
*** Starting 1 switches
s1 ...
*** Starting CLI:
mininet> s1 ip route show
default via 172.17.0.1 dev eth0
172.17.0.0/16 dev eth0  proto kernel  scope link  src 172.17.0.2
mininet>
```


```
host1$ docker run -d --name container1 --ip 172.17.0.3 centos:7 /bin/bash -c "while true; do sleep 3600; done"
host2$ docker run -d --name container1 --ip 172.17.0.4 centos:7 /bin/bash -c "while true; do sleep 3600; done"
```
