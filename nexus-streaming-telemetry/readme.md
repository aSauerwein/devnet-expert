# NXOS Streaming Telemetry
## Goal
stream nexus telemtry data to telegraf over tls
## howto
### certificate for telegraf
create certificate with openssl
```
openssl req -newkey rsa:2048 -nodes -keyout telegraf.ntslab.loc.key -x509 -days 365 -out telegraf.ntslab.loc.crt
```
create secret from certificate files
```
kubectl create secret tls telegraf.ntslab.loc -n telegraf --cert telegraf.ntslab.loc.crt --key telegraf.ntslab.loc.key
```
### telegraf, influx and grafana
all 3 are installe from helm charts, see _infrastructure for details

telegraf needs to be updated to include certificate from volumemounts
```yaml
volumes:
- name: tls-certificate
  secret:
    secretName: "telegraf.ntslab.loc"
mountPoints:
- name: tls-certificate
  mountPath: /etc/telegraf/certs/
```

tls.key ald tls.crt will be mounted into `/etc/telegraf/certs/` and ca be used in the telegraf configmap
( i left these config out of the values.yaml because it could also include secret values. )
telegraf configmap is 'secret' and consists of
```ini
[[outputs.influxdb]]
  database = "telegraf"
  urls = [
    "http://influxdb.influxdb.svc.cluster.local:8086"
  ]
[[inputs.cisco_telemetry_mdt]]
  service_address = ":57500"
  tls_cert = "/etc/telegraf/certs/tls.crt"
  tls_key = "/etc/telegraf/certs/tls.key"
  transport = "grpc"
```


### switch config
* download certificate to switch
    * start http server on cws
    ```
    python3 -m http.server
    ```
    * download certificate
    ```
    copy http://192.168.1.1:8000/telegraf.ntslab.loc.crt bootflash:/telegraf.ntslab.loc.crt vrf management
    ```
    * show file to see if it's correct
    ```
    show file bootflash:/telegraf.ntslab.loc.crt
    -----BEGIN CERTIFICATE-----
    MIIDpzCCA....
    -----END CERTIFICATE-----
    ```

* telemetry config
```
feature telemetry
telemetry
  certificate /bootflash/telegraf.ntslab.loc.crt telegraf.ntslab.loc
  destination-group 1
    ip address 172.24.86.142 port 32382 protocol gRPC encoding GPB 
    use-vrf management
  sensor-group 1
    path sys/intf depth unbounded
  sensor-group 2
    data-source NX-API
    path "show environment power" depth 0
    path "show processes cpu sort" depth 0
    path "show vlan id 2-5 counters" depth 0
  subscription 1
    dst-grp 1
    snsr-grp 1 sample-interval 30000
  subscription 2
    dst-grp 1
    snsr-grp 2 sample-interval 60000
```
## configure with ansible
```
cd nexus-streaming-telemetry
ansible-playbook playbook.yml -i ../lab_configs/inventory/inventory.ym
(ansible) expert@expert-cws:~/devnet-expert/nexus-streaming-telemetry$ ansible-playbook playbook.yml -i ../lab_configs/inventory/inventory.yml 
/home/expert/venvs/ansible/lib/python3.9/site-packages/paramiko/transport.py:236: CryptographyDeprecationWarning: Blowfish has been deprecated
  "class": algorithms.Blowfish,

PLAY [NXOS Streaming Telemetry] **************************************************************************************************************************************************************************************************************

TASK [enable scp] ****************************************************************************************************************************************************************************************************************************
ok: [dev-nx9kv-1]
ok: [dev-nx9kv-2]

TASK [copy certificate to Switch] ************************************************************************************************************************************************************************************************************
ok: [dev-nx9kv-1]
ok: [dev-nx9kv-2]

TASK [write telemtry config] *****************************************************************************************************************************************************************************************************************
ok: [dev-nx9kv-2]
ok: [dev-nx9kv-1]

TASK [show telemetry transport] **************************************************************************************************************************************************************************************************************
ok: [dev-nx9kv-2]
ok: [dev-nx9kv-1]

TASK [debug] *********************************************************************************************************************************************************************************************************************************
ok: [dev-nx9kv-1] => {
    "msg": [
        "Session Id      IP Address      Port       Encoding     Transport  Status    \n--------------------------------------------------------------------------------\n0               172.24.86.142   32382      GPB          gRPC       Connected \n--------------------------------------------------------------------------------\n\nRetry buffer Size:             10485760            \nEvent Retry Messages (Bytes):  0                   \nTimer Retry Messages (Bytes):  0                   \nTotal Retries sent:            0                   \nTotal Retries Dropped:         0"
    ]
}
ok: [dev-nx9kv-2] => {
    "msg": [
        "Session Id      IP Address      Port       Encoding     Transport  Status    \n--------------------------------------------------------------------------------\n0               172.24.86.142   32382      GPB          gRPC       Connected \n--------------------------------------------------------------------------------\n\nRetry buffer Size:             10485760            \nEvent Retry Messages (Bytes):  0                   \nTimer Retry Messages (Bytes):  0                   \nTotal Retries sent:            0                   \nTotal Retries Dropped:         0"
    ]
}

PLAY RECAP ***********************************************************************************************************************************************************************************************************************************
dev-nx9kv-1                : ok=5    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
dev-nx9kv-2                : ok=5    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

## useful links
https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/sw/7-x/programmability/guide/b_Cisco_Nexus_9000_Series_NX-OS_Programmability_Guide_7x/b_Cisco_Nexus_9000_Series_NX-OS_Programmability_Guide_7x_chapter_011000.pdf


https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/sw/93x/progammability/guide/b-cisco-nexus-9000-series-nx-os-programmability-guide-93x/b-cisco-nexus-9000-series-nx-os-programmability-guide-93x_chapter_0101001.html#id_40248

https://developer.cisco.com/docs/nx-os/#!telemetry
https://beye.blog/model-driven-telemetry-with-cisco-nexus/

## troubleshooting
show telemetry transport
show telemetry data collector details


## settings
supported encodings as of:
https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/sw/93x/progammability/guide/b-cisco-nexus-9000-series-nx-os-programmability-guide-93x/b-cisco-nexus-9000-series-nx-os-programmability-guide-93x_chapter_0101001.html
```
proto — The transport protocol type of the telemetry data to be sent. NX-OS supports:
    gRPC
    HTTP
    VUDP and secure UDP (DTLS)
Supported encoded types are:
    HTTP/JSON YES
    HTTP/Form-data YES Only supported for Bin Logging.
    GRPC/GPB-Compact YES Native Data Source Only.
    GRPC/GPB YES
    UDP/GPB YES
    UDP/JSON YES
```