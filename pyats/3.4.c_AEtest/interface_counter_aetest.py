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


class interface_errors(aetest.Testcase):
    """interface_errors
    < docstring description of this testcase >
    """

    # List of counters keys to check for errors
    #   Model details: https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/_models/interface.pdf
    counter_error_keys = ("in_crc_errors", "in_errors", "out_errors")

    @aetest.setup
    def setup(self, testbed):
        """Learn and save the interface details from the testbed devices."""
        self.learnt_interfaces = {}
        for device_name, device in testbed.devices.items():
            # Only attempt to learn details on supported network operation systems
            if device.os in ("ios", "iosxe", "iosxr", "nxos"):
                logger.info(f"{device_name} connected status: {device.connected}")
                logger.info(f"Learning Interfaces for {device_name}")
                self.learnt_interfaces[device_name] = device.learn("interface").info
    @aetest.test
    def test(self, steps):
        # Loop over every device with learnt interfaces
        for device_name, interfaces in self.learnt_interfaces.items():
            with steps.start(
                f"Looking for Interface Errors on {device_name}", continue_=True
            ) as device_step:
                # Loop over every interface that was learnt
                for interface_name, values in interfaces.items():
                    with device_step.start(
                        f"Checking Interface {interface_name}", continue_=True
                    ) as interface_step:
                        if "counters" in values:
                            for counter in self.counter_error_keys:
                                if counter in values["counters"]:
                                    if values["counters"][counter] > 0:
                                        interface_step.failed(
                                            f'Device {device_name} Interface {interface_name} has a count of {values["counters"][counter]} for {counter}'
                                        )
                                else:
                                    # counter not supported by that interface
                                    logger.info(
                                        f"Device {device_name} Interface {interface_name} missing {counter}"
                                    )
                        else:
                            # If the interface has no counters, mark as skipped
                            interface_step.skipped(
                                f"Device {device_name} Interface {interface_name} missing counters"
                            )

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
