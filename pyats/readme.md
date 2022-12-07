## pyATS and Genie

### Exam Objectives
```
3.4 Modify and troubleshoot an automated test by using pyATS to meet requirements

    3.4.a Create a testbed file for connecting to Cisco IOS, IOS XE, or NX-OS devices

    3.4.b Gather current configuration and operational state from devices using the Genie parsers and models included with pyATS

    3.4.c Develop and execute test jobs and scripts using AEtest to verify network health
```

### Usage
You must set the following environment variables for the testbed to load properly:
`PYATS_USER`, `PYATS_PASS`, `PYATS_ENABLE_PASS`

To parse device data via Python script:
`python device_parser_script.py`

To learn device features and perform diff:
```
Snapshot #1
pyats learn interface --testbed=testbed.yml --output output

**Force change in interface (i.e. shut interface, remove BGP neighbor statement, etc.)**

Snapshot #2
pyats learn interface --testbed=testbed.yml --output output2

Diff
genie diff output output2
```

It's also possible to learn all. 
pyats learn all --testbed-testbed.yml shows every possible module:
```
['acl', 'arp', 'bgp', 'dot1x', 'eigrp', 'fdb', 'hsrp', 'igmp', 'interface', 'isis', 'lag', 'lisp', 'lldp', 'mcast', 'mld', 'msdp', 'nd', 'ntp', 'ospf', 'pim', 'platform', 'prefix_list', 'rip', 'route_policy', 'routing', 'static_routing', 'stp', 'utils', 'vlan', 'vrf', 'vxlan', 'config']' on devices '
```

## 3.4.c Develop and execute test jobs and scripts using AEtest to verify network health
Check for Interface Error counter
```
pyats run job 3.4.c_AEtest/test_job.py --testbed-file=testbed.yml 
```
Check if ntp servers are configured
```
pyats run job 3.4.c_AEtest/test_job_ntp.py --testbed-file=testbed.yml 
```

## helpful links
https://github.com/hpreston/intro-network-tests
