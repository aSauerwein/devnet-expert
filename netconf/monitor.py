from ncclient import manager
from ncclient.xml_ import to_ele

# worth a look https://adtran.github.io/netconf_client/api.html#module-netconf_client.ncclient


# debug
# import logging
# handler = logging.StreamHandler()
# # for l in ['ncclient.transport.session', 'ncclient.operations.rpc']:
# for l in ['ncclient.transport.ssh', 'ncclient.transport.session', 'ncclient.operations.rpc']:
#     logger = logging.getLogger(l)
#     logger.addHandler(handler)
#     logger.setLevel(logging.DEBUG)


username = "ibkadmin"
password = "XX"
wlc = "XXX"

m = manager.connect(host=wlc, port=830, username=username, password=password, hostkey_verify=False, timeout=120)

filter = """
 <establish-subscription xmlns="urn:ietf:params:xml:ns:yang:ietf-event-notifications"
   xmlns:yp="urn:ietf:params:xml:ns:yang:ietf-yang-push">
  <stream>yp:yang-push</stream>
  <yp:xpath-filter>/access-point-oper-data/capwap-data/name|/access-point-oper-data/capwap-data/ip-addr|/access-point-oper-data/capwap-data/ap-state</yp:xpath-filter>
  <yp:period>300</yp:period>
 </establish-subscription>
"""

# m.create_subscription(filter=("xpath", "/process-cpu-ios-xe-oper:cpu-usage/process-cpu-ios-xe-oper:cpu-utilization/process-cpu-ios-xe-oper:five-seconds"))
m.dispatch(to_ele(filter))

# m.establish_subscription(
#     xpath="/process-cpu-ios-xe-oper:cpu-usage/process-cpu-ios-xe-oper:cpu-utilization/process-cpu-ios-xe-oper:five-seconds"
# )


while True:
    print("Waiting for next notification")

    # This will block until a notification is received because
    # we didn't pass a timeout or block=False
    n = m.take_notification()
    print(n.notification_xml)
