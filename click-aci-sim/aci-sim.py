#!/usr/bin/env python
# small script to interact with ACI simulator


import click
import requests
from acisdk import ACI
from rich import print
from rich.table import Table
from rich.console import Console

console = Console()


@click.command()
@click.option("-h", "--host", required=True)  # sandboxapicdc.cisco.com
@click.option("-u", "--username", required=True)  # admin
@click.option("-p", "--password", required=True)  # !v3G@!4@Y
@click.option("-k", "--skip-no-verify", default=True, is_flag=True)  # !v3G@!4@Y
@click.option("--debug/--no-debug", default=False)
def cli(host, username, password, *args, **kwargs):
    click.echo("Debug mode is %s" % ("on" if kwargs.get("debug") else "off"))
    aci = ACI(host, username, password, *args, **kwargs)
    tenants = aci.listTenant()
    print_table(
        ["name", "dn", "uid"],
        tenants["imdata"],
        subkey1="fvTenant",
        subkey2="attributes",
    )

    tenant_id = click.prompt("Please select a Tenant by ID", type=int)

    l3outs = aci.listL3Out(dn=tenants["imdata"][tenant_id]["fvTenant"]["attributes"]["dn"])
    print_table(
        ["name", "dn", "uid"],
        l3outs["imdata"],
        subkey1="l3extOut",
        subkey2="attributes",
    )
    l3out_id = click.prompt("Please select a L3Out by ID", type=int)

    epgs = aci.getMo(l3outs["imdata"][l3out_id]["l3extOut"]["attributes"]["dn"], "l3extInstP")
    print_table(
        ["name", "dn", "uid"],
        epgs["imdata"],
        subkey1="l3extInstP",
        subkey2="attributes",
    )
    
    epg_id = click.prompt("Please select a EGP by ID", type=int)
    epgs = aci.getMo(epgs["imdata"][epg_id]["l3extInstP"]["attributes"]["dn"], "l3extSubnet")
    print_table(
        ["name", "dn", "ip", "uid"],
        epgs["imdata"],
        subkey1="l3extSubnet",
        subkey2="attributes",
    )

def print_table(fields, data, title="", subkey1="", subkey2=""):
    table = Table(title=title)
    table.add_column("ID")
    for field in fields:
        table.add_column(field)
    for id, line in enumerate(data):
        if subkey1:
            if subkey2:
                values = [line[subkey1][subkey2][f] for f in fields]
            else:
                values = [line[subkey1][f] for f in fields]
        else:
            values = [line[f] for f in fields]
        
        values.insert(0,str(id))
        table.add_row(*values)

    console.print(table)


if __name__ == "__main__":
    cli(auto_envvar_prefix="DE")
