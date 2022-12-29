# CML2 Lab Configs
## Preparation
* download qcow2 image from https://learningnetwork.cisco.com/s/article/devnet-expert-equipment-and-software-list
* upload to cml2 instance
* create new image definition from https://github.com/CiscoDevNet/cml-community/tree/master/node-definitions/cisco/cws
* import lab yaml
* update IP address of dev-edge-1 gi0/15 ("public" interface) and default gateway to your needs
* start lab
* now the cws ubuntu workstation should be availble over your lab public with ssh(tcp/22) and rdp (tcp/3389)

## Topology

### Devices
Device | username | password | MGMT-IP | NAT-IP | Type | Description
---|---|---|---|---|---|---
dev-edge-1 | expert | 1234QWer! | 172.24.88.7 | N/A | IOS L3 | dynamic NAT for MGMT and CWS Lan, Static NAT for CWS ( ssh, rdp )
dev-cws-1 | root/expert | 1234QWer! | 192.168.1.1 | 172.24.88.7 | Ubuntu | Ubuntu Candiate Workstation. SSH and RDP
dev-mgmt-1 | expert | 1234QWer! | 192.168.100.250 | N/A | IOS L2 | L2 Switch for MGMT Lan
dev-c8kv-1 | expert | 1234QWer! | 192.168.100.11 | N/A | Catalyst 8000v 
dev-c8kv-2 | expert | 1234QWer! | 192.168.100.12 | N/A | Catalyst 8000v
dev-c8kv-3 | expert | 1234QWer! | 192.168.100.13 | N/A | Catalyst 8000v
dev-iosv-1 | expert | 1234QWer! | 192.168.100.21 | N/A | IOSv L3
dev-iosv-1 | expert | 1234QWer! | 192.168.100.22 | N/A | IOSv L3
dev-iosv-1 | expert | 1234QWer! | 192.168.100.23 | N/A | IOSv L3
dev-iosvl2-1 | expert | 1234QWer! | 192.168.100.31 | N/A | IOSv L2
dev-nx9kv-1 | expert | 1234QWer! | 192.168.100.41 | N/A | Nexus 9000v
dev-nx9kv-1 | expert | 1234QWer! | 192.168.100.42 | N/A | Nexus 9000v

### VLANS
ID | Desc | Subnet | Gateway
---|---|---|---
100 | MGMT | 192.168.100.0/24 | 192.168.100.254


### infos
https://blogs.cisco.com/developer/363-askhankcml2-01  
https://cml2.ntslab.loc/api/v0/ui/