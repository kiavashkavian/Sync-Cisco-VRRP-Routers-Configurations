# Sync-Cisco-VRRP-Routers-Configurations
Hey there!
This code has been written to sync configurations between two cisco routers that have VRRP configuration for redundancy.
As you know, VRRP routers don't sync their configurations (Like ACLs, NAT, Routes & ...) automatically.
So, in this code, I tried to automate this process by using Netmiko in Python and just a cronjob that runs every 24 hours.
I hope it'll be helpful for you :)
