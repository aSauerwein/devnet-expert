# Devnet Expert Preparation
## ENV Setup
[Infrastructure List](https://learningnetwork.cisco.com/s/article/devnet-expert-equipment-and-software-list)

Virtual Router and Switches running in CML2 Personal Edition

to use all the packages on your locla machine python 3.9 is required
```
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.9 python3.9-dev python3.9-distutils
mkvirtualenv devnet-expert -p python3.9
pip install -r requirements.txt
```

## Alway on Sandboxes
### ACI Simulator
Address: https://sandboxapicdc.cisco.com/
Username: admin
Password: !v3G@!4@Y

### NSO
Address: sandbox-nso-1.cisco.com
Username: developer
Password: Services4Ever
HTTPS Port for NSO GUI/API: 443
Example Connection: https://sandbox-nso-1.cisco.com
SSH Port for direct NSO access: 22

### IOS XE on CSR (Latest)
Address: sandbox-iosxe-latest-1.cisco.com
SSH Port: 22
NETCONF Port: 830
gRPC Telemetry Port: 57500
RESTCONF Port: 443 (HTTPS) 
Username: developer
Password: C1sco12345

### IOS XE on CSR (Recommended)
Address: sandbox-iosxe-recomm-1.cisco.com 
SSH Port: 22
NETCONF Port: 830
RESTCONF Port: 443 (HTTPS) 
Username: developer
Password: C1sco12345

### IOS-XR 9000v
Address:	sandbox-iosxr-1.cisco.com
SSH Port:	22
NETCONF Port:	830
XR bash Port:	57722
gRPC Port:	57777
Username: admin
Password: C1sco12345
