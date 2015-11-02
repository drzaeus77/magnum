#!/bin/sh

# Start slave services
for service in docker mesos-slave bird; do
    echo "starting service $service"
    service $service start
    rm -f /etc/init/$service.override
done
