from ncclient import manager
import xmltodict
from rich.table import Table
from rich.console import Console
from pathlib import Path
import os

HOST = "192.168.100.11"
USERNAME = "expert"
PASSWORD = "1234QWer!"
NETCONF_PORT = 830

# IETF Interface Types
IETF_INTERFACE_TYPES = {
    "loopback": "ianaift:softwareLoopback",
    "ethernet": "ianaift:ethernetCsmacd",
}


def main():
    # open connect to netconf device
    m = manager.connect(
        host=HOST,
        port=NETCONF_PORT,
        username=USERNAME,
        password=PASSWORD,
        hostkey_verify=False,
        look_for_keys=False,
        allow_agent=False,
    )

    # get_config(m, to_file=True)

    # print_cap(m, to_file=True)

    print_interfaces(m)
    
    # configure_ospf(m)

    # add loopback interface
    #add_loopback(
    #    m,
    #    {
    #        "name": "Loopback123",
    #        "desc": "configured by me",
    #        "enabled": "true",
    #        "ip_address": "3.3.3.10",
    #        "mask": "255.255.255.255",
    #    },
    #)
    m.create_subscription()
    m.close_session()


def print_cap(m: manager.Manager, to_file=False):
    """
    Print Netconf Server Capablities
    """
    for capability in m.server_capabilities:
        print(capability)
    if to_file:
        """
        Write Capabilities into a file
        """
        cap_list = ""
        for capability in m.server_capabilities:
            cap_list += str(capability) + "\n"
        Path("cap.txt").write_text(cap_list)


def get_config(m: manager.Manager, netconf_filter="", to_file=False):
    """
    Print Network Interfaces
    """
    netconf_reply = m.get_config(source="running")
    if to_file:
        Path("config.txt").write_text(netconf_reply.xml)

def configure_ospf(m: manager.Manager):
    """
    """
    config = """
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

    """
    m.edit_config(config, target="running")

def print_interfaces(m: manager.Manager):
    """
    Print Network Interfaces
    """
    netconf_filter = """
    <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
            <description>Netconf</description>
        </interface>
    </interfaces>
    </filter>"""
    netconf_reply = m.get_config(source="running", filter=netconf_filter)
    # convert reply to dict
    netconf_data = xmltodict.parse(netconf_reply.xml)["rpc-reply"]["data"]
    if netconf_data is not None:
        # Prepare output Table
        table = Table(title="Network Interfaces")
        table.add_column("Name", no_wrap=True)
        table.add_column("Description")
        table.add_column("Enabled")

        # Create a list of interfaces
        for interface in netconf_data["interfaces"]["interface"]:
            table.add_row(
                interface["name"], interface.get("description", ""), interface["enabled"]
            )
        pass
        console = Console()
        console.print(table)
    else:
        print("Netconf request returned no Data")

def add_loopback(m: manager.Manager, new_loopback: dict):
    """
    Add Loopback Interface
    """
    netconf_interface_template = """
    <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface operation="replace">
                <name>{name}</name>
                <description>{desc}</description>
                <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">
                    {type}
                </type>
                <enabled>{status}</enabled>
                <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                    <address>
                        <ip>{ip_address}</ip>
                        <netmask>{mask}</netmask>
                    </address>
                </ipv4>
            </interface>
        </interfaces>
    </config>"""
    netconf_data = netconf_interface_template.format(
        name=new_loopback["name"],
        desc=new_loopback["desc"],
        type=IETF_INTERFACE_TYPES["loopback"],
        status=new_loopback["enabled"],
        ip_address=new_loopback["ip_address"],
        mask=new_loopback["mask"],
    )
    netconf_reply = m.edit_config(netconf_data, target="running")

    pass


def add_user(m: manager.Manager, new_user: dict):
    """
    add a new User with specified privilege level
    """
    netconf_user_template = """
    <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface operation="replace">
                <name>{name}</name>
                <description>{desc}</description>
                <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">
                    {type}
                </type>
                <enabled>{status}</enabled>
                <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                    <address>
                        <ip>{ip_address}</ip>
                        <netmask>{mask}</netmask>
                    </address>
                </ipv4>
            </interface>
        </interfaces>
    </config>"""


if __name__ == "__main__":
    main()
