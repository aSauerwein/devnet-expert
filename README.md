# Devnet Expert Preparation
## ENV Setup
[Infrastructure List](https://learningnetwork.cisco.com/s/article/devnet-expert-equipment-and-software-list)

Virtual Router and Switches running in CML2 Personal Edition

to use all the packages on your locla machine python 3.9 is required
```
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.9 python3.9-dev python3.9-distutils
mkvirtualenv devnet-expert -p python3.9
pip install -r requirements.txt
```

## Candidate Workstation
username: expert
password: 1234QWer!
username: root
password: 1234QWer!

## Alway on Sandboxes
### ACI Simulator
Address: https://sandboxapicdc.cisco.com/
Username: admin
Password: !v3G@!4@Y

### NSO
Address: sandbox-nso-1.cisco.com
Username: developer
Password: Services4Ever
HTTPS Port for NSO GUI/API: 443
Example Connection: https://sandbox-nso-1.cisco.com
SSH Port for direct NSO access: 22

### IOS XE on CSR (Latest)
Address: sandbox-iosxe-latest-1.cisco.com
SSH Port: 22
NETCONF Port: 830
gRPC Telemetry Port: 57500
RESTCONF Port: 443 (HTTPS) 
Username: developer
Password: C1sco12345

### IOS XE on CSR (Recommended)
Address: sandbox-iosxe-recomm-1.cisco.com 
SSH Port: 22
NETCONF Port: 830
RESTCONF Port: 443 (HTTPS) 
Username: developer
Password: C1sco12345

### IOS-XR 9000v
Address:	sandbox-iosxr-1.cisco.com
SSH Port:	22
NETCONF Port:	830
XR bash Port:	57722
gRPC Port:	57777
Username: admin
Password: C1sco12345

## MDT on IOS XR
https://developer.cisco.com/learning/labs/03-iosxr-02-telemetry-python/enabling-model-driven-telemetry-on-the-router/
grpc config and sensor path
```
grpc
 no-tls
 port 57777
!
telemetry model-driven
 sensor-group IPV6Neighbor
  sensor-path Cisco-IOS-XR-ipv6-nd-oper:ipv6-node-discovery/nodes/node/neighbor-interfaces/neighbor-interface/host-addresses/host-address
 !
 subscription IPV6
  sensor-group-id IPV6Neighbor sample-interval 15000
 !
!
end
```
grpc status
```
RP/0/RP0/CPU0:r1#show grpc status
Mon Aug 27 02:04:06.558 UTC
*************************show gRPC status**********************
---------------------------------------------------------------
transport                       :     grpc
access-family                   :     tcp4
TLS                             :     disabled
trustpoint                      :     NotSet
listening-port                  :     57777
max-request-per-user            :     10
max-request-total               :     128
vrf-socket-ns-path              :     global-vrf
_______________________________________________________________
*************************End of showing status*****************
RP/0/RP0/CPU0:r1#

```

Telemtry model info
```
RP/0/RP0/CPU0:r1#show  telemetry model-driven subscription IPV6 internal
Wed Nov 30 22:32:23.451 UTC
Subscription:  IPV6
-------------
  State:       NA
  Sensor groups:
  Id: IPV6Neighbor
    Sample Interval:      15000 ms
    Sensor Path:          Cisco-IOS-XR-ipv6-nd-oper:ipv6-node-discovery/nodes/node/neighbor-interfaces/neighbor-interface/host-addresses/host-address
    Sensor Path State:    Resolved

  Collection Groups:
  ------------------
  No active collection groups
```

MDT telemtry collection test
```
RP/0/RP0/CPU0:r1#run mdt_exec -s Cisco-IOS-XR-ipv6-nd-oper:ipv6-node-discovery/nodes/node/neighbor-interfaces/neighbor-i$
Wed Nov 30 22:29:41.560 UTC
Enter any key to exit...
 Sub_id 200000001, flag 0, len 0
 Sub_id 200000001, flag 4, len 2175
--------
{"node_id_str":"r1","subscription_id_str":"app_TEST_200000001","encoding_path":"Cisco-IOS-XR-ipv6-nd-oper:ipv6-node-discovery/nodes/node/neighbor-interfaces/neighbor-interface/host-addresses/host-address","collection_id":1,"collection_start_time":1669847383828,"msg_timestamp":1669847383850,"data_json":[{"timestamp":1669847383849,"keys":{"node-name":"0/0/CPU0","interface-name":"GigabitEthernet0/0/0/0","host-address":"1010:1010::20"},"content":{"last-reached-time":{"seconds":156},"reachability-state":"reachable","link-layer-address":"5254.0093.8ab0","encapsulation":"arpa","selected-encapsulation":"arpa","origin-encapsulation":"dynamic","interface-name":"Gi0/0/0/0","location":"0/0/CPU0","is-router":true,"serg-flags":255,"vrfid":1610612736}},{"timestamp":1669847383849,"keys":{"node-name":"0/0/CPU0","interface-name":"GigabitEthernet0/0/0/0","host-address":"fe80::5054:ff:fe93:8ab0"},"content":{"last-reached-time":{"seconds":142},"reachability-state":"reachable","link-layer-address":"5254.0093.8ab0","encapsulation":"arpa","selected-encapsulation":"arpa","origin-encapsulation":"dynamic","interface-name":"Gi0/0/0/0","location":"0/0/CPU0","is-router":true,"serg-flags":255,"vrfid":1610612736}},{"timestamp":1669847383849,"keys":{"node-name":"0/0/CPU0","interface-name":"GigabitEthernet0/0/0/0","host-address":"ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff"},"content":{"last-reached-time":{"seconds":0},"reachability-state":"reachable","link-layer-address":"0000.0000.0000","encapsulation":"arpa","selected-encapsulation":"arpa","origin-encapsulation":"static","interface-name":"Gi0/0/0/0","location":"0/0/CPU0","is-router":false,"serg-flags":255,"vrfid":1610612736}},{"timestamp":1669847383851,"keys":{"node-name":"0/0/CPU0","interface-name":"GigabitEthernet0/0/0/1","host-address":"ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff"},"content":{"last-reached-time":{"seconds":0},"reachability-state":"reachable","link-layer-address":"0000.0000.0000","encapsulation":"arpa","selected-encapsulation":"arpa","origin-encapsulation":"static","interface-name":"Gi0/0/0/1","location":"0/0/CPU0","is-router":false,"serg-flags":255,"vrfid":1610612736}}],"collection_end_time":1669847383857}
--------
 Sub_id 200000001, flag 4, len 2175
```