# CML2 Lab Configs
## Topology

## Devices
Device | username | password | MGMT-IP | NAT-IP | Type | Description
---|---|---|---|---|---|---
dev-edge-1 | expert | 1235QWer! | 172.24.88.7 | N/A | IOS L3 | dynamic NAT for MGMT and CWS Lan, Static NAT for CWS ( ssh, rdp )
dev-cws-1 | root/expert | 1235QWer! | 192.168.1.1 | 172.24.88.7 | Ubuntu | Ubuntu Candiate Workstation. SSH and RDP
dev-mgmt-1 | expert | 1235QWer! | N/A | N/A | IOS L2 | L2 Switch for MGMT Lan
dev-c8kv-1 | expert | 1235QWer! | 192.168.100.11 | N/A | Catalyst 8000v 
dev-c8kv-2 | expert | 1235QWer! | 192.168.100.12 | N/A | Catalyst 8000v
dev-c8kv-3 | expert | 1235QWer! | 192.168.100.13 | N/A | Catalyst 8000v 


## infos
https://blogs.cisco.com/developer/363-askhankcml2-01
https://cml2.ntslab.loc/api/v0/ui/
