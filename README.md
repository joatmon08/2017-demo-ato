# Automating Connectivity

This creates two hosts with Open vSwitch installed to demonstrate
the general principles of automating switches and evaluating
that they are able to connect to each other when a container
network is created.

The code serves as an example for those who want to automate
actions in their network. It is not required.

## References
* [Multi-Host Networking](http://docker-k8s-lab.readthedocs.io/en/latest/docker/docker-ovs.html)

## Vagrant Up
Add output of `vagrant ssh-config` to ~/.ssh/config.

## To Test
### host1
```
docker run -d --name container1 centos:7 /bin/bash -c "while true; do sleep 3600; done"
docker exec -it container1 ping -c 3 172.17.0.3
```

### host2
```
docker run -d --name container1 centos:7 /bin/bash -c "while true; do sleep 3600; done"
docker run -d --name container2 centos:7 /bin/bash -c "while true; do sleep 3600; done"
docker rm -f container1
docker exec -it container2 ping -c 3 172.17.0.2
```


## Ansible Playbook
```
ansible-playbook site.yml -b -i hosts --extra-vars "container_network=test"
```

## Docker network creation
Create Docker network with custom bridge name!
```
docker network create -o "com.docker.network.bridge.name"="rlw" hi
```


```
[Service]
ExecStart=
ExecStart=/usr/bin/dockerd -H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock --cluster-store=consul://127.0.0.1:8500 --cluster-advertise=eth1:2375
```