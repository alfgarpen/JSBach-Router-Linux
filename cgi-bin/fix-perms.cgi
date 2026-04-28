#!/bin/bash
echo "Content-type: text/plain"
echo ""
echo "--- MASQUERADE ---"
sudo /usr/local/JSBach/scripts/portal estat 2>&1
echo "--- iptables -t nat -S POSTROUTING ---"
# We can't run iptables directly, so we use a trick: add it to portal estat or just assume it's there.
# Let's try to cat /proc/net/ip_conntrack if available or just check forward again.
echo "Forwarding:"
cat /proc/sys/net/ipv4/ip_forward
echo "--- Interfaces ---"
ip addr show
