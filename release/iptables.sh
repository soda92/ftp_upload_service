#!/bin/bash
echo 1 > /proc/sys/net/ipv4/ip_forward

/sbin/iptables -t nat -A POSTROUTING -o ppp0 -j MASQUERADE
/sbin/iptables -A FORWARD -i ppp0 -o eth0 -m state --state RELATED,ESTABLISHED -j ACCEPT
/sbin/iptables -A FORWARD -i eth0 -o ppp0 -j ACCEPT
