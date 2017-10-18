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

echo "=== INSTALLED CONSUL & DOCKER! ==="
exit 0
