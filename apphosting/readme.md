## pyATS and Genie

### Exam Objectives
```
3.3	Deploy an application on a Cisco IOS XE device by leveraging the technologies of Guest Shell and application hosting
```

### Howto
#### Router ( Catalyst 800V )
1. first enable iox
```
asa-cat8000v#show iox

IOx Infrastructure Summary:
---------------------------
IOx service (CAF)              : Not Running
IOx service (HA)               : Not Supported 
IOx service (IOxman)           : Not Running
IOx service (Sec storage)      : Not Supported 
Libvirtd                       : Running

asa-cat8000v#conf t
Enter configuration commands, one per line.  End with CNTL/Z.
asa-cat8000v(config)#iox
asa-cat8000v(config)#exit
asa-cat8000v#show iox

IOx Infrastructure Summary:
---------------------------
IOx service (CAF)              : Running
IOx service (HA)               : Not Supported 
IOx service (IOxman)           : Not Running
IOx service (Sec storage)      : Not Supported 
Libvirtd                       : Running
```
2. enable container networking/nat+
```
interface gigabitEthernet 3
ip nat outside
int virtualportgroup0
ip address 192.168.100.1 255.255.255.0
ip nat inside
# create an access list to enable nat
ip access-list standard IOX_NAT
permit 192.168.100.0 0.0.0.255
ip nat inside source list IOX_NAT interface gigabitEthernet 3 overload

# assignt network config to guestshell container
app-hosting appid guestshell
app-vnic gateway0 virtualportgroup 0 guest-interface 0
guest-ipaddress 192.168.100.5 netmask 255.255.255.0
app-default-gateway 192.168.100.1 guest-interface 0
name-server0 8.8.8.8
```
3. spin up guestshell container
```
asa-cat8000v#guestshell enable
Interface will be selected if configured in app-hosting
Please wait for completion
guestshell installed successfully
Current state is: DEPLOYED
guestshell activated successfully
Current state is: ACTIVATED
guestshell started successfully
Current state is: RUNNING
Guestshell enabled successfully

asa-cat8000v#show app-hosting list
App id                                   State
---------------------------------------------------------
guestshell                               RUNNING
```
4. to access guestshell execute `guestshell`
5. to execute commands on the underlying host execute `dohost`
```
[guestshell@guestshell ~]$ dohost "show ip int brief"
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet1       unassigned      YES unset  administratively down down    
GigabitEthernet2       unassigned      YES unset  administratively down down    
GigabitEthernet3       172.24.88.114   YES DHCP   up                    up      
VirtualPortGroup0      192.168.100.1   YES manual up                    up 
```
5.a Which invokes a python script, which executes `clip` of package `cli`
```
import sys
import argparse
from cli import clip

parser = argparse.ArgumentParser(description='Execute IOS CLI commands.')
parser.add_argument('commands', metavar='"CMD"', nargs='+', help='IOS CLI command to be executed')

args = parser.parse_args()

for cmd in args.commands:
    clip(cmd)
    sys.stdout.flush()
```

### Thousandeyes
```
app-hosting install appid thousandeyes package https://downloads.thousandeyes.com/enterprise-agent/thousandeyes-enterprise-agent-4.3.0.cisco.tar
configure terminal
app-hosting appid thousandeyes
app-vnic gateway1 virtualportgroup 0 guest-interface 0
guest-ipaddress 192.168.100.10 netmask 255.255.255.0
exit
app-default-gateway 192.168.100.1 guest-interface 0
name-server0 172.24.85.10
name-server1 172.25.85.10
app-resource docker
prepend-pkg-opts
run-opts 1 "-e TEAGENT_ACCOUNT_TOKEN=y3h87ynft7uolsm0rkusm800033ila1r"
run-opts 2 "--hostname cat8000v-asauerwein"
exit
exit
exit
write memory
app-hosting activate appid thousandeyes
app-hosting start appid thousandeyes
```

## docs
https://0x2142.com/getting-started-with-ios-xe-guestshell/