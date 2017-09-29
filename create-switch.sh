#!/bin/bash

. $(dirname ${BASH_SOURCE})/shell/util.sh

NETWORK="ato"
CLIENT_LABEL="client"
SUBNET="172.19.0.0/16"

function cleanup {
	docker network rm $NETWORK 2> /dev/null || true
}

trap cleanup EXIT

desc "CREATE A MOCK SWITCH USING MININET"
desc ""
desc "Create network \"$NETWORK\""
run "docker network create --subnet $SUBNET $NETWORK"

desc "Start the container"
run "docker run -itd --name=ato-switch --privileged -v /lib/modules:/lib/modules mininet:latest"

desc "Connect the network"
run "docker network connect ato ato-switch"

desc "Remove the other network"
run "docker exec ato-switch python switch.py --subnet 172.19.0.0/16 --interface eth1 --ip 172.19.0.2"

desc "Clean up"
run "docker rm -f ato-switch"
run "docker network rm $NETWORK"