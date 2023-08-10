# Network Services Orchestrator
## Blueprint Topics covered
2.10	Create a basic Cisco NSO service package to meet given business and technical requirements. The service would generate a network configuration on the target device platforms using the "cisco-ios-cli" NED and be of type "python-and-template"
2.10.a	Create a service template from a provided NSO device configuration
2.10.b	Create a basic YANG module for the service containers (including lists, leaf lists, data types, leaf references, and single argument "when" and "must" conditions)
2.10.c	Create basic actions to verify operational status of the service
2.10.d	Monitor service status by reviewing the NCS Python VM log file
# devnet learning labs
https://developer.cisco.com/learning/tracks/get_started_with_nso/nso/



## ACL-Service
Hank Preston shows in BRKCRT-2050 a few examples from Devnet Expert Exam.
On slide 65 there is an example NSO Service called `acl-service`
https://www.ciscolive.com/on-demand/on-demand-details.html?#/session/1670019628164001nq9F
the ncs package in `acl-service` directory exaclty matches the service described on slide 65

Note: yes, python is not needed in this example, but the blueprint explicitely mentions "python-and-template"