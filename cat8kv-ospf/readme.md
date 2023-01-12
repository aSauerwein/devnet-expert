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
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <router>
            <router-ospf xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ospf">
                <ospf>
                    <process-id>
                        <id>1</id>
                        <network>
                            <ip>10.10.12.0</ip>
                            <wildcard>255.255.255.0</wildcard>
                            <area>0</area>
                        </network>
                        <network>
                            <ip>10.10.13.0</ip>
                            <wildcard>255.255.255.0</wildcard>
                            <area>0</area>
                        </network>
                        <network>
                            <ip>10.1.0.0</ip>
                            <wildcard>255.255.255.0</wildcard>
                            <area>0</area>
                        </network>
                        <router-id>1.1.1.1</router-id>
                    </process-id>
                </ospf>
            </router-ospf>
        </router>
        <interface>
            <GigabitEthernet>
                <name>1</name>
                <switchport>
                    <trunk xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-switch">
                        <native>
                            <vlan-config>
                                <tag>true</tag>
                            </vlan-config>
                        </native>
                    </trunk>
                </switchport>
                <ip>
                    <address>
                        <primary>
                            <address>10.0.12.1</address>
                            <mask>255.255.255.0</mask>
                        </primary>
                    </address>
                    <router-ospf xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ospf">
                        <ospf>
                            <process-id>
                                <id>1</id>
                                <area>
                                    <area-id>0</area-id>
                                </area>
                            </process-id>
                        </ospf>
                    </router-ospf>
                </ip>
            </GigabitEthernet>
            <GigabitEthernet>
                <name>3</name>
                <switchport>
                    <trunk xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-switch">
                        <native>
                            <vlan-config>
                                <tag>true</tag>
                            </vlan-config>
                        </native>
                    </trunk>
                </switchport>
                <ip>
                    <address>
                        <primary>
                            <address>10.0.13.1</address>
                            <mask>255.255.255.0</mask>
                        </primary>
                    </address>
                    <router-ospf xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ospf">
                        <ospf>
                            <process-id>
                                <id>1</id>
                                <area>
                                    <area-id>0</area-id>
                                </area>
                            </process-id>
                        </ospf>
                    </router-ospf>
                </ip>
            </GigabitEthernet>
        </interface>
    </native>
</config>
```
* small script `apply-configs.py` will look for .xml config files and sends an netconf edit-config rpc to update the device configiration
* it seems like ios-xe-native cannot enable interfaces, but ietf-interfaces can
```xml
    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
      <interface>
        <name>GigabitEthernet1</name>
        <enabled>true</enabled>
      </interface>
    </interfaces>
```
* connect with ssh to check if all router have the correct routing table:
```
dev-c8kv-3#show ip route
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area 
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2, m - OMP
       n - NAT, Ni - NAT inside, No - NAT outside, Nd - NAT DIA
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       H - NHRP, G - NHRP registered, g - NHRP registration summary
       o - ODR, P - periodic downloaded static route, l - LISP
       a - application route
       + - replicated route, % - next hop override, p - overrides from PfR
       & - replicated local route overrides by connected

Gateway of last resort is not set

      10.0.0.0/8 is variably subnetted, 9 subnets, 2 masks
O        10.0.12.0/24 [110/2] via 10.0.23.2, 00:09:33, GigabitEthernet2
                      [110/2] via 10.0.13.1, 00:10:59, GigabitEthernet3
C        10.0.13.0/24 is directly connected, GigabitEthernet3
L        10.0.13.3/32 is directly connected, GigabitEthernet3
C        10.0.23.0/24 is directly connected, GigabitEthernet2
L        10.0.23.3/32 is directly connected, GigabitEthernet2
O        10.1.0.1/32 [110/2] via 10.0.13.1, 00:03:28, GigabitEthernet3
O        10.2.0.1/32 [110/2] via 10.0.23.2, 00:03:26, GigabitEthernet2
C        10.3.0.0/24 is directly connected, Loopback1
L        10.3.0.1/32 is directly connected, Loopback1
```
