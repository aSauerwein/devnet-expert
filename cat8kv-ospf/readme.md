# Create OSPF on cat8kv with netconf
* sample ospf configuration
```
router ospf 1
 router-id 1.1.1.1
 network 10.10.12.0 0.0.0.255 area 0
 network 10.10.13.0 0.0.0.255 area 0
interface GigabitEthernet1
 ip ospf 1 area 0
interface GigabitEthernet3
 ip ospf 1 area 0
end
```

## how to
* configure one of the cat8k router by hand
* connect to yang explorer and create a new device profile "dev-cat8kv-1"
* create a new file repository "devnet-expert"
* select netconf and your pervious created device profile and click "get schema list"
* "download schema list" into your repository
* create a new yang-module set "devnet-expert"
    * use previous created repository
    * add entire repistory to module set
* now use protocols -> netconf to download the configuration
    * yang-set: devnet-expert
      modules: cisco-ios-xe-ospf
      netconf-operation: get-config
      device: dev-cat8kv-1
    * build rpc, run rpc
* a new tab will open which shows the complete configuration. copy everything you need
```xml

```
