## Ansible and IOS

### Exam Objectives
```
3.2	Automate the configuration of a Cisco IOS XE network device (based on a provided architecture and configuration), including these components:
	
    3.2.a	Interfaces
    3.2.b	Static routes
    3.2.c	VLANs
    3.2.d	Access control lists
    3.2.e	BGP peering
    3.2.f	BGP and OSPF routing tables
    3.2.g	BGP and OSPF neighbors
```

### Preparation
1. instll ansible
```
pip install ansible==2.9.26
```
2. optional: Install cisco ACI Module ( included in CWS )
```
ansible-galaxy collection install cisco.aci:2.1.0
```
3. list of available modules: https://docs.ansible.com/ansible/2.9/modules/list_of_network_modules.html#ios
4. fill in variables at inventory.yml and group_vars.
5. execute
```
ansible-playbook -i inventory.yml playbook.yml
```