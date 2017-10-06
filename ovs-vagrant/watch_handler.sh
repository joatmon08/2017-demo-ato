#!/usr/bin/env sh
exec >> /tmp/consul_watch.log
IFS=" "
while read a
do
    echo $a
done
