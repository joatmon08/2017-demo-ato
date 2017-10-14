#!/bin/bash

function isinstalled {
  if yum list installed "$@" >/dev/null 2>&1; then
    return 0
  else
    return 1
  fi
}

function isactive {
  if systemctl is-active "$@" >/dev/null 2>&1; then
    echo "$@ IS ON"
  else
    systemctl start "$@"
  fi
}
yum -y update && yum -y upgrade

echo "=== INSTALLING OVS DEPENDENCIES ==="
yum -y install make gcc openssl-devel autoconf automake \
rpm-build redhat-rpm-config python-devel python-six \
openssl-devel kernel-devel kernel-debug-devel libtool wget \
net-tools bridge-utils
if [ $? -ne 0 ]; then
    echo "FAILED TO DOWNLOAD OVS DEPENDENCIES"
    exit 1
fi

echo $'[cloud7]
name=CentOS Cloud7 Openstack
baseurl=http://cbs.centos.org/repos/cloud7-openstack-common-release/x86_64/os/
enabled=1
gpgcheck=0'  > /etc/yum.repos.d/cloud7.repo

if isinstalled "openvswitch"; then
    echo "=== OVS IS ALREADY INSTALLED"
else
    echo "=== INSTALLING OVS ==="
    output=`yum -y install openvswitch`
    if [ $? -ne 0 ]; then
        echo "FAILED TO INSTALL OVS : ${output}"
        exit 1
    fi
fi

echo "=== CHECKING OVS VERSION ==="
output=`ovs-vsctl --version`
if [ $? -ne 0 ]; then
    echo "NEED TO CHANGE PATH FOR OVS : ${output}"
    exit 1
fi

echo "=== TURNING ON OVS ==="
isactive "openvswitch"

systemctl enable openvswitch

echo "=== INSTALLING CONSUL ==="
wget https://releases.hashicorp.com/consul/0.9.3/consul_0.9.3_linux_amd64.zip
unzip consul_0.9.3_linux_amd64.zip
mv consul /usr/bin/
echo "" > /tmp/consul_watch.log

echo $'[Unit]
Description=consul

[Service]
ExecStart=/usr/bin/consul agent -config-file /opt/consul/config/config.json -server -dev -ui -client 0.0.0.0

[Install]
WantedBy=multi-user.target' > /etc/systemd/system/consul.service

echo "=== CONFIGURE CONSUL ==="
yum -y install git
mkdir -p /opt/consul/config && chmod 777 /opt/consul/config
git clone -b artifacts https://github.com/joatmon08/docker-consul-handler.git /opt/consul/config
chmod +x /opt/consul/config/handler

echo $'[dockerrepo]
name=Docker Repository
baseurl=https://yum.dockerproject.org/repo/main/centos/7/
enabled=1
gpgcheck=1
gpgkey=https://yum.dockerproject.org/gpg' > /etc/yum.repos.d/docker.repo

if isinstalled "docker"; then
    echo "=== DOCKER IS ALREADY INSTALLED"
else
    echo "=== INSTALLING DOCKER ==="
    output=`yum -y install docker-engine`
    if [ $? -ne 0 ]; then
        echo "FAILED TO INSTALL DOCKER : ${output}"
        exit 1
    fi
fi

echo "=== CONFIGURE DOCKER ==="
mkdir -p /etc/systemd/system/docker.service.d
echo $'[Service]
ExecStart=
ExecStart=/usr/bin/dockerd -H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock --cluster-store=consul://127.0.0.1:8500 --cluster-advertise=eth1:2375' > /etc/systemd/system/docker.service.d/override.conf

echo "=== TURNING ON DOCKER ==="
isactive "docker"

echo "=== CHECKING DOCKER DAEMON ==="
output=`docker ps`
if [ $? -ne 0 ]; then
    echo "FAILED TO SHOW DOCKER INFORMATION : ${output}"
    exit 1
fi

systemctl enable docker

echo "=== BOOTSTRAP COMPLETED SUCCESSFULLY! ==="
exit 0
