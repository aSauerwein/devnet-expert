from scrapli import Scrapli

from vaultClient import token_auth, get_secret_v2
import os

# export VAULT_TOKEN='hvs.CAESIN6C-Opgrmr1C4hmwneJcVNX0E26F0Uy26F7eckkfzcjGh4KHGh2cy42ZzZEOWZLQWV0dVJWZUVsNGtsdHBLV3I'
client = token_auth("https://asa-vault.ntslab.loc:8200", os.environ.get("VAULT_TOKEN"))
credentials = get_secret_v2(client,"devnet/switch")

my_device = {
    "host": "192.168.100.11",
    "auth_username": credentials["username"],
    "auth_password": credentials["password"],
    "platform": "cisco_iosxe",
    "auth_strict_key": False,
}

conn = Scrapli(**my_device)
conn.open()
response = conn.send_command("show version")
print(response.result)

pass
