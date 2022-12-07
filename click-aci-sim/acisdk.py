from requests import session
from requests.packages import urllib3

class ACI:

    sess = session()
    host = ""

    def __init__(self, host, username, password, *args, **kwargs):
        self.host = host
        self.login(host, username, password, *args, **kwargs)

    def login(self, host, username, password, skip_no_verify, *args, **kwargs):
        payload = {"aaaUser": {"attributes": {"name": username, "pwd": password}}}
        url = f"https://{host}/api/aaaLogin.json"
        self.sess.verify = skip_no_verify
        if not skip_no_verify:
            # disable urlib warning
            urllib3.disable_warnings()
        result = self.sess.request(method="POST", json=payload, url=url)
        result.raise_for_status()
        token = result.json()["imdata"][0]["aaaLogin"]["attributes"]["token"]
        self.sess.headers.update({"Cookie": f"APIC-cookie={token}"})

    def listTenant(self):
        url = f"https://{self.host}/api/node/class/fvTenant.json"
        return self.sess.request(method="GET", url=url).json()

    def listL3Out(self, dn):
        url = f"https://{self.host}/api/node/mo/{dn}.json"
        params = {"query-target": "children", "target-subtree-class": "l3extOut"}
        return self.sess.request(method="GET", url=url, params=params).json()

    def getMo(self,dn,target_subtree_class,format="json"):
        url = f"https://{self.host}/api/node/mo/{dn}.json"
        params = {"query-target": "children", "target-subtree-class": target_subtree_class}
        return self.sess.request(method="GET", url=url, params=params).json()