#!/bin/bash

. /etc/sysconfig/heat-params

echo "configuring mesos (slave)"

myip=$(ip addr show eth0 |
       awk '$1 == "inet" {print $2}' | cut -f1 -d/)

# This specifies how to connect to a master or a quorum of masters
echo "zk://$MESOS_MASTER_IP:2181/mesos" > /etc/mesos/zk

# The hostname the slave should report
echo "$myip" > /etc/mesos-slave/hostname

# The IP address to listen on
echo "$myip" > /etc/mesos-slave/ip

# List of containerizer implementations
echo "docker,mesos" > /etc/mesos-slave/containerizers

# Amount of time to wait for an executor to register
cat > /etc/mesos-slave/executor_registration_timeout <<EOF
$EXECUTOR_REGISTRATION_TIMEOUT
EOF

function join { local IFS="$1"; shift; echo "$*"; }
resolvers=($(awk '/^nameserver/ { printf "\"%s\"\n", $2 }' /etc/resolv.conf))
resolvers=$(join , "${resolvers[@]}")
mkdir -p /etc/mesos-dns
cat > /etc/mesos-dns/config.js <<EOF
{
  "zk": "zk://$MESOS_MASTER_IP:2181/mesos",
  "refreshSeconds": 5,
  "ttl": 60,
  "domain": "mesos",
  "port": 53,
  "resolvers": [$resolvers],
  "timeout": 5,
  "email": "root.mesos-dns.mesos"
}
EOF
