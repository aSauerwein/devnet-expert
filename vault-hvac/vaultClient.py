import hvac

VAULT_URL = "https://asa-vault.ntslab.loc:8200"
# create token for 30days
# vault token create -policy devnet-expert -ttl 720h
VAULT_TOKEN = "hvs.CAESIN6C-Opgrmr1C4hmwneJcVNX0E26F0Uy26F7eckkfzcjGh4KHGh2cy42ZzZEOWZLQWV0dVJWZUVsNGtsdHBLV3I"

LDAP_CRED = ("user", "secretPass")


def main():
    client = token_auth(VAULT_URL, VAULT_TOKEN)
    # client = ldap_auth(VAULT_URL, LDAP_CRED)

    # get secret at given path. version allows to get specific version
    # omit or set to 0 to get latest version
    switch_credentials = get_secret_v2(client, "/devnet/switch")

    pass


def token_auth(url, token):
    client = hvac.Client(url, token, verify=False)
    if client.is_authenticated():
        return client
    else:
        raise hvac.exceptions.Unauthorized()


def ldap_auth(url, credentials):
    client = hvac.Client(url, verify=False)
    login_response = client.auth.ldap.login(
        username=credentials[0], password=credentials[1]
    )
    if client.is_authenticated():
        return client
    else:
        raise hvac.exceptions.Unauthorized()


def get_secret_v2(client, path, version=0):
    result = client.secrets.kv.v2.read_secret_version(path, version=version, mount_point="kv")
    return result["data"]["data"]


if __name__ == "__main__":
    main()
