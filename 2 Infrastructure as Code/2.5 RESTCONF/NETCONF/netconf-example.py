from ncclient import manager
import xmltodict
from rich.table import Table
from rich.console import Console
from pathlib import Path
import os

HOST = "172.24.88.7"
USERNAME = "ibkadmin"
PASSWORD = os.getenv("NETCONFG_PASSWORD")
NETCONF_PORT = 22

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

    get_config(m, to_file=True)

    print_cap(m, to_file=True)

    print_interfaces(m)

    # add loopback interface
    add_loopback(
        m,
        {
            "name": "Loopback123",
            "desc": "configured by me",
            "enabled": "true",
            "ip_address": "3.3.3.10",
            "mask": "255.255.255.255",
        },
    )
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


def print_interfaces(m: manager.Manager):
    """
    Print Network Interfaces
    """
    netconf_filter = """
    <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
        </interface>
    </interfaces>
    </filter>"""
    netconf_reply = m.get_config(source="running", filter=netconf_filter)
    # convert reply to dict
    netconf_data = xmltodict.parse(netconf_reply.xml)["rpc-reply"]["data"]

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
