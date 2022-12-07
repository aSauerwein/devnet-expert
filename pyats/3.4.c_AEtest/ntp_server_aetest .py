# Example
# -------
#
#   script arguments demo

import logging
from pyats import aetest
from genie.testbed import load
from unicon.core.errors import TimeoutError, StateMachineError, ConnectionError

logger = logging.getLogger(__name__)


class CommonSetup(aetest.CommonSetup):
    # @aetest.subsection
    # def load_testbed(self, testbed):
    #     # Convert pyATS testbed to Genie Testbed
    #     logger.info(
    #         "Converting pyATS testbed to Genie Testbed to support pyATS Library features"
    #     )
    #     testbed = load(testbed)
    #     self.parent.parameters.update(testbed=testbed)

    @aetest.subsection
    def connect(self, testbed):
        """
        establishes connection to all your testbed devices.
        """
        # make sure testbed is provided
        assert testbed, "Testbed is not provided!"

        # connect to all testbed devices
        #   By default ANY error in the CommonSetup will fail the entire test run
        #   Here we catch common exceptions if a device is unavailable to allow test to continue
        try:
            testbed.connect()
        except (TimeoutError, StateMachineError, ConnectionError):
            logger.error("Unable to connect to all devices")


class verify_connected(aetest.Testcase):
    """verify_connected
    Ensure successful connection to all devices in testbed.
    """

    @aetest.test
    def test(self, testbed, steps):
        # Loop over every device in the testbed
        for device_name, device in testbed.devices.items():
            print(type(device))
            with steps.start(
                f"Test Connection Status of {device_name}", continue_=True
            ) as step:
                # Test "connected" status
                if device.connected:
                    logger.info(f"{device_name} connected status: {device.connected}")
                else:
                    logger.error(f"{device_name} connected status: {device.connected}")
                    step.failed()

class ntp_server(aetest.Testcase):
    """
    check if right ntp server are configured
    """
    ntp_server = {"0.at.pool.ntp.org", "0.it.pool.ntp.org"}

    @aetest.setup
    def setup(self, testbed):
        self.learnt_ntp_server= {}
        for device_name, device in testbed.devices.items():
            if device.os in ("ios", "iosxe", "iosxr", "nxos"):
                logger.info(f"{device_name} connected status: {device.connected}")
                logger.info(f"Learning Interfaces for {device_name}")
                self.learnt_ntp_server[device_name] = device.learn("ntp").info
    
    @aetest.test
    def test(self, steps):
        for device_name, device in self.learnt_ntp_server.items():
            with steps.start(
                f"Looking for NTP Server on {device_name}", continue_=True
            ) as device_step:
                # check if all ntp servers are confired
                # "issubset" checks if all ntp servers are a subset of all the ntp servers configured
                # check is still passed if more then these server are configured
                learnt_ntp_server = set(device['vrf']['default']['unicast_configuration']['address'].keys())
                if not self.ntp_server.issubset(learnt_ntp_server):
                    logger.error(f"{device_name} configured ntp server {learnt_ntp_server} do not contain {self.ntp_server}")
                    device_step.failed()


class CommonCleanup(aetest.CommonCleanup):
    """CommonCleanup Section
    < common cleanup docstring >
    """

    # uncomment to add new subsections
    # @aetest.subsection
    # def subsection_cleanup_one(self):
    #     pass


# main()
if __name__ == "__main__":
    # for stand-alone execution
    import argparse
    from pyats import topology

    parser = argparse.ArgumentParser(description="standalone parser")
    parser.add_argument(
        "--testbed",
        dest="testbed",
        help="testbed YAML file",
        type=topology.loader.load,
        default=None,
    )

    # do the parsing
    args = parser.parse_known_args()[0]

    aetest.main(testbed=args.testbed)
