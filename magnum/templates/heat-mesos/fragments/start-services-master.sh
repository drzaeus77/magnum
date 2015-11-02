#!/bin/sh

# Start master services
for service in zookeeper mesos-master marathon bird; do
    echo "starting service $service"
    service $service start
    rm -f /etc/init/$service.override
done
