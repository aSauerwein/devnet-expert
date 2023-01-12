from ncclient import manager
import xmltodict
from rich.table import Table
from rich.console import Console
from pathlib import Path
import os

USERNAME = "expert"
PASSWORD = "1234QWer!"
NETCONF_PORT = 830

DEVICES = {
    "dev-c8kv-1": "192.168.100.11",
    "dev-c8kv-2": "192.168.100.12",
    "dev-c8kv-3": "192.168.100.13",
}


def main():
    # open connect to netconf device
    for device,ip in DEVICES.items():
        m = manager.connect(
            host=ip,
            port=NETCONF_PORT,
            username=USERNAME,
            password=PASSWORD,
            hostkey_verify=False,
            look_for_keys=False,
            allow_agent=False,
        )

        print(f"Configuring {device}")
        config = Path(__file__).parent / "configs" / f"{device}.xml"
        configure_ospf(m, config.read_text())
        m.close_session()

def configure_ospf(m, config):
    netconf_reply = m.edit_config(config, target="running")
    if netconf_reply.ok and netconf_reply.error == None:
        return
    else:
        print(netconf_reply.xml)

if __name__ == "__main__":
    main()